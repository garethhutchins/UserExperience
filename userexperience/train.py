from django.core.files.storage import FileSystemStorage
from django.conf import settings as conf_settings
import mimetypes
import pandas as pd
import json
import re
import requests

def load_csv(myfile):
    #Look to see what needs to be treaded as csv
    csv_types = ["application/vnd.ms-excel","application/csv","text/csv"]
    #Save the file so it can be read
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    full_file_path = fs.location + "/" + filename
    #Guess the Mime Type
    mime = mimetypes.guess_type(full_file_path)
    if mime[0] in csv_types:
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
        args = {'text' : False, 'table_data' : data, 'column_names' : column_names, 'index_name' : index_name, 'first_view' : True}
        return args

def table_submit(request):
    selected_column = request.POST.get('selected_column')
    #Now loop through all of the elemets to convert them into arrays
    list_vals = []
    for key, value in request.POST.items():
        #Look to see if the column is a mathc
        if re.search(selected_column,key):
            #Add the value to a list
            list_vals.append(value)
    df = pd.DataFrame(list_vals)
    json_records = df.to_json(orient='records')
    data = []
    data = json.loads(json_records)
    #Now send the results back to the page
    args = {'text' : False, 'table_data' : data, 'index_name' : selected_column, 'cleaned' : True}
    return args
def model_train(request):
    #Get the URL from the setting
    url = conf_settings.REST
    url = url + "/train_topic_table/"
    #Now get the items from the request
    req = {}
    column = request.POST.get('training_param')
    req['selected_column'] = column
    model_selection = request.POST.get('model_selection')
    req['model_type'] = model_selection
    #Now look to see what model has been selected to get the rest of the information
    if model_selection == "K-MEANS":
        num_topics = request.POST.get('num_topics')
        req['num_topics'] = num_topics
    if model_selection == "TF-IDF":
        normalisation = request.POST.get('normalisation')
        req['normalisation'] = normalisation
        label_column = request.POST.get('label_column')
        req['label_column'] = label_column
    if model_selection == "NMF" or model_selection == "LDA":
        normalisation = request.POST.get('normalisation')
        req['normalisation'] = normalisation
        num_topics = request.POST.get('num_topics')
        req['num_topics'] = num_topics
    #Now get the file
    #Save the file so it can be read
    fs = FileSystemStorage()
    myfile = request._files['myfile']
    filename = fs.save(myfile.name, myfile)
    full_file_path = fs.location + "/" + filename
    #Guess the Mime Type
    mime = mimetypes.guess_type(full_file_path)
    with open(full_file_path, 'rb') as file:
    
        files=[
            ('file',(filename,file,mime[0]))
        ]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=req, files=files)
    
    #Now delete the file
    fs.delete(filename)
    if response.status_code == 200 :
        #Everything is OK
        #Load the Json response
        res = json.loads(response.content)
        model_type = res['model_type']
        model_name = res['name']
        topics_image = res['topics_image']
        num_topics = res['num_topics']
        if model_type == "TF-IDF":
            labels = res['topic_labels']['labels']
            score = res['topic_labels']['score']
            args = {'model_type' : model_type, 'model_name': model_name, 'topics_image': topics_image,
            'labels': labels, 'score' :score}
        else:
            labels = res['topic_labels']
            
            if len(labels) == 0:
                labels = {}
                for x in range(1,num_topics+1):
                    labels[x] = ""
            args = {'model_type' : model_type, 'model_name': model_name, 'topics_image': topics_image,
            'labels': labels}
        return response.status_code, args
    else:
        args = {'Error' : response.text}
        return response.status_code, args