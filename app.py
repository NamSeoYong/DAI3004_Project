from flask import Flask, render_template, Response, Request
from time import sleep

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/object')
def object():
    return render_template("object.html")

@app.route('/cam')
def cam():
    return render_template('cam.html')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=443, debug=True)
