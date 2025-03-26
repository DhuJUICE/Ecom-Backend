from django.urls import path
from . import views

#token view imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

#swagger imports to use swagger documentation for restApi
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

#getting the swagger documentation schema set up to be used
# Define your schema view for Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Yummy Tummies API",
        default_version='v1',
        description="API documentation for Yummy Tummies Backend",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yummytummies.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
	#swagger documentation for api endpoint
	# Swagger UI endpoint for API documentation
    path('/swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

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
    path('api/cart/<int:user_id>', views.CartManagement.as_view(), name='api-cart-id'),
    
	#ADD TO CART FUNCTIONALITY
	path('api/cart/add', views.AddToCart.as_view(), name='api-cart-add'),

	#TRANSACTION MANAGEMENT API ENDPOINTS
	path('api/transaction', views.TransactionManagement.as_view(), name='api-transaction'),
	path('api/transaction/<int:pk>', views.TransactionManagement.as_view(), name='api-transaction-id'),

	#CHECKOUT MANAGEMENT API ENDPOINTS
	path('api/checkout', views.CheckoutManagement.as_view(), name='api-checkout'),
	
]
