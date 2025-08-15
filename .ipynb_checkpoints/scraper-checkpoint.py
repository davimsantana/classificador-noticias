import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

CATEGORIES = {
    'economia':      'https://g1.globo.com/rss/g1/economia/',
    'saude':         'https://g1.globo.com/rss/g1/saude/',
    'educacao':      'https://g1.globo.com/rss/g1/educacao/',
    'mundo':         'https://g1.globo.com/rss/g1/mundo/',
    'politica':      'https://g1.globo.com/rss/g1/politica/',
    'meio ambiente': 'https://g1.globo.com/rss/g1/meio-ambiente',
    'pop-arte':      'https://g1.globo.com/rss/g1/pop-arte',
    'tecnologia':    'https://g1.globo.com/rss/g1/tecnologia',
    'turismo':       'https://g1.globo.com/rss/g1/turismo-e-viagem',
    'curiosidades':  'https://g1.globo.com/rss/g1/olha-que-legal'
}

news_data = []
total_categories = len(CATEGORIES)

print("--- INICIANDO LEITOR DE NOTÍCIAS RSS ---")

for category, url_feed in CATEGORIES.items():
    print(f"\n[+] Lendo feed da categoria: {category.upper()}")

    try:

        response = requests.get(url_feed)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'xml')

        items = soup.find_all('item')
        print(f"  -> Encontrados {len(items)} itens no feed.")

        for item in items:
            title = item.find('title').text.strip()
            link  = item.find('link').text.strip()

            description_html = item.find('description').text.strip()
            description_soup = BeautifulSoup(description_html, 'html.parser')

            description_text = description_soup.get_text(separator=" ", strip=True)

            news_data.append({
                'categoria':   category,
                'title':       title,
                'link':        link,
                'description': description_text
            })
    except requests.exceptions.RequestException as e:
        print(f"ERRO AO ACESSAR FEED -> {url_feed}: {e}")
        continue

print("\n--- CONSULTA FINALIZADA ---")
print(f"Total de notícias extraídas: {len(news_data)}")


print("\nSalvando dados...")

df = pd.DataFrame(news_data)
df.to_csv('noticias.csv', index=False, encoding="utf-8")

print("Dados salvos com sucesso!")
