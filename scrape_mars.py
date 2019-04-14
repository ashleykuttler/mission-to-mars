# Declare Dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time

#initiate browser 
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

#Create MARS Dictionary to import into Mongo
mars_info = {}

#MARS NEWS
def scrape_news():
    try:
        browser = init_browser()
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        mars_info['news_title']= news_title
        mars_info['news_p']= news_p

        return mars_info
    finally:
        browser.quit()

#FEATURED IMAGE
def scrape_featured_image():
    try:
        browser = init_browser()
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)

        browser.click_link_by_partial_text('FULL IMAGE')
        time.sleep(2)
        browser.click_link_by_partial_text('more info')
        time.sleep(2)
        browser.click_link_by_partial_text('.jpg')
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        featured_img_url = soup.find('img').get('src')
        mars_info['featured_img_url'] = featured_img_url

        return mars_info
    finally:
        browser.quit()


#MARS WEATHER
def scrape_weather():
    try:
        browser = init_browser()
        twitter_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(twitter_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        headers = soup.find_all('div', class_='stream-item-header')
        tweets = soup.find('div', class_='js-tweet-text-container')
        for header in headers: 
            header = header.find('b').text
            if 'MarsWxReport' in header:
                latest_tweet= tweets.find('p').text
                mars_info['latest_tweet']=latest_tweet
                break
            else: 
                pass
        return mars_info
    finally:
        browser.quit()

#MARS FACTS
def scrape_facts():
    try:
        browser = init_browser()
        url = 'https://space-facts.com/mars/'
        tables = pd.read_html(url)
        df = tables[0]
        df.columns = ['Property', 'Value']
        facts = df.to_html()
        mars_info['tables'] = facts
        return mars_info
    finally:
        browser.quit()


#MARS HEMISPHERES
def scrape_hemispheres():
    try: 
        browser = init_browser() 
        hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hem_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='item')

        hem_url_list = []
        base_url = 'https://astrogeology.usgs.gov' 

        for i in items: 
            title = i.find('h3').text
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            browser.visit(base_url + partial_img_url)
            partial_img_html = browser.html
            soup = BeautifulSoup(partial_img_html, 'html.parser')
            img_url = base_url + soup.find('img', class_='wide-image')['src']
            
            hem_url_list.append({"title" : title, "img_url" : img_url})
            mars_info['hem_url_list'] = hem_url_list
        return mars_info
    finally:
        browser.quit()