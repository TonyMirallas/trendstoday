from cgi import test
import time
import schedule
from scraping_twitter import twitter_scraping


schedule.every().day.at("11:00").do(twitter_scraping)
schedule.every().day.at("22:00").do(twitter_scraping)
# schedule.every().day.at("17:48").do(twitter_scraping)

while True:
    schedule.run_pending()
    print("Its all good man...")
    time.sleep(60*30)
    # time.sleep(1)
