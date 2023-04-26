from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, UserEditForm, SetPasswordForm, TasksForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Tarea
from django.utils import timezone

class Alumnos(View):
    def get(self, request, *args, **kwargs):
        context={
        }
        return render(request, 'alumnos/inicio_alumnos.html', context)

def cuentaAlumnos(request):
    return render(request, 'alumnos/cuenta_alumnos.html')

class VRegistro(View):
    def get(self, request):
        form=CustomUserCreationForm()
        return render(request, "alumnos/registro/registro.html", {"form":form})

    def post(self, request):
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
           form.save()
           messages.success(self.request, f'Usuario Registrado con Exito')
           return redirect('alumno:cuenta')
        
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
    
            return render(request, "alumnos/registro/registro.html", {"form":form})


def cerrar_sesion(request):
    logout(request)
    return redirect('alumno:logear')

def logear(request):
    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario=form.cleaned_data.get("username")
            contra=form.cleaned_data.get("password")
            usuario=authenticate(username=nombre_usuario, password=contra)
            if usuario is not None:
                login(request, usuario)
                return redirect('alumno:cuenta')
            else:
                messages.error(request, "Usuario no Valido")
        else:
            messages.error(request, "Informacion Incorrecta")

    form=AuthenticationForm()
    return render(request, "alumnos/login/login.html", {"form":form})

@login_required
def editar_Perfil(request):
    usuario=request.user
    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST)
        if miFormulario.is_valid():
            informacion = miFormulario.cleaned_data
            usuario.email = informacion["email"]
            usuario.last_name = informacion["last_name"]
            usuario.first_name = informacion["first_name"]
            usuario.save()
            messages.success(request, f'Usuario Editado con Exito')
            return render(request,"alumnos/cuenta_alumnos.html")
    else:
        miFormulario = UserEditForm(initial={'email':usuario.email})
    return render(request,"alumnos/editar/editasperfil.html", {"miFormulario":miFormulario, "usuario":usuario})


@login_required
def editar_password(request):
    usuario=request.user
    if request.method == 'POST':
        form = SetPasswordForm(usuario, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Password Editada con Exito')
            logout(request)
            return redirect('alumno:cuenta')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
    form = SetPasswordForm(usuario)
    return render(request,"alumnos/editar/editar.pass.html", {"form":form})

@login_required
def tasks(request):
    tasks = Tarea.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_complete(request):
    tasks = Tarea.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def taskDetail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Tarea, pk = task_id, user=request.user)
        form=TasksForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form':form})
    else: 
        try:
            task = get_object_or_404(Tarea, pk = task_id, user=request.user)
            form = TasksForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form':form, 'error': 'Error al actulizar su tarea'})
            
@login_required            
def complete_task(request, task_id):
    task = get_object_or_404(Tarea, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.dateCompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Tarea, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
@login_required
def createTasks(request):
    if request.method == 'GET':
        return render(request, 'create_tasks.html', {'form': TasksForm})
    else:
        try:
            form = TasksForm(request.POST)
            new_task = form.save(commit = False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_tasks.html', {'form': TasksForm, 'error':'Coloque un dato valido' })