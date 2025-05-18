from django.urls import path
from .views import run_code , home

urlpatterns = [
    path('run/', run_code),
    path('' ,home)
]