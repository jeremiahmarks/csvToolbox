#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-10-27 17:12:48
# @Last Modified 2015-10-27

from flask import Flask, render_template
from flask.ext.script import Manager
app = Flask(__name__)
manager = Manager(app)
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/app/<appname>')
def apppage(appname):
    return render_template('applicationScreen.html', appname=appname)

if __name__ == '__main__':
  manager.run()
