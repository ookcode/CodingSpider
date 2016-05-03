#!/usr/bin/python
#coding=utf-8
import os
from flask import Flask
from flask import Response
from flask import request

app = Flask(__name__)
@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/env')
def env():
    html = "System Environment:\n\n"
    for env in os.environ.keys():
        html += env + ': ' + os.environ[env] + "\n"
    return Response(html, mimetype='text/plain')

@app.route('/spider', methods=['GET', 'POST'])
def spider():
    if 'username' in request.args and 'password' in request.args :
        username = request.args['username']
        password = request.args['password']
        output = os.popen("python coding_spider.py -u {} -p {}".format(username,password))
        return Response(output.read(), mimetype='text/plain')
    else :
        return Response('error params,please input username and password', mimetype='text/plain')

if __name__ == "__main__":
    app.run()