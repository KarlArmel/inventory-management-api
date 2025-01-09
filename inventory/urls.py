from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, InventoryChangeViewSet, CategoryViewSet, InventoryLevelView, InventoryChangeHistoryView
from django.urls import path, include


router = DefaultRouter()

router.register(r'inventory-items', InventoryItemViewSet)
router.register(r'inventory-changes', InventoryChangeViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns = router.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('inventory.urls')),
    path('api/inventory_levels/', InventoryLevelView.as_view(), name='inventory-levels'),

]