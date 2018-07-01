from django.urls import path

from .views import *

app_name = 'pastebox'


urlpatterns=[
    path('', LoginView.as_view(), name='login'),
    path('signup/',SignupView.as_view(), name='signup'),
    path('logout/',log_out, name='logout'),
    path('lists/',PastesListView.as_view(),name='pastelists'),
    path('lists/add',AddPaste.as_view(),name='newpaste'),
    path('show/<str:pk>',ShowPaste.as_view(),name='showpaste'),
    path('delete/<str:pk>',DelPaste.as_view(),name='delpaste'),
    path('edit/<str:pk>',EditPaste.as_view(),name='editpaste'),
    #will display a content for anonymus user for the given url if exists.
    path('<str:pk>',ViewPaste.as_view(),name='showingpaste'),
    path('about/',AboutView.as_view(),name='about')
]