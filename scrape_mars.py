
# coding: utf-8

# In[3]:


#Dependencies
from bs4 import BeautifulSoup as bs
import requests
import urllib.request
from splinter import Browser
import pandas as pd


# In[4]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[5]:


#Scrape the NASA news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')


# In[6]:


#scrape first article
article = soup.find('li', class_='slide')


# In[11]:


news_title = article.find('h3').text
news_p = article.find('div', class_='article_teaser_body').text
news_p


# In[8]:


#Scrape for image
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


# In[9]:


browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')


# In[15]:


img = soup.find('article', class_='carousel_item')
featured_image_url = 'https://www.jpl.nasa.gov' + img['style'].split("'")[1]


# In[16]:


#scrape the Mars weather Twitter
url = 'https://twitter.com/marswxreport?lang=en'


# In[17]:


browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')


# In[19]:


mars_weather = soup.find('p', class_='tweet-text').text
mars_weather


# In[29]:


#scrape Mars facts
url = 'http://space-facts.com/mars/'


# In[30]:


table = pd.read_html(url)
html_table = table[0].to_html()
html_table


# In[31]:


#Scrape USGS Astrogeology site for high resolution images for Mars' hemispheres
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# In[32]:


browser.visit(url)


# In[33]:


hemisphere_image_urls = []
hemispheres = ['Cerberus Hemisphere','Schiaparelli Hemisphere',
               'Syrtis Major Hemisphere','Valles Marineris Hemisphere']
for h in hemispheres:
    browser.click_link_by_partial_text(h)
    html = browser.html
    soup = bs(html, 'html.parser')
    img_url = soup.findAll('dd')[1].find('a')['href']
    hemisphere_image_urls.append({'title':h, 'img_url':img_url})
    browser.click_link_by_partial_text('Back')
    print('Done Scraping')
    return {'news_title':news_title, 'news_p':news_p, 
    'featured_image_url':featured_image_url, 'mars_weather':mars_weather,
    'html_table':html_table, 'hemisphere_image_urls':hemisphere_image_urls}
