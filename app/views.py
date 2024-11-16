from django.shortcuts import render
from app.models import *

# Create your views here.

def test1(request):
    return test.objects.get(id=1)