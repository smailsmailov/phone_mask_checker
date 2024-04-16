from django.contrib import admin
from django.urls import path , include
from main_app import urls as main_app_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path( '' , include(main_app_urls.urlpatterns)),
]
