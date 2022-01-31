from urllib import response
from django.core.files.storage import FileSystemStorage
from django.conf import settings as conf_settings
import mimetypes
import pandas as pd
import json
import re
import requests

def list_models():
    #Get the URL from the setting
    url = conf_settings.REST
    url = url + "/models/"
    response = requests.request("GET",url)
    if response.status_code != 200:
        return response.status_code, {'Message':'Unable to Connect to REST services, check settings'}
    #Get the json
    js = json.loads(response.text)
    model_name = []
    model_type = []
    training_file = []
    normalisation = []
    score = []
    image = []
    labels = []
    #Now loop through all of the response
    for j in js:
        model_name.append(j['name'])
        model_type.append(j['model_type'])
        normalisation.append(j['normalisation'])
        training_file.append(j['file_name'])
        #try for score
        try:
            score.append(j['topic_labels']['score'])
            #Now add TF-IDF labels
            topic_labels = []
            for key, value in j['topic_labels']['labels'].items():
                topic_labels.append(value)
            labels.append(", ".join(topic_labels))
        except:
            score.append('0')
            #Now do the same for other model types
            for key, value in j['topic_labels'].items():
                topic_labels.append(value)
            labels.append(", ".join(topic_labels))

        
    #Now create an empty dataframe
    df = pd.DataFrame()
    df['Model ID'] = model_name
    df['Model Type'] = model_type
    df['Training File'] = training_file
    df['Normalisation'] = normalisation
    df['Score'] = score
    df['Topics'] = labels
    
    df_j = df.to_json(orient="records")
    data = []
    data = json.loads(df_j)
    column_names = df.columns.values
    return response.status_code, data, column_names
