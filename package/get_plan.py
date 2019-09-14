# the location and name of this file is going to change!
import requests
import time
import re
from pprint import pprint
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'}


def soup(file):
    return BeautifulSoup(file, "html.parser")


def formatting(source):
    raw_list = soup(source).find(class_="mon_list")
    contents = soup(str(raw_list)).get_text(separator="|")
    raw_title = soup(source).find(class_="mon_title")
    title = soup(str(raw_title)).get_text(separator="|")
    raw_massage = soup(source).find(class_="info")
    massage = soup(str(raw_massage)).get_text(separator="")
    contents = re.split("\n", contents)
    return [title, massage, contents]


def get_page(payload, url_s, url_today, url_tomorow):
    sess = requests.Session()
    sess.post(url_s, data=payload, headers=headers)
    time.sleep(0.1)
    request_data_today = sess.get(url_today, headers=headers)
    request_data_tomorow = sess.get(url_tomorow, headers=headers)
    content_today = formatting(request_data_today.content)
    content_tomorow = formatting(request_data_tomorow.content)
    return [content_today, content_tomorow]

