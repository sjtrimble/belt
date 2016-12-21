from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from datetime import datetime
import re
import bcrypt

class UserManager(models.Manager):
	# Checking first that fields are all populated:
	def loginvalidation(self, formdata):
		errormessage = []
		validlogin = (False, "")
		error = False

		if len(formdata['username']) < 1:
				error = True
				errormessage.append("Please complete username field.")
		if len(formdata['password']) < 1:
			error = True
			errormessage.append("Please complete password field.")

		if error:
			validlogin = (False, errormessage)
			return validlogin

		else:
			if len(formdata['username']) < 3:
				error = True
				errormessage.append("Please enter a valid username.")
			# Check that password is of proper length:
			if len(formdata['password']) < 8:
				error = True
				errormessage.append("Please enter a password of at least 8 characters.")

		if error:
			validlogin = (False, errormessage)
			return validlogin

		else:
			# <--------- Handles login logic that allows or deny access: -------->
			# Check if a filter on the user provided username returns a result:
			if len(User.objects.filter(username=formdata['username'])) > 0:
				# Check that the passwords match using bcrypt
				thisuser = User.objects.filter(username=formdata['username'])[0]
				hashed = User.objects.filter(username= formdata['username'])[0].encrypted_password
				hashed = hashed.encode()
				password = formdata['password']
				password = password.encode()
				if bcrypt.hashpw(password, hashed) == hashed:
					validlogin = (True, thisuser)
				else:
	 				errormessage.append("Invalid username or password.")
	 				validlogin = (False, errormessage)
			else:
				errormessage.append("Invalid username or password.")
				validlogin = (False, errormessage)
			return validlogin

	def registrationvalidation(self, formdata):
		errormessage = []
		validregistration = (False, "")
		error = False
		if len(formdata['username']) < 1:
			error = True
			errormessage.append("Please complete username field.")
		if len(formdata['password']) < 1:
			error = True
			errormessage.append("Please complete password field.")
		if len(formdata['name']) < 1:
			error = True
			errormessage.append("Please complete name field.")
		if len(formdata['confirm_password']) < 1:
			error = True
			errormessage.append("Please confirm password.")

		if error:
			validregistration = (False, errormessage)
			return validregistration

		else:
			if len(formdata['username']) < 3:
				error = True
				errormessage.append("Please enter a valid username address.")
			# Check that password is of proper length:
			if len(formdata['password']) < 8:
				error = True
				errormessage.append("Please enter a password of at least 8 characters.")
			# Check that username is not already in use (returns a filter result):
			if len(User.objects.filter(username=formdata['username'])) > 0:
				error = True
				errormessage.append("That username has already been registered. Please use a different username address.")
			# Check that first name is of proper length:
			if len(formdata['name']) < 2:
				error = True
				errormessage.append("Please enter a first name of at least 2 characters long.")
			if formdata['password'] != formdata['confirm_password']:
				error = True
				errormessage.append("Passwords do not match.")

			# Check for format
			if error:
				validregistration = (False, errormessage)
				return validregistration

			else:
			# Creates a new User object:
			# Setting a variable to easily call it below in the bcrypt method:
				password = formdata['password'].encode()
				thisuser = User.objects.create(name=formdata['name'], username=formdata['username'], encrypted_password=bcrypt.hashpw(password, bcrypt.gensalt()))
				validregistration = (True, thisuser)
			return validregistration

class TripManager(models.Manager):
	def tripvalidation(self, formdata, user):
		errormessage = []
		validtrip = (False, "")
		error = False
		today = datetime.now().date()

		if len(formdata['destination']) < 1:
			error = True
			errormessage.append("Please complete destination field.")
		if len(formdata['description']) < 1:
			error = True
			errormessage.append("Please complete description field.")

		if error:
			validtrip = (False, errormessage)
			return validtrip

		else:

			if str(formdata['start_date']) < str(today) or str(formdata['end_date']) < str(today):
				error = True
				errormessage.append("Please enter a future trip date.")

			if str(formdata['end_date'])[0:4] < str(formdata['start_date'])[0:4]:
				error = True
				errormessage.append("Please enter an end date after the start date.")

			if error:
				validtrip = (False, errormessage)
				return validtrip

			else:
				newtrip = Trip.objects.create(destination=formdata['destination'], description=formdata['description'], start_date=formdata['start_date'], end_date=formdata['end_date'], user=user)
				validtrip = (True, newtrip)
				return validtrip

	def jointrip(self, trip, user):
		trip.attendee.add(user)
		return True

# User DB Table Goes Here
class User(models.Model):
	name = models.CharField(max_length=50)
	username = models.CharField(max_length=50)
	encrypted_password = models.CharField(max_length=250)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Trip(models.Model):
	destination = models.CharField(max_length=50)
	description = models.CharField(max_length=50)
	user = models.ForeignKey('User', related_name='planner')
	start_date = models.DateField()
	end_date = models.DateField()
	attendee = models.ManyToManyField('User')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = TripManager()
