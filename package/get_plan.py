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
    return title, massage, contents


def get_page(payload, url_s, url, url_2=None):
    sess = requests.Session()
    sess.post(url_s, data=payload, headers=headers)
    time.sleep(0.1)
    request_data = sess.get(url, headers=headers)
    if url_2:
        request_data_2 = sess.get(url_2, headers=headers)
        title, massage, contents = formatting(request_data.content)
        first = [title, massage, contents]
        title, massage, contents = formatting(request_data_2.content)
        secound = [title, massage, contents]
        return first, secound
    else:
        title, massage, contents = formatting(request_data.content)
        first = [title, massage, contents]
        return first

