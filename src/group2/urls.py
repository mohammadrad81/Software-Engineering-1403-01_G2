from django.urls import path
from . import views


app_name = 'group2'
urlpatterns = [
  path('', views.home, name='group2'),
  path('get-sentence/', views.get_sentence, name='get_sentence'),
  path('get-file/', views.get_file, name='get_file'),
] 
