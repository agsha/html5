import logging
import os
import socket
import sqlite3
import sys
import json

from flask_cors import CORS

from py.src.chart_template import Chart
from flask import Flask
app = Flask(__name__)
CORS(app)
console = logging.StreamHandler(sys.stdout)
console.setFormatter(logging.Formatter("%(message)s"))
logging.getLogger('').addHandler(console)
logging.getLogger('').setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

this_host = socket.gethostname()
try:
  this_ip = socket.gethostbyname(this_host)
except:
  pass
this_file = os.path.abspath(__file__)
this_file_name = os.path.basename(__file__)
this_dir = os.path.dirname(os.path.abspath(__file__))
home_dir = os.path.expanduser('~')

__author__ = 'sharath.g'

db_file = os.path.abspath(os.path.join(this_dir, "..", "..", "example.db"))
log.error(db_file)


def insert(num):
  conn = sqlite3.connect(db_file)

  c = conn.cursor()
  values = []
  for i in range(num):
    values.append(("series1", i))
    values.append(("series2", num - 1 - i))

  c.executemany("INSERT INTO series (name, value) VALUES (?, ?)", values)
  conn.commit()
  conn.close()

def query():
  conn = sqlite3.connect(db_file)

  chart = Chart()
  c = conn.cursor()
  chart.title("My first chart").xtitle("data point number").ytitle("value of series")

  for row in c.execute('SELECT * FROM series ORDER BY name'):
    chart.add_point(row[0], int(row[1]))

  print(json.dumps(chart.obj, indent=2))
  return json.dumps(chart.obj, indent=2)


def truncate():
  conn = sqlite3.connect(db_file)
  c = conn.cursor()
  c.execute("delete from series")
  conn.commit()
  conn.close()

@app.route("/hello")
def go():
  truncate()
  insert(1000)
  return query()


if __name__ == "__main__":
  go()
