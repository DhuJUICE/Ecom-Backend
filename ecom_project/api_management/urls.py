from django.urls import path
from . import views

#token view imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
	path('api/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
	
	path('api', views.DisplayPage),

	#Used for logging users in - No need for the login endpoint
	path('api/token', TokenObtainPairView.as_view(), name='token'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),

	#USER MANAGEMENT API ENDPOINTS
	path('api/register', views.Register.as_view(), name='api-register'),
	#path('api/login', views.Login.as_view(), name='api-login'),
	path('api/logout', views.Logout.as_view(), name='api-logout'),

	#PRODUCT MANAGEMENT API ENDPOINTS
	path('api/product', views.ProductManagement.as_view(), name='api-product'),
	path('api/product/<int:pk>', views.ProductManagement.as_view(), name='api-product-id'),

	#CART MANAGEMENT API ENDPOINTS
	path('api/cart', views.CartManagement.as_view(), name='api-cart'),
	path('api/cart/<int:pk>', views.CartManagement.as_view(), name='api-cart-id'),
    
	#ADD PRODUCT TO CART FUNCTIONALITY
	path('api/cart/add', views.AddToCart.as_view(), name='api-cart-add'),

	#REMOVE PRODUCT FROM CART FUNCTIONALITY
	path('api/cart/remove', views.CartRemoveProduct.as_view(), name='api-cart-remove'),

	#INCREMENT PRODUCT QUANTITY IN USERS CART FUNCTIONALITY
	path('api/cart/increment', views.CartIncrementProduct.as_view(), name='api-cart-increment-product'),

	#DECREMENT PRODUCT QUANTITY IN USERS CART FUNCTIONALITY
	path('api/cart/decrement', views.CartDecrementProduct.as_view(), name='api-cart-decrement-product'),

	#TRANSACTION MANAGEMENT API ENDPOINTS
	path('api/transaction', views.TransactionManagement.as_view(), name='api-transaction'),
	path('api/transaction/<int:pk>', views.TransactionManagement.as_view(), name='api-transaction-id'),

	#CHECKOUT MANAGEMENT API ENDPOINTS
	path('api/checkout', views.CheckoutManagement.as_view(), name='api-checkout'),
	
]
