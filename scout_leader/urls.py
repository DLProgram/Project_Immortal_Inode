from django.urls import path

from . import views

app_name = 'scout_leader'

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('<int:match_num>/', views.scout, name='scout'),
    path('save_data/', views.save_data, name='save_data'),
]
