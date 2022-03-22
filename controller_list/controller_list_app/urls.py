from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list_control', views.list_control, name='list_control')
]