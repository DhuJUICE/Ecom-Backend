import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_management.serializers import UserSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import UserProfile

def register_view(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			
			first_name = data.get('first_name')
			last_name = data.get('last_name')
			email = data.get('email')
			password = data.get('password')
			confirm_password = data.get('confirm_password')
			username = email
			
			# Optional business owner request flag
			request_business_owner = data.get('request_business_owner', False)
			
			if User.objects.filter(email=email).exists():
				return JsonResponse({"message": "Email already exists.", "status": "error"}, status=400)

			if password != confirm_password:
				return JsonResponse({"message": "Passwords do not match.", "status": "error"}, status=400)

			new_user = User.objects.create_user(
				first_name=first_name,
				last_name=last_name,
				username=username,
				email=email,
				password=password
			)
			
			# Create associated UserProfile manually with custom role request info
			role = 'openUser'  # default
			business_owner_request = bool(request_business_owner)

			new_user.userprofile.role = role
			new_user.userprofile.business_owner_request = business_owner_request
			new_user.userprofile.save()

			return JsonResponse({"message": "User registered successfully!", "status": "success"}, status=201)

		except json.JSONDecodeError:
			return JsonResponse({"message": "Invalid JSON format.", "status": "error"}, status=400)

	return JsonResponse({"message": "Invalid request method. POST required.", "status": "error"}, status=405)