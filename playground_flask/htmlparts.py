#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-10-27 17:01:13
# @Last Modified 2015-10-27


def prehead():
  pagehtml="""Content-type: text/html\n\n\n"""
  return pagehtml

def htmlHead():
  pagehtml = """
  <html>
    <head>
      <link rel="stylesheet" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">
      <script src="//code.jquery.com/jquery-1.10.2.js"></script>
      <script src="//code.jquery.com/ui/1.11.2/jquery-ui.js"></script>
      <script>
        $(function() {
          $( ".datepicker" ).datepicker();
        });
      </script>

      <style>

        @import url(http://fonts.googleapis.com/css?family=Open+Sans:400,700);

        * {
          padding:0;
          margin:0;
          position:relative;
          box-sizing:border-box;
        }
        body {
          font-size:16px;
          font-family: 'Open Sans', sans-serif;
        }



        h1,h2,h3 {
          color:#ff0000;
          text-align:center;
        }
        .errormessage{
          color: red;
          text-align: center;
          font-size: 64px;
        }
      </style>
      <meta http-equiv="Content-type" content="text/html;" />
      <title> Crackbrain: One off functions for Infusionsoft</title>
      <meta name="description" Content="One off searches and functions that are not a part of Infusionsoft." />
    </head>
    <body>
  """
  return pagehtml

def menu():
  pagehtml="""
  <div>
    <form method="POST">
      <input type="submit" name="logout" value="Logout">
      <input type="submit" name="btar" value="Better tag application report">
      <input type="submit" name="rancon" value="Pick Random Contacts">
      <input type="submit" name="alltags" value="All tags">
      <input type="submit" name="ordertest" value="Test Order Creation" />
    </form>
  </div>
  """
  return pagehtml



def gatherInfo():
  pagehtml= """
        <div class="p1">
          <h3>Welcome to Crackbra.in.</h3>
          <p>
            This is my personal collection of Infusionsoft functions that provide some added functionality to the core application.
            These functions are in no way affiliated with Infusionsoft nor any of its affiliates, they are just a set of functions
            that I expect that users will find useful.
            <br />
            These functions are provided with absolutely no warranty, guarantee, or any avenue of real meaningful support.  As of the
            time of this writing there are no functions that remove data from your Infusionsoft application, nor are there any that store data anywhere except in a cookie on your computer.  I use this so that I do not have to pass the app name and API key through hidden fields the whole time you are browsing. If you log out it will delete the cookie.
            <br />
            You can examine the most recent copy of the source code (that I have been bothered to upload) <a href="https://github.com/jeremiahmarks/betterTagApplicationReport">on its github page</a>, so you can self host this if you so wish.  This is also available so that you can improve it, please do fork the daylights out of it!.
          </p>
        </div>
        <div class="p2">
          <p>
            If the most recent version of code that is operating here does not appear to be hosted on github, or there is some
            functionality that you would like to see implemented, please do <a href="mailto:jeremiah@crackbra.in">email me</a>
            and let me know.
          </p>
        </div>
      <form method="POST">
        <label for="appname">Appname</label>
        <input type="text" name="appname" id="appname">
        <label for="apikey">API Key</label>
        <input type="text" name="apikey" id="apikey">
        <input type='submit' name="submit" value="submit">
      </form>
  """
  return pagehtml


def footer():
  pagehtml="""
    </body>
  </html>
  """
  return pagehtml
