"""automate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from .views import test, login, auth, upload_api, save_file, get_api_json, get_specific_api_json, tabletemplate

urlpatterns = [

# path('login/',  view =login, name='login'), # replace with empty
path('auth',  view =auth, name='auth'),
# path('',  view =test, name='home'),
path('',  view =login, name='home'),
path('edit/<str:tname>',  view =test, name='home'),
path('upload-api',  view =upload_api, name='uploadapi'),
path('save-file',  view =save_file, name='uploadapi'),
path('get-api-json',  view = get_api_json, name='uploadapi'),

path('get-spec-json/<str:genre>',  view = get_specific_api_json, name='uploadapi'),
path('tabletemplate/',  view = tabletemplate, name='uploadapi')

]