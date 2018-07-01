from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pastes(models.Model):
    user = models.ForeignKey(User, models.CASCADE)

    title = models.CharField(max_length=64)
    type= models.CharField(max_length=32 ,default="text")
    content=models.TextField(max_length=None)
    expiryon=models.DateField(blank=False,null=False)
    code=models.CharField(primary_key=True,max_length=10)

    def __str__(self):
        return self.title
