from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = '__all__'  # This will include all fields in the model
