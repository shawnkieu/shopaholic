from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *

# Create your views here.

def home(request):	
	return render(request, 'home.html')

def register(request):
	if request.method == 'POST':
		username = request.POST.get('logusername')
		password = request.POST.get('logpass')
		email = request.POST.get('logemail')


		if not username:
			messages.success(request, "Username cannot be blank")
		elif not password:
			messages.success(request, "Password cannot be blank")
		elif not email:
			messages.success(request, "Email cannot be blank")
		elif User.objects.filter(username=username).exists():
			messages.success(request, "Username is already taken")
		elif User.objects.filter(email=email).exists():
			messages.success(request, "Username is already taken")
		else:
			user = User.objects.create_user(username=username,password=password,email=email)
			messages.success(request, "User is successfully created")
			return redirect('dashboard')

	return render(request,'login.html')

def signin(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		if not username:
			messages.success(request, "Username cannot be blank")
		elif not password:
			messages.success(request, "Password cannot be blank")
		else:
			user=authenticate(request, username=username,password=password)
			if user is not None:
				login(request,user)
				messages.success(request,"Successfully logged in")
				return redirect('dashboard')
			else:
				messages.success(request,"Invalid username or password")
				return render(request,'login.html')

	return render(request,'login.html')

def logout_user(request):
	logout(request)
	messages.success(request,"Successfully logged out")
	return redirect('login')

def dashboard(request):
	customers = Customer.objects.all()
	orders = Order.objects.all()

	all_order = Order.objects.count()
	order_delivered = Order.objects.filter(status='Delivered').count()
	order_pending = Order.objects.filter(status='Pending').count()
	order_fullfill = round((order_delivered/all_order)*100,2)
	context = {
		'all_order': all_order,
		'order_delivered': order_delivered,
		'order_pending':order_pending,
		'order_fullfill':order_fullfill,
		'customers': customers,
		'orders': orders,
	}
	return render(request, 'dashboard.html',context)
	