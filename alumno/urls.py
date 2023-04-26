from django.urls import path
from .views import  Alumnos, VRegistro, cerrar_sesion,logear,editar_Perfil,editar_password, tasks, tasks_complete, createTasks, taskDetail, complete_task, delete_task
from alumno import views

app_name='alumno'

urlpatterns = [
      path('', Alumnos.as_view(), name=('home')),
      path('Autenticacion/', VRegistro.as_view(), name="Autenticacion"),
      path('cuenta/', views.cuentaAlumnos, name='cuenta'),
      path('cerrar_sesion', cerrar_sesion, name="cerrar_sesion"),
      path('logear', logear, name="logear"),
      path('editar', editar_Perfil, name="editar"),
      path('editarpass', editar_password, name="editarpass"),
      path('tasks/', views.tasks, name="tasks"),
      path('tasks_completed/', views.tasks_complete, name="tasks_complete"),
      path('create/', views.createTasks, name="create"),
      path('tasks/<alumno:task_id>/', views.taskDetail, name="taskdetail"),
      path('tasks/<alumno:task_id>/complete', views.complete_task, name="complete"),
      path('tasks/<alumno:task_id>/delete', views.delete_task, name="delete"),
]

