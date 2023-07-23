"""HackathonTyl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from atexit import register
from django.contrib import admin
from django.urls import path
from main.views import *
urlpatterns = [
    path('',index,name="index"),
    path('admin/', admin.site.urls),
    path('login',login,name="login"),
    path("register",register,name="register"),
    path("p_home",p_home,name="p_home"),   #patient_home
    path("p_details",p_details,name="p_details"),
    path("book_appointment",book_appointment,name="book_appointment"),
    path("b_appointment",b_appointment,name="b_appointment"),
    path("d_login",d_login,name="d_login"),
    path("d_register",d_register,name="d_register"),
    path("d_home",d_home,name="d_home"),
    path("pres_medicine",pres_medicine,name="pres_medicine"),
    path("p_reports",p_reports,name="p_reports"),
    path("m_order",m_order,name="m_order"),
    path("a_register",a_register,name="a_register"),
    path("a_login",a_login,name="a_login"),
    path("a_home",a_home,name="a_home"),
    path("update_patient",update_patient,name="update_patient"),



]
