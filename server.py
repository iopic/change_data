from flask.templating import render_template
from forms import DocumentUploadForm
import os
from flask import current_app #for testing
from flask import Flask, flash, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import pandas as pd
import json
import plotly
from utils import load_data

app = Flask(__name__)


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# create the folders when setting up your app
os.makedirs(os.path.join(app.instance_path, 'instance'), exist_ok=True)




@app.route('/', methods=['GET', 'POST'])
def set_charts():
    #print(dir(request))
    #print(request.form)
    #print(request.files)
    #print(request.method)
    #print(dir(request))
    #print(request.values)
    #print(request.form)
    
    #generate some data
    chart_data = load_data()
    
    print(chart_data)
    return render_template('index.html', 
                    chart_list = chart_data,
                    selector_opts = [x['title'] for x in chart_data])



if __name__ == "__main__":
  app.run(debug = True, port = 8000)