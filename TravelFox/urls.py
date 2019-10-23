"""TravelFox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from TravelService import views

urlpatterns = [
    path('', views.index),
    path('travel_fox/test_connect/', views.test_connect),

    path('travel_fox/get_plan_list/', views.get_plan_list),
    path('travel_fox/get_plan/', views.get_plan),
    path('travel_fox/add_plan/', views.add_plan),
    path('travel_fox/get_plan_item_list/', views.get_plan_item_list),
    path('travel_fox/add_share/', views.add_share),
    path('travel_fox/del_share/', views.del_share),

    path('travel_fox/get_plan_item/', views.get_plan_item),
    path('travel_fox/add_plan_item/', views.add_plan_item),
    path('travel_fox/move_plan_item/', views.move_plan_item),
    path('travel_fox/modify_plan_item/', views.modify_plan_item),
    path('travel_fox/del_plan_item/', views.del_plan_item),

    path('travel_fox/wx_login/', views.wx_login),
    path('travel_fox/wx_register/', views.wx_register)
]
