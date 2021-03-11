import re
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import datetime
# Create your views here.
def home(request):
    return render(request, "userexperience/home.html")
def hello_there(request, name):
   return render(
       request,
       'userexperience/hello_there.html', {
           'name': name,
           'date':datetime.now()
       }
   )
def about(request):
    return render(request, "userexperience/about.html")
def contact(request):
    return render(request,"userexperience/contact.html")
print('starting web app')
print('http://127.0.0.1:8000/userexperience/VSCode')