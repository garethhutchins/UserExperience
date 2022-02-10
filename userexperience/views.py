import re
from turtle import update
import requests

import pandas as pd

from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import datetime

from django.conf import settings as conf_settings
from django.apps import apps
from flatten_json import flatten
from .train import load_csv, table_submit, model_train, update_model
from .test import list_models, analyse_document
# Create your views here.
def home(request):
    #If it's the first time - get the list of models to select from
    if request.method != "POST":
        #Get the list of Models
        status_code, df_j, column_names = list_models()
        if status_code == 200:
            args = {'df_j':df_j,'column_names':column_names}
        else:
            args = {'message':df_j}
        return render(request, "userexperience/home.html",args)
    #Now lets' upload the document as it's a post
    results = analyse_document(request)
    #see if there's an error
    if 'message' in results:
        args = results
        return render(request, "userexperience/home.html",args)
    #Return the results back to the results page
    args = analyse_document(request)
    return render(request,"userexperience/results.html",args)    
def results(request):
    return render(request,"userexperience/results.html")
def test(request):
    return render(request, "userexperience/test.html")
def train(request):
    #Check to see if a file has been selected
    if request.method == 'POST' and "file_upload" in request.POST:
        myfile = request.FILES['myfile']
        args = load_csv(myfile)
        return render(request, 'userexperience/train.html', args)
    #See if the post is from the model parameter screen
    if request.method == "POST" and "model_selection" in request.POST:
        args = model_train(request)
        return render(request, 'userexperience/train.html', args[1])
    #Now Update the Topics
    if request.method == "POST" and 'topic_label_1' in request.POST:
        img = update_model(request)
        args = {'updated_image':img}
        return render(request, "userexperience/train.html",args)
    args = {'first' : True}
    return render(request, "userexperience/train.html",args)
def settings(request):
    #Get the settings from the file
    #Save the settings
    if request.method == 'POST':
        #Get the form data
        tika_url = request.POST.get('tika_url')
        conf_settings.TIKA = tika_url
        rest_url = request.POST.get('rest_url')
        conf_settings.REST = rest_url
        conf_settings.WINDOW_SIZE = request.POST.get('window_size')
        conf_settings.WINDOW_SLIDE = request.POST.get('window_slide')
    args = {'tika_url' : conf_settings.TIKA,'rest_url':conf_settings.REST,'window_size':conf_settings.WINDOW_SIZE,'window_slide':conf_settings.WINDOW_SLIDE}
    return render(request, "userexperience/settings.html",args)
def about(request):
    return render(request, "userexperience/about.html")
def contact(request):
    return render(request,"userexperience/contact.html")

print('starting web app')
print('http://127.0.0.1:8000/userexperience/VSCode')
