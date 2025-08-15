import pandas as pd
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV

import spacy
import nltk
from nltk.corpus import stopwords

class Trainer:
    def __init__(self):
        print("Trainer Criado")
        self.nlp = spacy.load("pt_core_news_sm", disable=["parser", "ner"])
        self.stopwords = self.load_stopwords()

    def load_stopwords(self):
        try:
            return stopwords.words('portuguese')
        except LookupError:
            print("Baixando a lista de stopwords do NLTK...")
            nltk.download('stopwords')
            return stopwords.words('portuguese')
        
    def _preprocess_text(self, text):
        text = re.sub(r'[^\w\s]', '', text.lower())
        doc = self.nlp(text)

        lemmatized_tokens = [token.lemma_ for token in doc if token.text not in self.stopwords]
        
        return " ".join(lemmatized_tokens)

    def train_and_rate(self, df):
        """
        Recebe um DataFrame, executa a limpeza, treinamento e avaliação,
        e retorna o pipeline do modelo treinado.
        """
        print("\n--- INICIANDO PRÉ-PROCESSAMENTO E TREINAMENTO ---")
        
        df['texto_completo'] = df['title'] + ' ' + df['text']
        print("Aplicando Lematizacão nos textos...")
        df['texto_completo'] = df['texto_completo'].apply(self._preprocess_text)
        print("Lematizacão finalizada.")

        X = df['texto_completo']
        y = df['categoria']

        X_treino, X_teste, y_treino, y_teste = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        print(f"Dados divididos: {len(X_treino)} para treino, {len(X_teste)} para teste.")

        pipeline = Pipeline([
            ('vetorizador', TfidfVectorizer(
                ngram_range=(1, 3),        
                sublinear_tf=True,                        
            )),
            ('classificador', LinearSVC(
                class_weight='balanced',
                random_state=42                    
            ))
        ])
        
        
        params_grid = {
            'vetorizador__max_features': [10000, 15000, 20000],
            'vetorizador__min_df': [3],
            'vetorizador__max_df': [0.9], 
            'classificador__C': [0.01, 0.1, 1],
            'classificador__max_iter': [3000]
        }

        grid_search = GridSearchCV(pipeline, params_grid, cv=5, n_jobs=-1, verbose=2)
     
        print("Iniciando a busca pelos melhores hiperparâmetros (GridSearchCV)...")
        
        grid_search.fit(X_treino, y_treino)

        print("\nMelhores parâmetros encontrados:")
        print(grid_search.best_params_)

        print("\n--- AVALIAÇÃO DO MODELO OTIMIZADO ---")
        previsoes = grid_search.predict(X_teste)
        acuracia = accuracy_score(y_teste, previsoes)
        print(f"Acurácia no conjunto de teste: {acuracia * 100:.2f}%")
        print("\nRelatório de Classificação:")
        print(classification_report(y_teste, previsoes))

        return grid_search.best_estimator_

        """ 
        print("\n[INFO 2] Matriz de Confusão:")
        categorias_ordenadas = grid_search.classes_
        matriz_confusao = confusion_matrix(y_teste, previsoes, labels=categorias_ordenadas)

        plt.figure(figsize=(12, 10))
        sns.heatmap(matriz_confusao, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=categorias_ordenadas, yticklabels=categorias_ordenadas)
        plt.title('Matriz de Confusão')
        plt.xlabel('Categoria Prevista')
        plt.ylabel('Categoria Verdadeira')
        plt.savefig('reports/matriz_confusao.png')
        plt.show()
        print("-> Matriz de confusão salva como 'matriz_confusao.png'")

        print("\n[INFO 3] Exemplos de Classificações Incorretas:")
        df_analise = pd.DataFrame({'texto_completo': X_teste, 'verdadeiro': y_teste, 'previsto': previsoes})
        erros = df_analise[df_analise['verdadeiro'] != df_analise['previsto']]
        
        print("\nExemplos de 'economia' classificados como outra coisa:")
        print(erros[erros['verdadeiro'] == 'economia'].head())

        print("\nExemplos de 'mundo' classificados como outra coisa:")
        print(erros[erros['verdadeiro'] == 'mundo'].head())

        erros.to_csv('reports/erros_de_classificacao.csv', index=False)
        print("\n-> Todos os erros foram salvos em 'erros_de_classificacao.csv'")
      """
    