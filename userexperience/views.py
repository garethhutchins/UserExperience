import re
import requests
import mimetypes
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
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        #Save the file so it can be read
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        full_file_path = fs.location + "/" + filename
        #Set the tika request url
        url = "http://localhost:9998/tika"
        #open the file for reading
        with open(full_file_path, 'rb') as f:
            payload=f.read()
        #Guess the Mime Type and set the content type for the tika request
        mime = mimetypes.guess_type(full_file_path)
        headers = {
                'Content-Type': mime[0]
                }
        response = requests.request("PUT", url, headers=headers, data=payload)
        #Now delete the file
        fs.delete(filename)
        #Now send the text results back to the testing page
        args = {'result' : response.text }
        return render(request, 'userexperience/train.html', args)
    return render(request, "userexperience/train.html")
def settings(request):
    #Save the settings
    if request.method == 'POST':
        print(conf_settings.TIKA)
        #settings.TIKA = 'Test'
        conf_settings.TIKA = "http://localhost:9998/tika"
    return render(request, "userexperience/settings.html")
def about(request):
    return render(request, "userexperience/about.html")
def contact(request):
    return render(request,"userexperience/contact.html")

print('starting web app')
print('http://127.0.0.1:8000/userexperience/VSCode')
