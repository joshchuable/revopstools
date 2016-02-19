import numpy as np
import pandas as pd
import sqlalchemy as sa
import datetime
# This function is built out in the second file below.
from sendgmailfinal import send_gmail

# This first file connects to jupiter, runs a SQL query, 
# saves the returned data in temp csv files, and then emails them to RVOA.
# Please note that 'PASSWORD' needs to be changed to your password.

# Get yesterday's date. Formatted as YYYY-MM-DD.
yesterday = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(1),'%Y-%m-%d')
two_days_ago = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(2),'%Y-%m-%d')

# Estabilsh database connection. Follows the convention "[engine_type]://[user]:[passwd]@[host]".
e = sa.create_engine("mysql+pymysql://rye.jones:PASSWORD@jupiter.afcv.net")

# Takes a sequel query and returns the data in a dataframe.
def sql_to_df(sql_query):
    # Set the dataframe to the returned values from the query.
    df = pd.read_sql(sql_query, e)
    # Return the dataframe.
    return df

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

# Set the returned SQL data from the queries to dataframes.
rubicon_daily_by_tag_report_csv = sql_to_df(daily_by_tag_query)
rubicon_daily_overall_report_csv = sql_to_df(daily_overall_query)

# Create file paths.
daily_by_tag_email_path = "/Users/rye.jones/Desktop/4-Code/ValueCPMs/reports_temp/daily_by_tag_%s.csv" % yesterday
daily_overall_email_path = "/Users/rye.jones/Desktop/4-Code/ValueCPMs/reports_temp/daily_overall_%s.csv" % yesterday

# Set inputs for send_gmail().
daily_by_tag_email = rubicon_daily_by_tag_report_csv.to_csv(daily_by_tag_email_path, sep=",", index_label=False, index=False, header=True)
daily_overall_email = rubicon_daily_overall_report_csv.to_csv(daily_overall_email_path, sep=",", index_label=False, index=False, header=True)

# Send the email with the file attachments.
send_gmail([daily_by_tag_email_path,daily_overall_email_path])