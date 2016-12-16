from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages, sessions
from .models import User, Quote, Favorite

# Create your views here.
def index(request):
	if "id" not in request.session:
		request.session['id'] = ''
	return render(request, 'belt_app/index.html')

def register(request):
	if request.method == "POST":
		valid_fields = User.objects.register(request.POST)
		if valid_fields[0] == "valid":
			request.session['id'] = valid_fields[1].id
			return redirect('/homepage')
		else:
			for i in valid_fields[1]:
				messages.error(request, i)
			return redirect('/')

def login(request):
	valid_login = User.objects.login(request.POST)
	if valid_login[0] == "valid":
		request.session['id'] = valid_login[1].id
		return redirect('/homepage')
	else:
		for i in valid_login[1]:
			messages.error(request, i)
		return redirect('/')

def homepage(request):
	if request.session['id'] == '':
		return redirect('/')
	user = User.objects.get(id = request.session['id'])
	context = {
	'users': user,
	'quotes': Quote.objects.all(),
	'favorites': Favorite.objects.filter(user = user)
	}
	print request.session['id']
	return render(request, 'belt_app/homepage.html', context)

def user(request, id):
	user = User.objects.get(id = id)
	context = {
	'user': user,
	'quotes': Quote.objects.filter(user = user)
	}
	return render(request, 'belt_app/userpage.html', context)

def log_out(request):
	request.session.clear()
	return redirect('/')

def add_quote(request):
	if request.method == "POST":
		valid_quote = Quote.objects.add_quote(request.POST, request.session['id'])
		if valid_quote[0] == "invalid":
			for i in valid_quote[1]:
				messages.error(request, i)
				return redirect('/homepage')
		else:
			return redirect('/homepage')

def remove_favorite(request, id):
	Quote.objects.remove_favorite(user_id = request.session['id'], quote_id = id)
	return redirect('/homepage')

def add_favorite(request, id):
	valid_add = Quote.objects.add_favorite(user_id = request.session['id'], quote_id = id)
	if valid_add[0] == "invalid":
		for i in valid_add[1]:
			messages.error(request, i)
			return redirect('/homepage')
	else:
		return redirect('/homepage')


