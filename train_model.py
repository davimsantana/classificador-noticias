from app.trainer import Trainer
import pandas as pd
import joblib


df = pd.read_csv("data/noticias_completas.csv")

if not df.empty:
    try:
        print("--- INICIANDO TREINAMENTO ---")
        trainer = Trainer()
        final_model = trainer.train_and_rate(df)

        joblib.dump(final_model, 'models/news_classifier_v1.0.pkl')

        print("--- TREINO FINALIZADO ---")
    except Exception as e:
        print("ERRO AO EXECUTAR TREINO DO MODELO")
        print(e)