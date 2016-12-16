from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
# Create your models here.
class UserManager(models.Manager):
	def register(self, postData):
		errors = []
		email_taken = User.objects.filter(email = postData['email'])
		if email_taken:
			errors.append("Email is already in use. Please sign in or use a different email address")
		if len(postData['email']) < 1:
			errors.append('Email cannot be blank')
		elif not re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', postData['email']):
			errors.append('email invalid')
		if len(postData['password']) < 1: 
			errors.append('Password cannot be empty')
		if not re.match(r'^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d)).{8,32}$', postData['password']):
			errors.append('Password must be at least 8 characters, have atleast one capital letter, one number, and one special character')
		elif postData['confirm_password'] != postData['password']:
			errors.append('The passwords you entered do not match')
		if len(postData['first_name']) < 1:
			errors.append('First Name cannot be blank')
		if len(postData['last_name']) < 1:
			errors.append('Last Name cannot be blank')
		if not re.match(r'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$', postData['birthday']):
			errors.append('Birthdate field if not valid. please use format DD/MM/YYYY')
		if errors == []:
			encrypt_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
			User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = encrypt_pw, birthday = birthday)
			user_valid = User.objects.get(email = postData['email'])
			return ["valid", user_valid]
		else: 
			return ["invalid", errors]

	def login(self, postData):
		errors = []
		if len(postData['email']) < 1:
			errors.append('Email cannot be blank')
		if not re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', postData['email']):
			errors.append('email invalid')
		valid_email = User.objects.filter(email = postData['email'])
		if not valid_email:
			errors.append('This email does not exist in our system. Please register a new account!')
		if len(postData['password']) < 1: 
			errors.append('Password cannot be empty')
		if errors == []:
			user = User.objects.get(email = postData['email'])
			hashed = user.password
			if bcrypt.hashpw(postData['password'].encode(), hashed.encode()) == hashed:
				return ["valid", user]
			else: 
				errors.append('Invalid Password, please try again!')
				return ["invalid", errors]
		else:
			return ["invalid", errors]

class QuoteManager(models.Manager):
	def add_quote(self, postData, id):
		errors = []
		if len(postData['author']) < 3:
			errors.append('Quoted By field must contain at least 3 characters.')
		if len(postData['quote']) < 10:
			errors.append('Message field must contain at least 10 characters.')
		if errors == []:
			user = User.objects.get(id = id)
			quote = Quote.objects.create(quote = postData['quote'], author = postData['author'], user = user)
			Favorite.objects.create(user = user, quote = quote)
			return ["valid", user]
		else:
			return ["invalid", errors]

	def remove_favorite(self, user_id, quote_id):
		find_user = User.objects.get(id = user_id)
		find_quote = Quote.objects.get(id = quote_id)
		remove_favorite = Favorite.objects.get(user = find_user, quote = find_quote).delete()
		return True

	def add_favorite(self, user_id, quote_id):
		errors = []
		find_user = User.objects.get(id = user_id)
		find_quote = Quote.objects.get(id = quote_id)
		favorite_exists = Favorite.objects.filter(user = find_user, quote = find_quote)
		if not favorite_exists:
			add_favorite = Favorite.objects.create(user = find_user, quote = find_quote)
			return ["valid", find_user]
		else: 
			errors.append('You have already Favorited this Quote!')
			return["invalid", errors]


class User(models.Model):
	first_name = models.CharField(max_length = 100)
	last_name = models.CharField(max_length = 100)
	email = models.CharField(max_length = 100)
	password = models.CharField(max_length = 250)
	birthday = models.CharField(max_length = 10)
	created_on = models.DateTimeField(auto_now_add = True)
	objects = UserManager()

class Quote(models.Model):
	quote = models.CharField(max_length = 100)
	author = models.CharField(max_length = 100)
	user = models.ForeignKey(User)
	created_on = models.DateTimeField(auto_now_add = True)
	objects = QuoteManager()


class Favorite(models.Model):
	user = models.ForeignKey(User)
	quote = models.ForeignKey(Quote)


