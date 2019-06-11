import logging
import os
import socket
import sqlite3
import sys
import json

import psycopg2 as psycopg2

from athena_tables.py.src.chart_template import Chart
from flask import  Blueprint

bp = Blueprint('athena_tables', __name__)
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

db_file = os.path.abspath(os.path.join(this_dir, "example.db"))
log.error(db_file)


def insert():
  pg = psycopg2.connect(host="10.30.1.2", port=5432, database="athena", user="athena", password="")
  print(pg)
  c = pg.cursor()
  c.execute("""SELECT nspname || '.' || relname AS "relation",
    (pg_total_relation_size(C.oid)) AS "total_size", reltuples::numeric::integer AS approximate_row_count
  FROM pg_class C
  LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
  WHERE nspname NOT IN ('pg_catalog', 'information_schema')
    AND C.relkind <> 'i'
    AND nspname !~ '^pg_toast'
  ORDER BY pg_total_relation_size(C.oid) DESC""")
  rows = c.fetchall()

  conn = sqlite3.connect(db_file)
  c = conn.cursor()

  c.executemany("INSERT INTO athena_info (name, size, rows) VALUES (?, ?, ?)", rows)
  conn.commit()
  conn.close()
  pg.close()


def query():
  conn = sqlite3.connect(db_file)

  chart1 = Chart()
  chart1.title("Athena table sizes and rows").xtitle("table names").ytitle("size in bytes").ytitle("num rows").ytitle("bytes per row")


  c = conn.cursor()
  categories = []
  for row in c.execute('SELECT * FROM athena_info ORDER BY size desc'):
    categories.append(row[0].replace("public.", ""))
    print(row[0].replace("public.", ""))
    chart1.add_point("size_bytes", int(row[1]))
    chart1.add_point("num_rows", int(row[2]))
    if row[2] == 0:
      chart1.add_point("bytes_per_row", 0)
    else:
      chart1.add_point("bytes_per_row", int(row[1]/row[2]))

  chart1.xcategories(categories)
  return json.dumps({"chart1": chart1.obj})


def truncate():
  conn = sqlite3.connect(db_file)
  c = conn.cursor()
  c.execute("delete from athena_info")
  conn.commit()
  conn.close()

def ddl():
  conn = sqlite3.connect(db_file)
  c = conn.cursor()
  c.execute("drop table athena_info")


  c.execute("""CREATE TABLE athena_info (
	name TEXT,
	"size" NUMERIC,
	"rows" NUMERIC
);
""")

@bp.route("/athena_tables/hello")
def go2():
  # ddl()
  # truncate()
  # insert()
  return query()


if __name__ == "__main__":
  go2()
