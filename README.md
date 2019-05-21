# About
Hello! This is a sample web application with jquery + highcharts + python (flask) + SQLite3
It is meant for quick interactive data analysis. The intended workflow is:
* Measure what needs to be measured and populate an SQLite db and copy it over to this project `example.db`
* Hook it upto highcharts for easy visualization

# How to build and run

This project requires `> python 3.3`

* Load up your virtual environment `sudo apt-get install python3-venv` and `python3 -m venv .` and `source bin/activate`
* `pip install -r requirements.txt`
* `FLASK_APP=py.src.hello.py flask run`
* In _another_ terminal, start a static file server. e.g. `python3 -m http.server`
* navigate to http://localhost:8000/ in your browser

# Performance?
Highcharts is easily able to render two series of 50K points each. It starts creaking at 100K points. It REALLY struggles with 1M points. You know, the mouse dies for a couple of seconds, everything is choppy..., but does manage to render it in the end. Go crazy. 
