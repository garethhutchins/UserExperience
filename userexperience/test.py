from email import header
from http.client import HTTPException
from urllib import response
from django.core.files.storage import FileSystemStorage
from django.conf import settings as conf_settings
import mimetypes
import pandas as pd
import json
import re
import requests
import matplotlib
import base64
import uuid

def list_models():
    #Get the URL from the setting
    url = conf_settings.REST
    url = url + "/models/"
    try:
        response = requests.request("GET",url)
    except:
        data = {}
        return 500, data, {'Message':'Unable to Connect to REST services, check settings'}
    
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
            topic_labels = []
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

def analyse_document(request):
    #Get the file and save it
    file_uploaded = request._files['myfile']
    #Content Type
    content_type = file_uploaded.content_type
    #File Name
    name = file_uploaded.name
    #Save the file so it can be read
    fs = FileSystemStorage()
    filename = fs.save(name, file_uploaded)
    full_file_path = fs.location + "/" + filename
    tika = 'true'
    tika_uri = conf_settings.TIKA
    headers = {
                    'Content-Type': content_type
                    }
    #open the file for reading
    with open(full_file_path, 'rb') as f:
        payload=f.read()
    try:
        response = requests.request('PUT',tika_uri,headers=headers, data=payload)
    except:
        fs.delete(filename)
        return {'message':'Unable to reach TIKA Server - Check Settings'}
    if response.status_code != 200:
        #An Error Occured
        fs.delete(filename)
        return {'message':response.text}
    text = response.text
    fs.delete(filename)
    #Now look at the model ID
    model_id = request.POST['model_id']
    req = {}
    req['text'] = text
    req['model_id'] = model_id
    #Get the window size settings
    req['window_size'] = conf_settings.WINDOW_SIZE
    req['window_slide'] = conf_settings.WINDOW_SLIDE
    headers = {}
    url = conf_settings.REST
    url = url + "/process_text/"
    try:
        response = requests.request("POST",url,headers=headers,data=req)
    except:
        return {'message','Unable to Connect to REST services, check settings'}
    #Now get the results from the post
    results = json.loads(response.text)
    #Now check the model type to tailor the results
    
    if results['model_type'] == 'TF-IDF':
        texts = []
        top_topic = []
        topics = []
        scores = []
        #Loop through al of the results
        for r in results['process_results']:
            texts.append(r['Text'])
            top_topic.append(r['Topics'][0])
            topics.append(r['Topics'])
            scores.append(r['Scores'])
        #Create the Topic Flow Image
        #Save the results to a dataframe
        df = pd.DataFrame()
        df['Text'] = texts
        df['Topics'] = topics
        df['Scores'] = scores
        #First get the list of Topics and scores from the df
        flow = df[['Topics','Scores']]
        tf_topics = flow['Topics'][0]
        df = pd.DataFrame(flow['Scores'].to_list(),columns=topics)
        lines = df.plot.line(figsize=(15,5),title="Topic Flow")
        lines.set_xlabel("Window Position")
        lines.set_ylabel("Topic Score")
        fig = lines.get_figure()
        fname = str(uuid.uuid4())
        fig.savefig(fname + ".png")
        img = base64.encode(fname+".png")
        #Now return these results
        return {'model_type':results['model_type'],'text':texts,'top_topic':top_topic,'topics':topics,'scores':scores,'plot':img}
    
