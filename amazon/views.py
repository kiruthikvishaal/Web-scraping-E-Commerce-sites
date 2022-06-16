from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from json import dumps

def get_url_amazon(search_term):
    """Generate url from search term"""
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')
    url = template.format(search_term)
    url+='&page()'
    return url
def extract_record(item):
    """Extract and return data from a single record"""
    #description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')

    #price
    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
        k = price[1::]
        k = k.replace(",","")
        k = (float)(k)
        p = round(k*73,2)
    except AttributeError:
        return
    #rank and rating
    try:
        rating = item.i.text
        #review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
    except AttributeError:
        rating=''
       # review_count=''
    try:
        img_url = item.find('img',{'class':'s-image'})
        img = img_url['src']
    except:
        url="NO URL FOUND"
    result = (description,p,rating,url,img)
    return result
# Create your views here.
#FLIPKART SITE
def get_url(search_item):
   # This function fetches the URL of the item that you want to search
    template = 'https://www.flipkart.com/search?q={}&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_1_4_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_1_4_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=mobile+phones&requestId=e625b409-ca2a-456a-b53c-0fdb7618b658&as-backfill=on'
    search_item = search_item.replace(" ","+")
    # Add term query to URL
    url = template.format(search_item)
    # Add term query placeholder
    url += '&page{}'
    return url

def extract_phone_model_info(item):
    """
    This function extracts model, price, ram, storage, stars , number of ratings, number of reviews,
    storage expandable option, display option, camera quality, battery , processor, warranty of a phone model at flipkart
    """
    #num_ratings = item.find('span',{'class':"_2_R_DZ"}).text.replace('\xa0&\xa0'," ; ")[0:item.find('span',{'class':"_2_R_DZ"}).text.replace('\xa0&\xa0'," ; ").find(';')].strip()
    #price = item.find('div',{'class':'_30jeq3 _1_WHN1'}).text
    try:
        name = item.find('div', attrs={'class': '_4rR01T'}).text
    except AttributeError:
        name = 'Name Not Found'
    try:
        price = item.find('div',class_='_30jeq3 _1_WHN1').text
        k=price[1::]
        k = k.replace(",", "")
        k= (float)(k)
    except AttributeError:
        return
    try:
        rating = item.find('div', attrs={'class': '_3LWZlK'}).text
    except AttributeError:
        rating = ''
    
    pro_url = "https://www.flipkart.com"+item['href']
    img = item.find('img', attrs={'class': '_396cs4 _3exPp9'})
    img = img['src']
    result = (name,k,rating,pro_url,img)
    return result

def get_url_pen(search_item):
   # This function fetches the URL of the item that you want to search
    template = 'https://www.flipkart.com/search?q={}&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_1_4_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_1_4_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=mobile+phones&requestId=e625b409-ca2a-456a-b53c-0fdb7618b658&as-backfill=on'
    search_item = search_item.replace(" ","+")
    # Add term query to URL
    url = template.format(search_item)
    # Add term query placeholder
    url += '&page{}'
    return url

def extract_phone_model_info_pen(item):
    """
    This function extracts model, price, ram, storage, stars , number of ratings, number of reviews,
    storage expandable option, display option, camera quality, battery , processor, warranty of a phone model at flipkart
    """
    #num_ratings = item.find('span',{'class':"_2_R_DZ"}).text.replace('\xa0&\xa0'," ; ")[0:item.find('span',{'class':"_2_R_DZ"}).text.replace('\xa0&\xa0'," ; ").find(';')].strip()
    #price = item.find('div',{'class':'_30jeq3'}).text
    try:
        name = item.find('a', attrs={'class': 's1Q9rs'}).text
    except AttributeError:
        name = 'Name Not Found'
    try:
        price = item.find('div',class_='_30jeq3').text
        k = price[1::]
        k=price[1::]
        k = k.replace(",", "")
        k= (float)(k)
    except AttributeError:
        return
    try:
        rating = item.find('div', attrs={'class': '_3LWZlK'}).text
    except AttributeError:
        rating = ''
    pro_url = item.find('a', attrs={'class': 's1Q9rs'})
    pro_url = "https://www.flipkart.com"+pro_url['href']
    img = item.find('img', attrs={'class': '_396cs4 _3exPp9'})
    img = img['src']
    result = (name,k,rating,pro_url,img)
    return result

def home(request):
    #path = "C:/Users/KIRUTHIK VISHAAL S/web scrpaing/chromedriver.exe"
    #driver = webdriver.Chrome(executable_path=path)
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome("C:/Users/KIRUTHIK VISHAAL S/web scrpaing/chromedriver.exe",options=option)
    records = []
    #url = get_url_amazon('ultrawide monitor')
    url = get_url_amazon('camera')
    for page in range(1,2):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # to store unqiue characteristics of the product
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
    driver.close()

    #----------------------------------------------------
    #FLIPKART SITE
    #----------------------------------------------------
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome("C:/Users/KIRUTHIK VISHAAL S/web scrpaing/chromedriver.exe",options=option)
    list1 = ['camera','refrigirator']
    z = 'camera'
    flag=0
    if z in list1:
        flag=1
    else:
        flag=2
    if flag==1:
        url = get_url(z)
        for page in range(1,2):
            driver.get(url.format(page))
            soup = BeautifulSoup(driver.page_source,'html.parser')
            results = soup.find_all('a',{'class':"_1fQZEK"})
        for item in results:
            records.append(extract_phone_model_info(item))
        driver.close()
    else:
        url = get_url_pen(z)
        for page in range(1,2):
            driver.get(url.format(page))
            soup = BeautifulSoup(driver.page_source,'html.parser')
            results = soup.find_all('div',{'class':"_4ddWXP"})
        for item in results:
            records.append(extract_phone_model_info_pen(item))
        driver.close()
    
    records.sort(key=lambda x:x[1])
    return render(request, "home.html", {'movies': records})