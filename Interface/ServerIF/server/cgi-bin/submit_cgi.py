#!/bin/python

import cgi
import flask

form = cgi.FieldStorage()
searchterm = form.getvalue('searchbox')

flask.redirect('/')
