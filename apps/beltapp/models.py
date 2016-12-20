from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from datetime import datetime
import re
import bcrypt

# Setting REGEX format for email to reference in logic below
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def loginvalidation(self, formdata):
	# Checking first that fields are all populated:
		errormessage = []
		validlogin = (False, "")
		error = False

		if len(formdata['email']) < 1:
				error = True
				errormessage.append("Please complete email field.")
		if len(formdata['password']) < 1:
			error = True
			errormessage.append("Please complete password field.")

		if error:
			validlogin = (False, errormessage)
			return validlogin

		else:
			if not EMAIL_REGEX.match(formdata['email']):
				error = True
				errormessage.append("Please enter a valid email address.")
			# Check that password is of proper length:
			if len(formdata['password']) < 8:
				error = True
				errormessage.append("Please enter a password of at least 8 characters.")

		if error:
			validlogin = (False, errormessage)
			return validlogin

		else:
			# <--------- Handles login logic that allows or deny access: -------->
			# Check if a filter on the user provided email returns a result:
			if len(User.objects.filter(email=formdata['email'])) > 0:
				# Check that the passwords match using bcrypt
				thisuser = User.objects.filter(email=formdata['email'])[0]
				hashed = User.objects.filter(email= formdata['email'])[0].encrypted_password
				hashed = hashed.encode()
				password = formdata['password']
				password = password.encode()
				if bcrypt.hashpw(password, hashed) == hashed:
					validlogin = (True, thisuser)
				else:
	 				errormessage.append("Invalid email or password.")
	 				validlogin = (False, errormessage)
			else:
				errormessage.append("Invalid email or password.")
				validlogin = (False, errormessage)
			return validlogin

	def registrationvalidation(self, formdata):
		errormessage = []
		validregistration = (False, "")
		error = False
		if len(formdata['email']) < 1:
			error = True
			errormessage.append("Please complete email field.")
		if len(formdata['password']) < 1:
			error = True
			errormessage.append("Please complete password field.")
		if len(formdata['name']) < 1:
			error = True
			errormessage.append("Please complete name field.")
		if len(formdata['alias']) < 1:
			error = True
			errormessage.append("Please complete alias field.")
		if len(formdata['confirm_password']) < 1:
			error = True
			errormessage.append("Please confirm password.")
		if len(str(formdata['birthday'])) < 1:
			error = True
			errormessage.append("Please enter your birthday.")

		if error:
			validregistration = (False, errormessage)
			return validregistration

		else:
			if not EMAIL_REGEX.match(formdata['email']):
				error = True
				errormessage.append("Please enter a valid email address.")
			print validregistration, error, "validemail"
			# Check that password is of proper length:
			if len(formdata['password']) < 8:
				error = True
				errormessage.append("Please enter a password of at least 8 characters.")
			print validregistration, error, "pwlen"
			# Check that email is not already in use (returns a filter result):
			if len(User.objects.filter(email=formdata['email'])) > 0:
				error = True
				print "It thinks this email is already in the system"
				errormessage.append("That email has already been registered. Please use a different email address.")
			print validregistration, error, "emailinsystem"
			# Check that first name is of proper length:
			if len(formdata['name']) < 2:
				error = True
				errormessage.append("Please enter a first name of at least 2 characters long.")
			print validregistration, error, "firstname"
			# Check that last name is of proper length:
			if len(formdata['alias']) < 2:
				error = True
				errormessage.append("Please enter a last name of at least 2 characters long.")
			print validregistration, error, "lastname"
			if formdata['password'] != formdata['confirm_password']:
				error = True
				errormessage.append("Passwords do not match.")
			print validregistration, error, "pw confirm"
			if str(formdata['birthday'])[0:4] > str(datetime.today().year):
				error = True
				errormessage.append("Please enter a valid birthday.")
			print validregistration, error, "birthday valid"

			# Check for format
			if error:
				validregistration = (False, errormessage)
				return validregistration

			else:
				print "now trying to create a user object"
			# Creates a new User object:
			# Setting a variable to easily call it below in the bcrypt method:
				password = formdata['password'].encode()
				thisuser = User.objects.create(name=formdata['name'], alias=formdata['alias'], email=formdata['email'], encrypted_password=bcrypt.hashpw(password, bcrypt.gensalt()), birthday=formdata['birthday'])
				print "object successfully created"
				validregistration = (True, thisuser)
			return validregistration

# User DB Table Goes Here
class User(models.Model):
	name = models.CharField(max_length=50)
	alias = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	encrypted_password = models.CharField(max_length=250)
	birthday = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()