from .models import *
from rest_framework.serializers import Serializer
from rest_framework import serializers

class TicketsSerializers(serializers.ModelSerializer):


    related_post = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['nmr', 'ticket_type', 'created_at', 'related_post', 'handicap']
        read_only_fields = ['created_at']

    def get_related_post(self, instance):

        return instance.related_post.name if instance.related_post else None
