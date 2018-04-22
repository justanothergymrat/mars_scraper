import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import selenium


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    browser = init_browser()
    mars = {}

    mars_news = []

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    content= soup.findAll("li", class_='slide')
    # print(len(content))
    for i in range(0,len(content)):
        title =  content[i].find('h3').get_text()
        text = content[i].find('div', class_='article_teaser_body').get_text()
        news_info = {'title': title, 'text':text}
        mars_news.append(news_info)

    mars['news'] = mars_news

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # print('opening site')
    browser.visit(url)
    time.sleep(5)
    # print('finding button')
    button = browser.find_by_id("full_image")
    # print(button)
    button.click()
    # print('clicked')
    time.sleep(5)
    # print('finding link')
    button2 = browser.find_link_by_partial_text('more info')
    button2.click()
    # print('clicked link')
    time.sleep(5)
    html = browser.html
    img_soup = BeautifulSoup(html, "html.parser")
    # print(img_soup.prettify())

    picture = img_soup.find('img', class_='main_image').get('src')
    # print(picture)
    base_image_url = 'https://www.jpl.nasa.gov'
    featured_image_url = base_image_url + picture
    # print(featured_image_url)
    time.sleep(2)
    mars['featured_image'] = featured_image_url
    
    
    url = "https://twitter.com/marswxreport?lang=en"
    # print('opening site')
    browser.visit(url)
    time.sleep(5)
    # print('finding tweet')
    # button = browser.find_by_id("stream-items-id")
    # print(button)
    # button.click()
    # print('clicked')
    # time.sleep(5)
    html = browser.html
    twitter_soup = BeautifulSoup(html, "html.parser")
    # print(twitter_soup.prettify())

    # mars_weather = twitter_soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text.strip()
    mars_weather = twitter_soup.find('div', class_='js-tweet-text-container').p.text.strip()
    # print(mars_weather)
    time.sleep(2)
    mars['weather'] = mars_weather
    
    url = "http://space-facts.com/mars/"
    # print('opening site')
    browser.visit(url)
    time.sleep(5)
    # print('scraping table')
    df = pd.read_html(url)
    df = df[0]
    df.columns = ['item', 'fact']
    mars_facts_table = df.to_html()
    # print(mars_facts_table)
    mars['facts'] = mars_facts_table

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemisphere_image_urls = []
    # print('opening site')
    browser.visit(url)
    time.sleep(5)
    # print('parsing images')
    html = browser.html
    hemi_soup = BeautifulSoup(html, "html.parser")

    content= hemi_soup.findAll("div", class_='description')
    # print(element.prettify())
    # print(len(content))
    for i in range(0,len(content)):
        title =  content[i].find('h3').get_text()
        link = content[i].find('a')
        base_url = 'https://astropedia.astrogeology.usgs.gov/'
        suffix = '.tif/full.jpg'
        full_url=base_url+link['href']+suffix
        full_url = full_url.replace('search/map', 'download')
        image_info = {'title': title, 'link':full_url}
        hemisphere_image_urls.append(image_info)
    mars['hemi_pics'] = hemisphere_image_urls

    return mars
