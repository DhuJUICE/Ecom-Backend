from django.urls import path
from . import views

#token view imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
	path('', views.DisplayPage),

	#Used for custom logging users in - No need for the login endpoint and sends back is_staff attribute for Role Based Access Control
	path('api/token', TokenObtainPairView.as_view(), name='token'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),

	#USER MANAGEMENT API ENDPOINTS
	path('api/register', views.Register.as_view(), name='api-register'),

	#PRODUCT MANAGEMENT API ENDPOINTS - FOR MENU
	path('api/product', views.ProductManagement.as_view(), name='api-product'),
	path('api/product/<int:pk>', views.ProductManagement.as_view(), name='api-product-id'),

	path('api/cart', views.CartManagement.as_view(), name='api-cart'),
	path('api/cart/<int:pk>', views.CartManagement.as_view(), name='api-cart-id'),

	#CHECKOUT MANAGEMENT API ENDPOINTS
	path('api/checkout', views.CheckoutManagement.as_view(), name='api-checkout'),
]
