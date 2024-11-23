from django.contrib import admin
from .models import Ticket,TicketsTrash

admin.site.register(Ticket)
admin.site.register(TicketsTrash)
