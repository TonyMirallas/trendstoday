from unicodedata import category
from flask import Flask, render_template
import sqlite3
import datetime

# Flask 2.2.2
# Python 3.8.10
# App to scrap twitter tt every day at 11 and 22 (schedule script on scheduled_jobs.py). Also it shows some stats about those scrapings

# one page for every hour (10, 17, 22) or for every day of tt

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('trendstoday.db')
    # conn.row_factory = sqlite3.Row # get results as python dictionarie
    return conn


def trend_by_date(conn, operator, date=None):

    if operator == "closer":
        sql = 'SELECT MAX(datetime), title FROM trend'
        datetime = conn.execute(sql).fetchall()[0][0]
        sql = 'SELECT * FROM trend WHERE datetime = "' + datetime + '"'

    elif operator == "before":
        sql = 'SELECT * FROM trend WHERE datetime < "' + date + '"'

    elif operator == "after":
        sql = 'SELECT * FROM trend WHERE datetime > "' + date + '"'

    elif operator == "equal":
        sql = 'SELECT * FROM trend WHERE datetime = "' + date + '"'

    trends = conn.execute(sql).fetchall()
    return trends


@app.route('/')
def index():
    # hour = datetime.datetime.now().strftime('%H')
    # today = datetime.datetime.now().strftime('%Y-%m-%d')
    conn = get_db_connection()
    trends = trend_by_date(conn, "closer")
    list_trends = []

    for trend in trends:
        print(trend)
        title = trend[0]
        tweet = trend[1]
        category = trend[2]
        date = trend[3]
        if '#' in title:
            src = 'https://twitter.com/search?q=' + \
                title.replace('#', '%23') + '&src=trend_click&vertical=trends'
        else:
            src = 'https://twitter.com/search?q=' + \
                title + '&src=trend_click&vertical=trends'

        dict_trend = {
            "title": title,
            "tweet": tweet,
            "category": category,
            "src": src
        }

        list_trends.append(dict_trend)

    conn.close()
    return render_template('index.html', trends=list_trends, date=date)
