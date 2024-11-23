from rest_framework import serializers
from .models import Account
from django.contrib.auth.hashers import make_password

class SignupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["password", "email", "first_name"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        
        return Account.objects.create(**validated_data,account_type="Client")
    

class LoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required = False)
    class Meta:
        model = Account
        fields = ["password" , "email", "username"]

