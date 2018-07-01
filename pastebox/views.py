from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from .forms import *
from django.http import HttpResponse
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.contrib.auth.decorators import login_required
from datetime import datetime

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form = LoginForm()
        return render(request,'pastebox/login.html',{'form':form,'message':None})

    def post(self,request,*args,**kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            values = list(form.cleaned_data.values())
            user=authenticate(request,username=values[0],password=values[1])
            if user is not None:
                login(request,user)
                return redirect('pastebox:pastelists')
            else:
                return render(request,'pastebox/login.html',{'form':form,'message':'Invalid credentials!'})

class SignupView(View):
    def get(self,request,*args,**kwargs):
        form = SignupForm()
        return render(request,'pastebox/signup.html',{'form':form,'errors':None})
    def post(self,request,*args,**kwargs):
        form=SignupForm(request.POST)
        if form.is_valid():
            values=list(form.cleaned_data.values())
            try:
                User.objects.create_user(username=values[0],password=values[2],email=values[1])
                return redirect('pastebox:login')
            except IntegrityError:
                return render(request, 'pastebox/signup.html', {'form': SignupForm, 'errors': 'User already exists!'})
        else:
            return render(request,'pastebox/signup.html',{'form':SignupForm,'errors':form.errors})

def log_out(request):
    logout(request)
    return redirect('pastebox:login')
#
# def Index(request):
#     if request.user.is_authenticated:
#         return HttpResponse("hello hi how are youu "+str(request.user))
#     return redirect(to='/pastebox/',error_message="Please Login")

class PastesListView(LoginRequiredMixin,ListView):
    login_url='pastebox:login'
    context_object_name = 'pastes_list'
    template_name = "pastebox/pastelist.html"
    def get_queryset(self):
        return Pastes.objects.filter(user=self.request.user.id,expiryon__gt=datetime.now())

class AddPaste(LoginRequiredMixin,CreateView):
    login_url = 'pastebox:login'
    success_url = 'pastebox:pastelists'
    model=Pastes
    def get(self,request,*args,**kwargs):
        form = PastesForm()
        return render(request,'pastebox/add_paste.html',{'form':form,'message':None})

    def post(self,request,*args,**kwargs):
        form = PastesForm(request.POST)
        if form.is_valid():
            data=list(form.cleaned_data.values())
            form=form.save(commit=False)
            if datetime.now().date() > form.expiryon:
                return render(request, 'pastebox/add_paste.html', {'form': PastesForm, 'errors': 'Please enter a proper date'})
            import uuid
            form.code=uuid.uuid4().hex[:6].upper()
            user=User.objects.get(id=request.user.id)
            form.user=user
            form.save()
            return redirect(to='pastebox:pastelists')
        else:
            return render(request,'pastebox/add_paste.html',{'form':PastesForm,'errors':'Please fill the form correctly'})


class ShowPaste(LoginRequiredMixin,DetailView):
    login_url = 'pastebox:login'
    context_object_name = 'paste_object'
    template_name = "pastebox/showpaste.html"

    def get_queryset(self):
        return Pastes.objects.filter(code=self.kwargs['pk'])

class EditPaste(LoginRequiredMixin,UpdateView):
    login_url = 'pastebox:login'
    success_url = 'pastebox:pastelists'
    model=Pastes
    fields=['title','type','content','expiryon']
    template_name = 'pastebox/add_paste.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Pastes, code=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(EditPaste, self).get_context_data(**kwargs)
        paste=Pastes.objects.get(code=self.kwargs['pk'])
        form = PastesForm(instance=paste)
        return {'form': context.get("form")}

    def post(self,request,*args,**kwargs):
        form = PastesForm(request.POST)
        if form.is_valid():
            data=list(form.cleaned_data.values())
            form=form.save(commit=False)
            if datetime.now().date() > data[3]:
                return redirect(to=request.path,kwargs={'message':'Please fill a valid date'})
                #return render(request,'pastebox/add_paste.html', {'form': PastesForm(instance=Pastes.objects.get(code=self.kwargs['pk'])), 'errors': 'Please enter a proper date'})
            form.code=self.kwargs['pk']
            form.user=request.user
            form.save()
            return redirect(to='pastebox:pastelists')
        else:
            return redirect(to=request.path, kwargs={'message': 'Please fill a valid date'})

class DelPaste(LoginRequiredMixin,View):
    login_url = login_url = 'pastebox:login'
    def get(self,request,*args,**kwargs):
        Pastes.objects.filter(code=kwargs['pk']).delete()
        return redirect(to='pastebox:pastelists')


class ViewPaste(DetailView):
    context_object_name = 'paste_object'
    template_name = "pastebox/viewpastes.html"

    def get_queryset(self):
        return Pastes.objects.filter(code=self.kwargs['pk'])

class AboutView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'pastebox/about.html')