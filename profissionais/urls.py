from django.urls import path

from profissionais import views

urlpatterns = [
    path('create/', views.add_profissional, name='add_profissional'),
    path('all/', views.get_all_profissionais, name='get_all_profissionais'),
    path('update/<int:pk>/', views.update_profissional, name='update_profissional'),
    path('profissional/<int:pk>/delete/', views.delete_profissional, name='delete_profissional'),
]