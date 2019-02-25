# Splinter, Beautiful soup dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def init_browser():
    # Splinter browser
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    

def scrape():
    browser = init_browser()
    mars_data = {}

    # news scraping mars_data{'headline','article'}
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    latest_news = soup.find('li','slide')

    mars_data['headline'] = latest_news.find(class_='content_title').text
    mars_data['article'] = latest_news.find(class_='article_teaser_body').text

    # space images mars_data{'featured_image'}
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.find_by_id('full_image').click()
    html = browser.html
    soup = bs(html, 'html.parser')

    button = soup.find(id='full_image').attrs
    part_url = button['data-link']

    button_url = 'https://www.jpl.nasa.gov' + part_url
    browser.visit(button_url)
    
    html = browser.html
    soup = bs(html, 'html.parser')

    link = soup.find_all(class_='download_tiff')
    featured_image_url = link[1].find('a')['href']

    mars_data['featured_image'] = featured_image_url

    # twitter weather mars_data{'mars_weather'}
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    tweets = soup.find_all('div', class_='tweet', attrs={"data-name": "Mars Weather"})

    pressure = 'pressure'

    for x in range(len(tweets)):
        tweet_text = tweets[x].find_all('p')
        weather_dirty = tweet_text[0].contents
        mars_weather = weather_dirty[0].replace('\n',' ')
        if pressure in mars_weather:
            break

    mars_data['mars_weather'] = mars_weather

    # space facts table mars_data{'table'}
    url = 'https://space-facts.com/mars/'
    
    table = pd.read_html(url)
    df = table[0]
    df_new = df.set_index([0])
    df_new.index.names = [None]
    df_rename = df_new.rename(columns={0:'Description',1:'Data'})
    html_table = df_rename.to_html()

    mars_data['table'] = html_table
    
    browser.quit()

    return mars_data



