from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
 
class BlogView(View):
    def get(self, request, *args, **kwargs):
        context={
        }
        return render(request, 'blog.html', context)

def contact(request):
    if request.method == 'POST':
        subject= request.POST['subject']
        comentario= request.POST['comentario'] + ', ' + request.POST['mail'] + ', ' + request.POST['name'] + ', ' + request.POST['num']
        email_from= settings.EMAIL_HOST_USER
        recipient_list = ['institutodeinglescye@gmail.com']
        send_mail(subject, comentario, email_from, recipient_list)
        return render(request, 'blog.html')
    return render(request, 'contac.html')
