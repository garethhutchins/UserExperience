import re
import requests
import mimetypes
import pandas as pd
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings as conf_settings
from django.apps import apps
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
def test(request):
    return render(request, "userexperience/test.html")
def train(request):
    #Check to see if a file has been selected
    #Look to see what needs to be treaded as csv
    csv_types = ["application/vnd.ms-excel","application/csv","text/csv"]
    if request.method == 'POST' and "file_upload" in request.POST:
        myfile = request.FILES['myfile']
        #Save the file so it can be read
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        full_file_path = fs.location + "/" + filename
        #Guess the Mime Type
        mime = mimetypes.guess_type(full_file_path)
        csv = request.POST.get('csv')
        if mime[0] in csv_types and csv == 'on':
            print('csv')
            #Read the file in Pandas
            df = pd.read_csv(full_file_path,index_col=0)
            #Now delete the file
            fs.delete(filename)
            #Set the result to be the dataframe as a string
            index_name = df.index.name
            column_names = df.columns
            json_records = df.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            args = {'text' : False, 'table_data' : data, 'column_names' : column_names, 'index_name' : index_name}
        else:
            #Put the document through tika
            #Set the tika request url
            url = conf_settings.TIKA
            #open the file for reading
            with open(full_file_path, 'rb') as f:
                payload=f.read()
            #Add the header
            headers = {
                    'Content-Type': mime[0]
                    }
            response = requests.request("PUT", url, headers=headers, data=payload)
            #Now delete the file
            fs.delete(filename)
            #Now send the text results back to the testing page
            args = {'result' : response.text, 'text' : True }
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
