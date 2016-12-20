from django.shortcuts import render, redirect
from models import User ############################### add other classes
import bcrypt
from django.contrib import messages, sessions
from django.db.models import Count
from datetime import datetime

def index(request):
	if 'userid' not in request.session:
		return render(request, 'beltapp/index.html')
	return render(request, 'beltapp/index.html')
	# else:
	# 	return redirect('/') #change homepage

def registration(request):
	data = User.objects.registrationvalidation(request.POST)
	if data[0]:
		messages.success(request, "You have successfully logged in!")
		user = data[1]
		request.session['userid'] = user.id
		return redirect('/') #change home page
	else:
		errors = User.objects.registrationvalidation(request.POST)[1]
		for error in errors:
			messages.error(request, error)
		return redirect('/')

def login(request):
	if User.objects.loginvalidation(request.POST)[0]:
		messages.success(request, "You have successfully logged in!")
		user = User.objects.loginvalidation(request.POST)[1]
		print user
		request.session['userid'] = user.id
		print user.id
		return redirect('/')
	else:
		errors = User.objects.loginvalidation(request.POST)[1]
		for error in errors:
			messages.error(request, error)
	return redirect('/')
