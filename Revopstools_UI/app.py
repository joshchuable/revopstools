from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import sqlalchemy as sa
import datetime

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("contents.html")

@app.route("/valueCPM")
def valueCPM():
	return render_template("valueCPM/valueCPM.html")

@app.route("/pyscripts/valueCPM_calc", methods=['POST'])
def valueCPM_calc():
	# Get yesterday's date. Formatted as YYYY-MM-DD.
	yesterday = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(1),'%Y-%m-%d')
	two_days_ago = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(2),'%Y-%m-%d')

	# The queries that return the Rubicon value CPM data.
	# The wildcard character '%' must be escaped with a '%'.
	daily_by_tag = """
	SELECT
	 report_date,
	 keyword,
	 paid_impressions                                                       AS rubicon_paid_impressions,
	 publisher_gross_revenue                                                AS rubicon_revenue,
	 SUM(dfp_impressions)                                                   AS dfp_impressions,
	 (publisher_gross_revenue / (SUM(dfp_impressions) / 1000) * .88)        AS value_cpm
	FROM
	 admgmt.rubicon_stats_daily a
	INNER JOIN
	 (
	  SELECT
	    financial_date,
	    tag,
	    impressions                                                         AS dfp_impressions
	   FROM revenue.tbl_revenue_answ_param4
	   WHERE revenue_type LIKE "%%rubicon%%"
	   ) AS b
	ON a.report_date = b.financial_date
	AND a.keyword = b.tag
	WHERE report_date IN ("{0}","{1}")
	AND dfp_impressions > 10
	GROUP BY keyword, report_date
	ORDER BY keyword, report_date, dfp_impressions DESC
	"""

	# Defines the queries for each report.
	daily_by_tag_query = daily_by_tag.format(yesterday, two_days_ago)

	# Estabilsh database connection. Follows the convention "[engine_type]://[user]:[passwd]@[host]".
	e = sa.create_engine("mysql+pymysql://rye.jones:2E7GP6ZZ6@jupiter.afcv.net")

	df = pd.read_sql(daily_by_tag_query, e)

	output = df.to_csv(sep=",", index_label=False, index=False, header=True)

	return output


if __name__ == "__main__":
	app.run(debug=True)