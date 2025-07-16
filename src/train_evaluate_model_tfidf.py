import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
# NLTK é uma biblioteca popular para processamento de linguagem natural.
# Usaremos ela para obter uma lista de stop words em português.
import nltk
from nltk.corpus import stopwords

# --- CONFIGURAÇÃO ---
# ATUALIZADO: Apontando para o nosso novo dataset com os dados do batch 2 integrados.
GOLDEN_DATASET_PATH = os.path.join('data', 'processed', 'golden_dataset.csv')
TEXT_FEATURES = ['nome_organizacao', 'descricao_organizacao', 'segmento_atuacao', 'tecnologias_disruptivas']
TARGET_LABELS = ['M1_Agro', 'M2_Saude', 'M3_Infra_Mobilidade', 'M4_Transformacao_Digital', 'M5_Bioeconomia_Energia', 'M6_Defesa_Soberania']
TEST_SET_SIZE = 0.2
RANDOM_STATE = 42 # Para reprodutibilidade dos resultados
MODEL_PIPELINE_PATH = os.path.join('reports', 'model_pipeline_v2_final.joblib')

def download_nltk_resources():
    """Verifica e baixa os recursos necessários do NLTK."""
    try:
        stopwords.words('portuguese')
    except LookupError:
        print("Baixando recursos do NLTK (stopwords)...")
        nltk.download('stopwords')

def load_and_prepare_data(filepath):
    """
    Carrega o Golden Dataset, trata valores nulos e combina as colunas de texto.
    """
    if not os.path.exists(filepath):
        print(f"ERRO: Golden Dataset não encontrado em '{filepath}'")
        return None, None, None

    df = pd.read_csv(filepath)
    print(f"Golden Dataset carregado com sucesso. {len(df)} linhas encontradas.")
    
    # Preenche valores NaN (nulos) nos campos de texto com uma string vazia
    for col in TEXT_FEATURES:
        df[col] = df[col].fillna('')
        
    # Combina as colunas de texto em um único campo para ser usado como feature
    df['combined_text'] = df[TEXT_FEATURES].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    
    X = df['combined_text']
    # Garante que as colunas de target existem antes de selecioná-las
    y = df[[col for col in TARGET_LABELS if col in df.columns]]
    
    return X, y, df

def main():
    """
    Função principal que orquestra o pipeline de treinamento e avaliação.
    """
    print("Iniciando o pipeline de treinamento e avaliação do modelo v2 (balanceado) com dados aumentados...")
    
    # Garante que os recursos do NLTK estão disponíveis
    download_nltk_resources()
    portuguese_stopwords = stopwords.words('portuguese')

    # 1. Carregar e preparar os dados
    X, y, df = load_and_prepare_data(GOLDEN_DATASET_PATH)
    if X is None:
        return

    # 2. Dividir os dados em conjuntos de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SET_SIZE, random_state=RANDOM_STATE
    )
    print(f"Dados divididos em {len(X_train)} para treino e {len(X_test)} para teste.")

    # 3. Construir o pipeline do Scikit-learn (Modelo v2)
    print("Construindo o pipeline do modelo...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words=portuguese_stopwords, ngram_range=(1, 2), max_features=3000)),
        ('clf', MultiOutputClassifier(LogisticRegression(solver='liblinear', class_weight='balanced', random_state=RANDOM_STATE)))
    ])
    
    # 4. Treinar o modelo
    print("Treinando o modelo...")
    pipeline.fit(X_train, y_train)
    print("Treinamento concluído.")

    # 5. Fazer previsões no conjunto de teste
    y_pred = pipeline.predict(X_test)

    # 6. Avaliar a performance e gerar o relatório
    print("\n--- Relatório de Classificação do Modelo v2 (com dados aumentados) ---\n")
    report = classification_report(
        y_test, 
        y_pred, 
        target_names=list(y.columns), 
        zero_division=0
    )
    print(report)
    
    # 7. Salvar o modelo final
    os.makedirs(os.path.dirname(MODEL_PIPELINE_PATH), exist_ok=True)
    joblib.dump(pipeline, MODEL_PIPELINE_PATH)
    print(f"\nModelo salvo em '{MODEL_PIPELINE_PATH}'")
    print("--------------------------------------------------------------------")
    print("\nCompare este resultado com o da primeira execução do modelo v2.")
    print("O objetivo é ver uma melhora nos scores F1 das classes que foram aumentadas.")

if __name__ == "__main__":
    main()
