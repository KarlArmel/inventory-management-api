from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, InventoryChangeViewSet, CategoryViewSet, InventoryLevelView, InventoryChangeHistoryView, LoginView, LogoutView
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views


router = DefaultRouter()

router.register(r'inventory-Items', InventoryItemViewSet, basename='inventory')
router.register(r'inventory-changes', InventoryChangeViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include('inventory.urls')),
    path('api/inventory_levels/', InventoryLevelView.as_view(), name='inventory-levels'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

]