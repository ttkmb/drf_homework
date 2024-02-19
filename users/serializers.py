from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Payments


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone', 'city']

