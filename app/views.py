# views.py
from django.http import JsonResponse
from .models import Text

def test1(request):
    # Assuming you want to return a specific Text object
    text_object = Text.objects.get(id=1)  # Fetch the Text object with ID 1
    return JsonResponse({'content': text_object.text})
