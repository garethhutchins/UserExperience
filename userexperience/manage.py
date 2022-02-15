from urllib import response
import requests
from django.conf import settings as conf_settings
import json
from .train import update_model
def manage_model(request):
    #See if the model needs updating
    if 'topics_submit' in request.POST:
            #The topics are being updates
            update_model(request)
            
    #Get the URL Settings
    url = conf_settings.REST
    url = url + "/models/"
    #Get the model ID - check the name used in the post
    if 'model_id' in request.POST:
        model_id = request.POST['model_id']
    else:
        model_id = request.POST['model_name']
    url = url + model_id
    #see if it's a get or a delete
    if 'delete' in request.POST:
        a = 0
    else:
        #Get the model Information
        response = requests.request("GET",url)
        model_info = json.loads(response.text)[0]
        #See if there's a score
        if 'score' in model_info['topic_labels']:
            model_info['score'] = model_info['topic_labels']['score']*100
            model_info['score']= "{:.2f}".format(model_info['score'])
            model_info['topic_labels'] = model_info['topic_labels']['labels']
        #We don't need to save_model returned
        return model_info
        
    