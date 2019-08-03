from flask import Flask, request
from core import Core
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
    return "{}</br>Current date: {}</br>Projected date: {}".format(sentence,datetime2str(res[0]),datetime2str(res[1]))

if __name__ == '__main__':
    app.run()
