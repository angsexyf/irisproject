from django.urls import path
from .views import *

app_name = "home"

urlpatterns = [
    path('', getMainPage, name="home"),
    path('getMainPage', getMainPage, name="getMainPage"),
    path('getRnDPage', getRnDPage, name="getRnDPage"),
    path('submitRequest', submitRequest, name="submitRequest"),
    path('main/', main_page, name="main_page"),
    path('testpage', test_page, name="test_page"),
]
