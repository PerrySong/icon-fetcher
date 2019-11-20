import requests
from bs4 import BeautifulSoup
import urllib
import ssl



# use this image scraper from the location that
# you want to save scraped images to

ssl._create_default_https_context = ssl._create_unverified_context


def get_image_url(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    app_icon_divs = soup.find("div", attrs={'class', 'app-icon'})
    # print('skill main divs = ', app_icon_divs.find("img")['src'], 'type = ' + str(type(app_icon_divs)))
    image_link = 'https://img.icons8.com/bubbles/2x/question-mark.png'
    if app_icon_divs and app_icon_divs.find("img") and app_icon_divs.find("img")['src']:
      image_link = app_icon_divs.find("img")['src']	
    return image_link


def fetch_image(link, filename):
    urllib.request.urlretrieve(link, filename)


def get_request_link(skill):
    return 'https://icons8.com/icons/set/' + skill

if __name__ == '__main__':
    path = input('enter file path: ')
    f = open(path, 'r')
    skills = f.readlines()
    for skill in skills:
        skill = skill.strip().replace('/', '\\')
        link = get_request_link(skill)
        image_url = get_image_url(link)
        print('fetching image from url: ', image_url, 'for skill: ' + skill)
        fetch_image(image_url, 'icons/' + skill + '.png')