from django.urls import path 
from . import views

urlpatterns = [  
    path('user/new/', views.user_new, name='user_new'),
]