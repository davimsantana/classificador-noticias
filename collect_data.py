import pandas as pd
from app.collectors.g1_collector import G1Collector
from config import TARGET_CATEGORIES

PAGES_TO_SEARCH = 50 

print("--- INICIANDO PROCESSO DE COLETA GERAL ---")

g1_collector = G1Collector() 

g1_data = g1_collector.collect_news(TARGET_CATEGORIES, pages_per_category=PAGES_TO_SEARCH)

if g1_data:
    print(f"\n--- COLETA FINALIZADA ---")
    print(f"Total de {len(g1_data)} notícias coletadas.")
    
    print("\nSalvando dados em 'noticias_completas.csv'...")
    
    df = pd.DataFrame(g1_data)
    df.to_csv('data/noticias_completas.csv', index=False, encoding='utf-8')
    
    print("Dados salvos com sucesso!")
else:
    print("\n--- COLETA FINALIZADA ---")
    print("Nenhuma notícia foi coletada. Verifique os logs.")