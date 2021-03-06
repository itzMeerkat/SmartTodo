from flask import Flask, request
from core import Core

import logging

app = Flask(__name__)

parser = Core()

def datetime2str(dt):
    return dt.strftime("%Y-%m-%d")

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/parse',methods=['POST'])
def parse():
    sentence = request.form['sentence']
    res = parser.getProjectedDate(sentence)
    if res is None:
        return "No date found"
    return "{}</br>Current date: {}</br>Projected date: {}".format(sentence,datetime2str(res[0]),datetime2str(res[1]))

if __name__ == '__main__':
    
    app.run(host='0.0.0.0')


