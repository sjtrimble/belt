from django.shortcuts import render, redirect
from models import User, Trip
import bcrypt
from django.contrib import messages, sessions
from django.db.models import Count
from datetime import datetime

def index(request):
	if 'userid' not in request.session:
		return render(request, 'beltapp/index.html')
	return redirect('/travels')
	# else:
	# 	return redirect('/') #change homepage

def travels(request):
	userid = request.session['userid']
	user = User.objects.filter(id=userid)[0]
	planner = user
	context = {
	"user": user,
	"othertrips": Trip.objects.exclude(attendee__id=userid).exclude(user=user),
	"mytrips": Trip.objects.filter(user=user) | Trip.objects.filter(attendee__id=userid)
	}
	return render(request, 'beltapp/dashboard.html', context)

def addtrip(request):
	return render(request, 'beltapp/addtrip.html')

def processnewtrip(request):
	userid = request.session['userid']
	user = User.objects.filter(id=userid)[0]
	if Trip.objects.tripvalidation(request.POST, user)[0]:
		return redirect('/travels')
	else:
		errors = Trip.objects.tripvalidation(request.POST, user)[1]
		for error in errors:
			messages.error(request, error)
		return redirect('/travels/add')

def join(request):
	userid=request.session['userid']
	user = User.objects.filter(id=userid)[0]
	trip = Trip.objects.filter(id=request.POST['tripid'])[0]
	Trip.objects.jointrip(trip, user)
	return redirect('/travels')

def destination(request, id):
	trip = Trip.objects.filter(id=id)[0]
	userid = request.session['userid']
	user = User.objects.filter(id=userid)[0]
	context = {
	"trip": trip,
	"joiners": trip.attendee.all(),
	}
	return render(request, 'beltapp/destination.html', context)

def registration(request):
	data = User.objects.registrationvalidation(request.POST)
	if data[0]:
		messages.success(request, "You have successfully logged in!")
		user = data[1]
		request.session['userid'] = user.id
		return redirect('/travels')
	else:
		errors = User.objects.registrationvalidation(request.POST)[1]
		for error in errors:
			messages.error(request, error)
		return redirect('/')

def login(request):
	if User.objects.loginvalidation(request.POST)[0]:
		messages.success(request, "You have successfully logged in!")
		user = User.objects.loginvalidation(request.POST)[1]
		request.session['userid'] = user.id
		return redirect('/travels')
	else:
		errors = User.objects.loginvalidation(request.POST)[1]
		for error in errors:
			messages.error(request, error)
	return redirect('/')

def logout(request):
	for key in request.session.keys():
		del request.session[key]
		messages.success(request, "You have successfully logged out!")
	return redirect('/')
