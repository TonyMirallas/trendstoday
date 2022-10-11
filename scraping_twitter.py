from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager # Code 2
import pickle # serialize cookies and save on pkl file. Load cookies after that
import time
import datetime
from init_db import get_db_connection

def twitter_scraping():

    # If headless mode is on, then twitter opens on white mode, which changes css classes. Thats why headless is off

    #headless = wont open browser
    options = Options()
    # options.add_argument("--window-size=1920,1080")
    # options.add_argument("--headless")

    driver = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install()) # Code 3
    # driver.get("https://twitter.com/explore/tabs/for-you")
    driver.get("https://twitter.com/explore/tabs/trending")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(3)
    # driver.get_screenshot_as_file("screenshot.png")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)
    driver.execute_script("scrollBy(0, -2000)")

    time.sleep(2)
    # spans = driver.find_elements(By.CSS_SELECTOR, 'span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0')

    conn = get_db_connection()    
    cursor = conn.cursor()
    sql = "INSERT INTO trend(title, tweet, category, datetime) VALUES(?,?,?,?);"

    trends = driver.find_elements(By.XPATH, "//div[@class='css-1dbjc4n r-1loqt21 r-6koalj r-1ny4l3l r-ymttw5 r-1f1sjgu r-o7ynqc r-6416eg']/div[@class='css-1dbjc4n r-16y2uox r-bnwqim']")

    for trend in trends:

        try:
            title = trend.find_element(By.XPATH, ".//div[@class='css-901oao r-1nao33i r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-1bymd8e r-bcqeeo r-qvutc0']//span[@class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']").text
        except NoSuchElementException:
            title = "Title not found"

        try:
            tweet = trend.find_element(By.XPATH, ".//div[@class='css-901oao r-1bwzh9t r-37j5jr r-n6v787 r-16dba41 r-1cwl3u0 r-14gqq1x r-bcqeeo r-qvutc0']//span[@class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']").text
        except NoSuchElementException:
            tweet = "0"

        try:
            category = trend.find_elements(By.XPATH, ".//div[@class='css-1dbjc4n r-1d09ksm r-18u37iz r-1wbh5a2']//span[@class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']")
        except NoSuchElementException:
            category = "Category not found"

        if len(category) < 2:
            category = "Category length too short"
        
        else:
            temp = category[2].text
            category = temp

        today = datetime.datetime.now().strftime('%Y-%m-%d %H')

        tweet = tweet.replace("Tweets", "")
        tweet = tweet.replace(" ", "")
        tweet = tweet.replace(".", "")

        if "mil" in tweet:
            tweet = tweet.replace("mil", "")

            if "," in tweet:
                tweet = tweet.replace(",", ".")

            try:
                tweet = float(tweet) * 1000
            except Exception:
                tweet = 0
        else:
            try:
                tweet = float(tweet)
            except Exception:
                tweet = 0
        tweet = int(tweet)

        cursor.execute(sql, (title, tweet, category, today))
        conn.commit()
        print("Title: " + title + " Tweet: " + str(tweet) + " Category: " + category + " Date: " + today)

    conn.close()
    driver.close()
    print("----- Scraping finalized -----")

    # save cookies on cookies.pkl file
    # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
