from django.urls import path
from . import views

app_name = 'group10'
urlpatterns = [
  path('', views.home, name='group10')

] 