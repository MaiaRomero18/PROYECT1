from django.urls import path
from .views import BlogView
from blog import views


app_name='blog'

urlpatterns = [
  path('', BlogView.as_view(), name=('home')),
  path('contact/', views.contact, name='contact')  
]
