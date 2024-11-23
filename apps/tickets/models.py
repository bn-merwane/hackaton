from django.db import models
from apps.accounts.models import Account
from apps.posts.models import Post




class Ticket(models.Model):
    RETRAIT_DEPOT = 'Retrait ou dépôt argent'
    PAIEMENT_FACTURES = 'Paiement de factures'
    SERVICES_COURRIERS = 'Services d’envoi ou de réception de courriers/colis'
    
    TICKET_TYPE_CHOICES = [
        (RETRAIT_DEPOT, 'Retrait ou dépôt argent'),
        (PAIEMENT_FACTURES, 'Paiement de factures'),
        (SERVICES_COURRIERS, 'Services d’envoi ou de réception de courriers/colis'),
    ]

    nmr = models.PositiveIntegerField(unique=True)
    owner = models.OneToOneField(Account, on_delete=models.CASCADE)
    handicap = models.BooleanField(default=False)
    ticket_type = models.CharField(max_length=502, choices=TICKET_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    related_post = models.ForeignKey(Post,on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ['nmr']  

    def __str__(self):
        return f"Ticket #{self.nmr} - {self.get_ticket_type_display()}"
    



class TicketsTrash(models.Model):
    RETRAIT_DEPOT = 'Retrait ou dépôt argent'
    PAIEMENT_FACTURES = 'Paiement de factures'
    SERVICES_COURRIERS = 'Services d’envoi ou de réception de courriers/colis'
    
    TICKET_TYPE_CHOICES = [
        (RETRAIT_DEPOT, 'Retrait ou dépôt argent'),
        (PAIEMENT_FACTURES, 'Paiement de factures'),
        (SERVICES_COURRIERS, 'Services d’envoi ou de réception de courriers/colis'),
    ]

    nmr = models.PositiveIntegerField()
    owner = models.ManyToManyField(Account)
    handicap = models.BooleanField(default=False)
    ticket_type = models.CharField(max_length=502, choices=TICKET_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    related_post = models.ForeignKey(Post,on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ['nmr']  

    def __str__(self):
        return f"Ticket #{self.nmr} - {self.get_ticket_type_display()}"



