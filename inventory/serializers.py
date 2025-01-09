from rest_framework import serializers
from .models import Inventory, InventoryChange, Category
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class InventoryItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Inventory
        fields = ['id', 'name', 'description', 'quantity', 'price', 'category', 'date_added', 'last_updated', 'user']


class InventoryChangeSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()  
    user = serializers.StringRelatedField()
    class Meta:
        model = InventoryChange
        fields = ['id', 'inventory_item', 'quantity_changed', 'date_changed', 'changed_by']
        fields = ['id', 'item', 'user', 'change_type', 'quantity_change', 'created_at']