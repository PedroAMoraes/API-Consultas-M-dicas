from django.urls import path

from profissionais import views

urlpatterns = [
    path('create/', views.add_profissional, name='add_profissional'),
    path('all/', views.get_all_profissionais, name='get_all_profissionais'),
    path('<int:pk>/update/', views.update_profissional, name='update_profissional'),
    path('<int:pk>/delete/', views.delete_profissional, name='delete_profissional'),
]