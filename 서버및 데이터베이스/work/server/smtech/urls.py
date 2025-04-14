from django.urls import path
from .views import *

app_name = "smtech"

urlpatterns = [
    path('getRnDPage', getRnDPage, name="getRnDPage"),
    path('openPage', open_page, name="open_page"),
]

