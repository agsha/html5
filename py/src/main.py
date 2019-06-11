import logging
import os
import socket
import sqlite3
import sys
import json

from flask_cors import CORS

from flask import Flask


app = Flask(__name__)
CORS(app)


__author__ = 'sharath.g'


def go():
  from athena_tables.py.src.hello import bp
  print("blueprint is ", bp)
  app.register_blueprint(bp, url_prefix="")

go()
