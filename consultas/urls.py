from django.urls import path

from consultas import views

urlpatterns = [
    path('create/', views.add_consulta, name='add_consulta'),
    path('all/', views.ConsultaslListView.as_view(), name='get_all_consultas'),
    path('<int:pk>/', views.get_consulta, name='get_consulta'),
    path('<int:pk>/update/', views.update_consulta, name='update_consulta'),
    path('<int:pk>/delete/', views.delete_consulta, name='delete_consulta'),
]