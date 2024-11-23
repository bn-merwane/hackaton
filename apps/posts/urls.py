
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
  path('Reserve/', Reserve.as_view()),
  path('AdminSettings/',SettingsPost.as_view())

]