from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions, generics 
from .models import Inventory, InventoryChange, Category
from .serializers import InventoryItemSerializer, InventoryChangeSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

class InventoryChangeHistoryView(generics.ListAPIView):
    serializer_class = InventoryChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        item_id = self.request.query_params.get('item_id', None)
        if item_id:
            return InventoryChange.objects.filter(item__id=item_id).order_by('-created_at')
        return InventoryChange.objects.all().order_by('-created_at')


class InventoryItemPagination(PageNumberPagination):
    page_size = 10


class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = InventoryItemPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        item = serializer.save(owner=self.request.user)
        InventoryChange.objects.create(
            item=item,
            user=self.request.user,
            change_type='restock',
            quantity_change=item.quantity
        )   
    def get_queryset(self):
        return InventoryItem.objects.filter(user=self.request.user)     
    def perform_update(self, serializer):
        item = serializer.save()

        
        old_quantity = InventoryItem.objects.get(id=item.id).quantity
        quantity_change = item.quantity - old_quantity

        if quantity_change != 0:
            
            change_type = 'restock' if quantity_change > 0 else 'sell'
            InventoryChange.objects.create(
                item=item,
                user=self.request.user,
                change_type=change_type,
                quantity_change=quantity_change
            ) 
    def view_inventory_levels(self, request):
        """Custom endpoint to view inventory levels with optional filters."""
        category = request.query_params.get('category', None)
        price_min = request.query_params.get('price_min', None)
        price_max = request.query_params.get('price_max', None)
        low_stock = request.query_params.get('low_stock', None)

        queryset = self.get_queryset()
        
        # Apply category filter
        if category:
            queryset = queryset.filter(category=category)

        # Apply price range filter
        if price_min and price_max:
            queryset = queryset.filter(price__gte=price_min, price__lte=price_max)

        # Apply low stock filter (e.g., items with quantity below 5)
        if low_stock:
            queryset = queryset.filter(quantity__lt=5)

        # Return the filtered inventory data
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='inventory-changes')
    def track_inventory_changes(self, request, pk=None):
        """Custom endpoint to view inventory changes history for an item."""
        item = self.get_object()
        changes = item.inventorychange_set.all()  # Assuming an InventoryChange model exists to track updates
        # Assuming InventoryChange has a serializer
        from .serializers import InventoryChangeSerializer
        serializer = InventoryChangeSerializer(changes, many=True)
        return Response(serializer.data)           


    @action(detail=True, methods=['get'])
    def inventory_changes(self, request, pk=None):
        item = self.get_object()
        changes = InventoryChange.objects.filter(inventory_item=item)
        page = self.paginate_queryset(changes)
        if page is not None:
            serializer = InventoryChangeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = InventoryChangeSerializer(changes, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class InventoryChangeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryChange.objects.all()
    serializer_class = InventoryChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

class InventoryLevelView(generics.ListAPIView):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = InventoryItem.objects.all()

        
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__name=category)

        
        price_min = self.request.query_params.get('price_min', None)
        price_max = self.request.query_params.get('price_max', None)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        
        low_stock = self.request.query_params.get('low_stock', None)
        if low_stock:
            low_stock_threshold = int(low_stock)
            queryset = queryset.filter(quantity__lt=low_stock_threshold)

        return queryset
