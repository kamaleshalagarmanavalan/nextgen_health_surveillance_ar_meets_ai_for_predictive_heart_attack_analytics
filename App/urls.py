"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import home,index, RegisterView,logout_view
from .import views

urlpatterns = [
    path('home/', home, name='users-home'),
    path('profile/', views.home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile1/', views.profile, name='users-profile'),
   
    path('database/',views.database,name='database'),
    path('matrix/',views.matrix,name='matrix'),
    path('patient_list/', views.patient_list, name='patient_list'),
    path('report/', views.report, name='report'),
    path('', views.Deploy_9, name='Deploy_9'),
    # path('Deploy_10/', views.Deploy_10, name='Deploy_10'),
    path('request/', views.request, name='request'),
    path('logout_view/',logout_view,name='logout_view'),
]
