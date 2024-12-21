from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import *



class CreateUserForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['phone','username','email','password1','password2','last_name','first_name','img','age','gender','position']


class ChangeUser(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ['username']
    