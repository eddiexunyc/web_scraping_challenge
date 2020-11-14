from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    mar_dicts = {}
    mar_url = "https://mars.nasa.gov/news/"
    mar_pic_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    mar_fact_url = "https://space-facts.com/mars/"
    mar_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    #mars new URL page to be scraped
    browser = init_browser()
    browser.visit(mar_url)
    soup = BeautifulSoup(browser.html, "html.parser")
    new_article = soup.find_all('div', class_ = "list_text")

    for new in new_article[:1]:
        new_title = new.find('div', class_ = 'content_title').text
        new_para = new.find('div', class_ = 'article_teaser_body').text
    
    #mars image URL page to be scraped
    browser.visit(mar_pic_url)
    soup = BeautifulSoup(browser.html, "html.parser")
    mar_image_path = soup.find_all('img')[3]["src"]
    image_url = "https://www.jpl.nasa.go" + mar_image_path

    #mars fact URL page to be scraped
    mar_table = pd.read_html(mar_fact_url)
    mar_df = mar_table[0]
    mar_df.columns = ["Description", "Value"]
    mar_df_table = mar_df.to_html()

    #mars hemisphere URL to be scraped
    browser.visit(mar_hemisphere_url)
    soup = BeautifulSoup(browser.html, "html.parser")
    mar_hemi_image_urls = []
    mar_article = soup.find_all('div', class_ = "item")
    for hemi in mar_article:
        mar_content = hemi.find('div', class_ = 'description')
        mar_title = mar_content.h3.text
        hemi_link = hemi.a['href']
        hemi_url = 'https://astrogeology.usgs.gov' + hemi_link
        browser.visit(hemi_url)
        soup = BeautifulSoup(browser.html, 'html.parser')
        hemi_image_link = soup.find('div', class_ = 'downloads')
        hemi_image_url = hemi_image_link.find('li').a['href']
        hemi_dict = {}
        hemi_dict['title'] = mar_title
        hemi_dict['img_url'] = hemi_image_url
        mar_hemi_image_urls.append(hemi_dict)
    
    mar_dicts = {
        'new_title': new_title,
        'new_para': new_para,
        'image': image_url,
        'table': str(mar_df_table),
        'hemisphere_images': mar_hemi_image_urls
        }

    return mar_dicts



    
