#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-10-27 17:12:48
# @Last Modified 2015-10-27

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
  return '<h1>HW</h1>'

if __name__ == '__main__':
  app.run(debug=True)
