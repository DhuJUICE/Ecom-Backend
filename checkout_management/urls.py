from django.urls import path
from . import views
urlpatterns = [
	path('ipn', views.payfast_ipn, name='payfast-ipn'),
]
