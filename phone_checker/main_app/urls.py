from django.contrib import admin
from django.urls import path
from .views import * 


urlpatterns = [
    path('', render_index , name = "main_page"),
    path('check_phone/' , check_phone , name = "check_phone")
]
