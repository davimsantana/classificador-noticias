import requests
import time
import logging

logging.basicConfig(level=logging.INFO)

from bs4 import BeautifulSoup
from .base_collector import BaseCollector

class G1Collector(BaseCollector):
    API_BASE_URL = "https://falkor-cda.bastian.globo.com/tenants/g1/instances/{}/posts/page/{}"

    def __init__(self):
        super().__init__("G1")
        self.total_urls = 0

    def extract_text(self, soup):
        news_body = soup.select_one('div.mc-article-body')
        text_parts = []

        if not news_body:
            logging.warning("Classe pai 'mc-article-body' não encontrada na matéria.")
            return None
            
        text_elements = news_body.select('p.content-text__container')

        if text_elements:
            for paragraph in text_elements:
                text_parts.append(paragraph.get_text(strip=True))
            
            text = ' '.join(text_parts)

            # print(f"     -> Texto da matéria: \n ' {text} '")
            return text

    def extract_title(self, soup):
        title_element = soup.select_one('.content-head__title')

        if title_element:
            title_text = title_element.get_text(strip=True)
           # logging.info(f"     -> Título matéria: {title_text}")

            return title_text
        
    def discover_max_pages(self, target_categories):
        for category, category_id in target_categories.items():
            
            logging.info(f"--- VERIFICANDO MÁXIMO DE PÁGINAS DA CATEGORIA {category} ---")

            page = 1
            MAX_PAGES_SAFEGUARD = 300

            while page <= MAX_PAGES_SAFEGUARD:
            
                api_url = self.API_BASE_URL.format(category_id, page)

                page_json = self.download_and_convert_json(api_url)

                if not page_json:
                    continue

                items = page_json.get('items', [])

                if not items:
                    break

                page += 1

            logging.info(f"     -> Quantidade de páginas para {category}: {page - 1}.")
    
    def collect_news(self, target_categories, pages_per_category=50):
        collected_data = []

        for category, category_id in target_categories.items():
            
            logging.info(f"--- EXTRAINDO NOTÍCIAS DA CATEGORIA {category} ---")

            for page in range(1, pages_per_category + 1):
                api_url = self.API_BASE_URL.format(category_id, page)

                page_json = self.download_and_convert_json(api_url)

                if not page_json:
                    continue

                items = page_json.get('items', [])

                if not items:
                    logging.info(f"     -> Página {page} vazia. Fim da categoria {category}.")
                    break
                
                logging.info(f"     -> Página {page}:")

                for item in items:
                    item_type = item.get('type')

                    if item_type != "materia":
                        continue

                    news_url = item.get('content', {}).get('url')

                    if news_url:
                        soup = self.extract_page(news_url)

                        if soup:
                            title = self.extract_title(soup)
                            text = self.extract_text(soup)
                            
                            if title and text:
                                collected_data.append({
                                    'categoria': category, 
                                    'url': news_url, 
                                    'title': title, 
                                    'text': text
                                })
                                
                                self.total_urls += 1

                            if not title:
                                logging.info(f"     -> Título não encontrado. URL: {news_url}")
                            elif not text:
                                logging.info(f"     -> Texto não encontrado. URL: {news_url}")
                                
                            

        logging.info(f'TOTAL DE URLS EXTRAÍDAS: {self.total_urls}')
        return collected_data

    
