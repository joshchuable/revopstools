from flask import Flask, request, render_template, make_response
from io import BytesIO
import numpy as np
import pandas as pd
from pandas import ExcelWriter
import sqlalchemy as sa
import datetime

def valueCPM_calc():
	# Get yesterday's date. Formatted as YYYY-MM-DD.
	yesterday = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(1),'%Y-%m-%d')
	two_days_ago = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(2),'%Y-%m-%d')

	# Estabilsh database connection. Follows the convention "[engine_type]://[user]:[passwd]@[host]".
	e = sa.create_engine("mysql+pymysql://rye.jones:2E7GP6ZZ6@jupiter.afcv.net")

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

	daily_overall = """
	SELECT
	 report_date,
	 SUM(paid_impressions)                                                       AS rubicon_paid_impressions,
	 SUM(publisher_gross_revenue)                                                AS rubicon_revenue,
	 dfp_impressions                                                             AS dfp_impressions,
	 (SUM(publisher_gross_revenue) / (dfp_impressions / 1000) * .88)             AS value_cpm
	FROM
	 admgmt.rubicon_stats_daily a
	INNER JOIN
	 (
	  SELECT 
	    financial_date,
	    SUM(impressions)                                                         AS dfp_impressions
	   FROM revenue.tbl_revenue_answ_param4
	   WHERE revenue_type LIKE "%%rubicon%%"
	   GROUP BY financial_date
	   ) AS b
	ON a.report_date = b.financial_date
	WHERE report_date IN ("{0}","{1}")
	GROUP BY report_date
	"""

	# Defines the queries for each report.
	daily_by_tag_query = daily_by_tag.format(yesterday, two_days_ago)
	daily_overall_query = daily_overall.format(yesterday, two_days_ago)

	def sql_to_df(sql_query):
	    # Set the dataframe to the returned values from the query.
	    df = pd.read_sql(sql_query, e)
	    # Return the dataframe.
	    return df

	# Set the returned SQL data from the queries to dataframes.
	rubicon_daily_by_tag_report = sql_to_df(daily_by_tag_query)
	rubicon_daily_overall_report = sql_to_df(daily_overall_query)

	# Set the dataframes to different sheets in a single xls file.
	io = BytesIO()
	writer = ExcelWriter('temp.xlsx', engine='xlsxwriter')
	writer.book.filename = io
	rubicon_daily_overall_report.to_excel(writer,'Rubicon Overall',index=False,header=True,index_label=None)
	rubicon_daily_by_tag_report.to_excel(writer,'Rubicon by Tag',index=False,header=True,index_label=None)
	writer.save()

	excel_file = io.getvalue()

	response = make_response(excel_file)
	response.headers["Content-Disposition"] = "attachment; filename=Rubicon_Daily_%s" % yesterday

	return response