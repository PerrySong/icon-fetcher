from selenium import webdriver
import time
from bs4 import BeautifulSoup
import urllib
import ssl
import sys
import json

if len(sys.argv) <= 1:
    print('please enter an argument to describe how many pages you want to scrape.')
    exit(0)

pages = int(sys.argv[1])

def load_stackshare_page(length):
    browser = webdriver.Chrome()
    browser.get('https://stackshare.io/tools/top')
    for _ in range(length):
        time.sleep(1)
        try:
            browser.find_element_by_class_name('trending-tab-load-more-services').click()
        except Exception:
            pass

    return browser.page_source

def fetch_image(link, filename):
    print('saving image to ' + filename)
    urllib.request.urlretrieve(link, 'stackshare-icons/' + filename)

def fetch_images(soup):
    divs = soup.findAll("div", {'class': 'trending-wrapper'})
    # print(divs)
    img_list = []
    for div in divs:

        print("dev = ", div)
        img_url = div.find("img")['src']
        name = div.find("span").contents[0]
        sub_category = div.find("span", {'itemprop': 'applicationSubCategory'}).contents[0].strip()
        description = div.find("div", {'class': 'trending-description'}).contents[0].strip()

        img_type = img_url.split('.')[-1]
        file_name = name + '.' + img_type
        print("category = ",  sub_category)
        print("description = ", description)
        img_list.append({'name': name, 'url': img_url, 'file_name': file_name, 'sub_category': sub_category, 'description': description})

        try:
            fetch_image(img_url, file_name)
        except Exception:
            pass
    f = open('stackshare-icons-meta-data.json', 'w+')
    f.write(json.dumps(img_list))
    f.flush()
    f.close()

if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    content = load_stackshare_page(pages)
    soup = BeautifulSoup(content, "html.parser")
    fetch_images(soup)
