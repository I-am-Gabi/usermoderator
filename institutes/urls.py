from django.urls import path 
from . import views

urlpatterns = [  
    path('institute/new/', views.institute_new, name='institute_new'),
]