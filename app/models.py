from django.db import models


class test(models.Model):
    
    text=models.TextField(max_length=20)

