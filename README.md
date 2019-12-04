# Mission to Mars

Web application that scrapes image and text data from NASA about Mars

## Web scraping

Using beautiful soup and splinter, information about Mars is pulled from NASA, twitter and spacefacts.com. 
Sample code from scrape_mars.py:

```python
# news scraping mars_data{'headline','article'}
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    latest_news = soup.find('li','slide')

    mars_data['headline'] = latest_news.find(class_='content_title').text
    mars_data['article'] = latest_news.find(class_='article_teaser_body').text
```

## Flask app

Using flask to connect to the stored data in a Mongo database, two routes are available in the app:
- home route ('/') which pulls the existing Mars facts from the database
- scrape route ('/scrape') which runs the webscraping code and updates the database
