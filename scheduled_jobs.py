import time
import schedule
from scraping_twitter import twitter_scraping


schedule.every().day.at("11:00").do(twitter_scraping)
schedule.every().day.at("22:00").do(twitter_scraping)
# schedule.every().day.at("17:48").do(twitter_scraping)

while True:
    schedule.run_pending()
    today = time.strftime("%Y-%m-%d %H %M %S", time.localtime())
    print("Its all good man... (" + today + ")")
    # time.sleep(30)
    time.sleep(1)
