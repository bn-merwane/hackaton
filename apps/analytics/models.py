from django.db import models
from apps.accounts.models import Account

class Employee_data(models.Model):
    employee = models.ForeignKey(Account, on_delete=models.CASCADE)
    TodayNmbrTiquets = models.PositiveIntegerField(default=0)
    todayLogin = models.DateTimeField()
    todaylogout  = models.DateTimeField()