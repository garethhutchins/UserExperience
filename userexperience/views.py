import re
import requests

import pandas as pd

from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import datetime

from django.conf import settings as conf_settings
from django.apps import apps
from flatten_json import flatten
from .train import load_csv, table_submit
# Create your views here.
def home(request):
    return render(request, "userexperience/home.html")

def test(request):
    return render(request, "userexperience/test.html")
def train(request):
    #Check to see if a file has been selected
    if request.method == 'POST' and "file_upload" in request.POST:
        myfile = request.FILES['myfile']
        args = load_csv(myfile)
        return render(request, 'userexperience/train.html', args)
    #See if the post is from the user selecting the correct columns from a previously uploaded file
    if request.method == "POST" and "table_submit" in request.POST:
        #This is now sending the table to be cleaned
        args = table_submit(request)
        return render(request, 'userexperience/train.html', args)
    args = {'text' : True}
    return render(request, "userexperience/train.html",args)
def settings(request):
    #Get the settings from the file
    #Save the settings
    if request.method == 'POST':
        #Get the form data
        tika_url = request.POST.get('tika_url')
        conf_settings.TIKA = tika_url
    args = {'tika_url' : conf_settings.TIKA}
    return render(request, "userexperience/settings.html",args)
def about(request):
    return render(request, "userexperience/about.html")
def contact(request):
    return render(request,"userexperience/contact.html")

print('starting web app')
print('http://127.0.0.1:8000/userexperience/VSCode')
