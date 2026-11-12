from django.urls import path

from consultas import views

urlpatterns = [
    path('create/', views.add_consulta, name='add_consulta'),
    path('all/', views.get_all_consultas, name='get_all_consultas'),
    path('update/<int:pk>/', views.update_consulta, name='update_consulta'),
    path('consulta/<int:pk>/delete/', views.delete_consulta, name='delete_consulta'),
]