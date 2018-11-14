from django.urls import path 
from . import views

urlpatterns = [   
    path('user/register/', views.register, name='register'),
]