from rest_framework import serializers
from .models import (
    Manager,
    Document,
    Order,
    OrderItem
)

class ManagerDetailSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source = 'app_user.email')
    class Meta:
        model = Manager
        fields = (
            'id',
            'company_name',
            'email',
            'phone_number',
        )