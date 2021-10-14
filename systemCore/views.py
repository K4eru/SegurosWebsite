from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.

@login_required(login_url="login")
def home(request):
	response = requests.get('http://127.0.0.1:8000/messages/')
	mesagges = response.json()
	return render(request, "index.html", {"mesagges": mesagges})