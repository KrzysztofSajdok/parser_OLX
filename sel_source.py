from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)
logging.FileHandler('logfile.log')
logging.basicConfig(filename='logfile.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')


class SelRequest:

    def __init__(self, url):
        self.url = url
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=self.options)
        self.source = ''

    def get_source(self):
        self.driver.get(self.url)
        logger.info(f'getting URL = {self.url}')
        self.driver.execute_script("return document.body.innerHTML")
        self.source = self.driver.page_source
        self.driver.close()
        return self.source

    def get_olx_stats(self):
        soup = BeautifulSoup(self.get_source(), "html.parser")
        span = soup.find_all('a', {'class': 'css-pyvavn'})
        lookfor = ["Wynajem", "Sprzedaż", "Zamiana"]
        stat = []
        for i in lookfor:
            a = '0'
            for el in span:
                if str(el).find(i) > 0:
                    a = str(el)[str(el).find('>', str(el).find(i) + 20) + 1:str(el).find('<', str(el).find(i) + 20)]
            try:
                stat.append(int(a))
            except ValueError:
                stat.append(int(a.replace(u'\xa0', u'')))
        logger.info(f'found data: {stat}')
        return stat


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
