from flask import Flask, request, render_template, make_response
from io import StringIO
import numpy as np
import pandas as pd
import sqlalchemy as sa
import datetime
from pscripts.valueCPM_calc import valueCPM_calc

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("contents.html")

@app.route("/valueCPM")
def valueCPM():
	return render_template("valueCPM/valueCPM.html")

@app.route("/settings")
def settings():
	return render_template("settings/settings.html")

@app.route("/pyscripts/valueCPM_calc", methods=['GET'])
def return_valueCPM():
	return valueCPM_calc();


if __name__ == "__main__":
	app.run(debug=True)