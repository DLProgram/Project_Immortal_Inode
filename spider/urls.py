from django.urls import path

from . import views

app_name = 'spider'

urlpatterns = [
    path('', views.index, name='index'),
    path('team/<str:team>', views.search_by_team, name='search_by_team'),
    path('event/<str:event_id>', views.event, name='event'),

]
