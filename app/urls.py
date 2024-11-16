from django.contrib import admin
from django.urls import path, include
from app.views import test1

urlpatterns = [
    path('test/', test1),  # Corrected this line by removing the extra parentheses
]
