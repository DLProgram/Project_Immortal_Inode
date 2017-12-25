from django.urls import path

from . import views

app_name = 'scout_leader'

urlpatterns = [
    path('', views.index, name='index'),
]
