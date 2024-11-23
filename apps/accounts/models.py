from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class Account(AbstractUser):
    CLIENT = "client"
    EMPLOYEE = "employee"
    FACTEUR = 'facteur'

    ACCOUNT_TYPE = [
        (CLIENT, "Client"),
        (EMPLOYEE, "Employee"),
        (FACTEUR,"Facteur"),
    ]

    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)

    email = models.EmailField(unique=True, blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)
    reset_code = models.IntegerField(null=True, blank=True)

  

    def __str__(self):
        return f"{self.username or self.email} ({self.account_type})"

    class Meta:
        ordering = ['account_type']
        indexes = [
            models.Index(fields=['id', 'account_type']),
        ]