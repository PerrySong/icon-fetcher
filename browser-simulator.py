from selenium import webdriver
import time
from bs4 import BeautifulSoup
import urllib
import ssl

def load_stackshare_page(length):
    browser = webdriver.Chrome()
    browser.get('https://stackshare.io/tools/top')
    for i in range(length):
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
    divs = soup.findAll("div", attrs={'class', 'trending-wrapper'})
    # print(divs)
    f = open('name-to-uri.json', 'w+')
    f.write('[\n')
    for div in divs:

        print("dev = ", div)
        img_url = div.find("img")['src']
        name = div.find("span")
        # category = div.find("span", attrs={'itemprop', 'applicationSubCategory'})
        img_type = img_url.split('.')[-1]
        file_name = name.contents[0] + '.' + img_type

        try:
            fetch_image(img_url, file_name)
        except Exception:
            pass

        f.write('\"' + file_name + '\",\n')

    f.write(']\n')

if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    content = load_stackshare_page(1)
    soup = BeautifulSoup(content, "html.parser")
    fetch_images(soup)
