from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import logging
import sys
import time

logger = logging.getLogger(__name__)
logging.FileHandler('logfile.log')
logging.basicConfig(filename='logfile.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')


class SelRequest:

    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=self.options)
        self.source = ''

    def get_source(self, url):
        logger.info(f'getting URL = {url}')
        start = time.time()
        self.driver.get(url)
        end = time.time()
        logger.debug(f'driver.get() took {end-start} s.')
        start = time.time()
        self.driver.execute_script("return document.body.innerHTML")
        end = time.time()
        logger.debug(f'driver.execute_script() took {end - start} s.')
        start = time.time()
        source = self.driver.page_source
        end = time.time()
        logger.debug(f'driver.page_source took {end - start} s.')
        # self.driver.close()
        end = time.time()
        logger.debug(f'source obtained in {end-start}')
        return source

    def get_olx_stats(self, source):
        soup = BeautifulSoup(source, "html.parser")
        span = soup.find_all('a', {'class': 'css-pyvavn'})
        for i in span:
            print(i.contents)
        # this is how span looks like:
        # [<a class="css-pyvavn" href="/d/nieruchomosci/mieszkania/wynajem/boleslawiec">Wynajem<span class="css-wz88">15</span></a>,
        # <a class="css-pyvavn" href="/d/nieruchomosci/mieszkania/sprzedaz/boleslawiec">Sprzedaż<span class="css - wz88">35</span></a>,
        # <a class="css-pyvavn" href="/d/nieruchomosci/mieszkania/zamiana/boleslawiec">Zamiana<span class="css-wz88">1</span></a>]

        # this is how span.contents looks like:
        # ['Wynajem', < span class ="css-wz88" > 15 < / span >]
        # ['Sprzedaż', < span class ="css-wz88" > 35 < / span >]
        # ['Zamiana', < span class ="css-wz88" > 1 < / span >]

        # this is how contents[1].string looks like:
        # 15
        # 35
        # 1
        lookfor = ["Wynajem", "Sprzedaż", "Zamiana"]
        stat = []
        for ad_type in lookfor:
            value = '0'
            for content in span:
                if content.contents[0].string == ad_type:
                    value = content.contents[1].string
                    # print(value)
            try:
                stat.append(int(value))
            except ValueError:
                stat.append(int(value.replace(u'\xa0', u'')))
        logger.info(f'found data: {stat}')
        print(stat)
        return stat















# lookfor = ["Wynajem", "Sprzedaż", "Zamiana"]
# stat = []
# for i in lookfor:
#     value = '0'
#     for el in span:
#         if str(el).find(i) > 0:
#             value = str(el)[str(el).find('>', str(el).find(i) + 20) + 1:str(el).find('<', str(el).find(i) + 20)]
#
# logger.info(f'found data: {stat}')
# lookfor = ["Wynajem", "Sprzedaż", "Zamiana"]
# stat = []
# for i in lookfor:
#     value = '0'
#     for el in span:
#         if str(el[0]).find(i) > 0:
#             a = i.contents[1].string
#
#     try:
#         stat.append(int(value))
#     except ValueError:
#         stat.append(int(value.replace(u'\xa0', u'')))
# logger.info(f'found data: {stat}')
# sys.exit()
# return stat


# link = 'https://www.olx.pl/d/nieruchomosci/mieszkania/lubin/'
#
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#
# driver.get(link)
# innerHTML = driver.execute_script("return document.body.innerHTML")
# sc =
# driver.close()
#
# soup = BeautifulSoup(sc, "html.parser")
# # print(soup.prettify())
# span = soup.find_all('a', {'class': 'css-pyvavn'})
#
# print(span)
