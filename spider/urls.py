from django.urls import path

from . import views

app_name = 'spider'

urlpatterns = [
    path('', views.index, name='index'),
    path('event/<str:event_id>', views.event, name='event'),
    path('add_to_db/<str:event_id>', views.add_to_db, name='add_to_db'),
]
