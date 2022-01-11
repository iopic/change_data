from server import app
from flask import Flask, request,current_app #for testing
from jinja2 import Template
from forms import DocumentUploadForm

with app.app_context():
    current_app.name

app.url_map 
with app.test_request_context('/'):
...     print(request.path)  # get the full path of the requested page without the domain name.
...     print(request.method)
...     print(current_app.name)

t = Template("Name: {{ name }}")


form = DocumentUploadForm()


import pandas as pd
from datetime import datetime

current_file = '/Users/samahol/Documents/beta/instance/covid_impact_education.csv'

df = pd.read_csv(current_file)
df['Date']=df['Date'].apply(lambda d: datetime.strptime(d, "%d/%m/%Y"))

#make basic chart: country by status
df_grouped = df.groupby(['Status','Country']).size().reset_index(name='count')
   
df_status = df.groupby(['Status']).size().reset_index(name='count')

labels = df_status['Status'].tolist()

values = df_status['count'].tolist()