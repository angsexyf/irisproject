from django.urls import path
from .views import *

app_name = "rcms"

urlpatterns = [
    path('getRnDPage', getRnDPage, name="getRnDPage"),
    path('openPage', open_page, name="open_page"),
    path('main/', main_page, name="main_page"),
    path('index', iframe_page, name="iframe_page"),
]

