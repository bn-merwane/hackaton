from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
   path('tickets/',HomePage.as_view()),
   path('Reserve/',Reserve.as_view()),
   path('TicketAdmin/',CurrentTicketAdmin.as_view())

]
