from django.shortcuts import render
from models import *

# Create your views here.

def test1(request):
    return test.objects.get(id=1)