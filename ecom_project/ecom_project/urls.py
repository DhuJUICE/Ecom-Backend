"""
URL configuration for ecom_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

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
    path('admin/', admin.site.urls),
    path('', include('api_management.urls')),
    path('', include('browse_management.urls')),
    path('', include('cart_management.urls')),
    path('', include('checkout_management.urls')),
    path('', include('product_management.urls')),
    path('', include('user_management.urls')),
    path('', include('contact_us.urls')),

    # Swagger UI endpoint for API documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
