from django import forms  
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm 
from .models import Tarea
from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm):  
    username = forms.CharField(label='Nombre de Usuario', min_length=5, max_length=150)  
    email = forms.EmailField(label='Email')  
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)  
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user  


class UserEditForm(UserCreationForm):
    email = forms.EmailField(label='Modificar su email')
    last_name = forms.CharField(label='Modificar su apellido')
    first_name = forms.CharField(label='Modificar su nombre')

    class Meta:
        model = User
        fields = ['email','last_name','first_name']

    def __init__(self, *args, **kwargs):
       super(UserEditForm, self).__init__(*args, **kwargs)
       del self.fields['password1']
       del self.fields['password2'] 


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']
              
class TasksForm(ModelForm):
    class Meta:
        model = Tarea
        fields = ['title', 'descripcion']