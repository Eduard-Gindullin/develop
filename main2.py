from random import randint
from wsgiref import headers
from bs4 import BeautifulSoup
from requests import get as reqt
import json
import tqdm
import time
import user_agent

data = {
    "data":[]
}

def headers():
    headers = dict()
    headers['user-agent'] = 'Mozilla/5.0 (WindowsNT 10.0; Win64; x64) AppleWebKit/537.36'
    return headers
    # 'Host': 'ufa.hh.ru'


#rt = reqt(tor_ports=(9050,), tor_cport=9051)

def parse(url):
    items = list()
    for page in range(1,200):
        print(page)
        page_url = f'https://hh.ru/search/vacancy?text=python+%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA&salary=&clusters=true&no_magic=true&ored_clusters=true&enable_snippets=true&page={page}&hhtmFrom=vacancy_search_list'
        print(url)
        resp = reqt(page_url, headers=headers()) 
        soup = BeautifulSoup(resp.text, "lxml")
        page_items = soup.find_all(class_="vacancy-serp-item-body")
        print(soup)
        if len(page_items)==0:
            #break
            for item_body in page_items:
                link = item_body.find(attrs={"data-qa":"serp-item__title"}) 
                item = {'title':link.text}

                region = item_body.find(attrs={"data-qa":"vacancy-serp__vacancy-adress"})
                item['region'] = region and region.text

                link_resp = reqt(link.attrs['href'], headers=headers())
                soup_item = BeautifulSoup(link_resp.text, "lxml")

                salary = soup_item.find(attrs={"data-qa":"vacancy-salary"})
                item['salary'] = salary and salary.text

                experience = soup_item.find(attrs={"data-qa":"vacancy-experience"})
                item['work experience'] = experience and experience.text

                print(item)
                items.append(item)
                time.sleep(randint(1,3)) 
                print(salary)


 