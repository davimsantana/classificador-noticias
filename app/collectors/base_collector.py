import requests
import time
import random
import logging

logging.basicConfig(level=logging.INFO)

from config import DELAY_RANGE
from bs4 import BeautifulSoup 

class BaseCollector:
    def __init__(self, font_name):
        self.font_name = font_name
        logging.info(f"--- INICIANDO COLETOR: {font_name} ---")

    def delay(self):
        time.sleep(random.uniform(*DELAY_RANGE))

    def extract_page(self, news_url):
        try:
            response = requests.get(news_url)
            response.raise_for_status()

            self.delay()

            return BeautifulSoup(response.content, 'lxml')
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na requisição {e}")
            return None
    
    def download_and_convert_json(self, url):
        try: 
            response = requests.get(url)
            response.raise_for_status()

            self.delay()
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao converter resposta em JSON: {e}")
            return None

        return response.json()
    
    def collect_news(self, target_categories):
        raise NotImplementedError("Cada coletor deve implementar o método 'collect_news'.")
    
    #def extract_news_text(self, news_url):
        #raise NotImplementedError("Cada coletor deve implementar o método 'extract_news_text'.")



