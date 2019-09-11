# the location and name of this file is going to change!
import requests
import time
from pprint import pprint
from bs4 import BeautifulSoup


username = input("username: ")
password = input("password: ")
payload = {'_username': username, '_password': password}
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
    return title, massage, contents


def get_page(url_s, url, url_2=None):
    sess = requests.Session()
    sess.post(url_s, data=payload, headers=headers)
    time.sleep(0.1)
    request_data = sess.get(url, headers=headers)
    if url_2:
        request_data_2 = sess.get(url_2, headers=headers)
        formatting(request_data.content)
        return formatting(request_data.content), formatting(request_data_2.content)
    else:
        return formatting(request_data.content)


plan_1, plan_2 = get_page('https://gymherderschule.de/iserv/login_check', 'https://gymherderschule.de/iserv/infodisplay/file/23/infodisplay/0/SchuelerOnline/subst_001.htm', 'https://gymherderschule.de/iserv/infodisplay/file/23/infodisplay/0/SchuelerOnline/subst_002.htm')

print("First Plan: \n")
pprint(plan_1)
print("\n\n")
print("Second Plan: \n")
pprint(plan_2)
print("\n\n")
