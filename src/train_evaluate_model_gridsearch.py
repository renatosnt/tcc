import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import nltk
from nltk.corpus import stopwords

# --- CONFIGURAÇÃO ---
GOLDEN_DATASET_PATH = os.path.join('data', 'processed', 'golden_dataset.csv')
TEXT_FEATURES = ['nome_organizacao', 'descricao_organizacao', 'segmento_atuacao', 'tecnologias_disruptivas']
TARGET_LABELS = ['M1_Agro', 'M2_Saude', 'M3_Infra_Mobilidade', 'M4_Transformacao_Digital', 'M5_Bioeconomia_Energia', 'M6_Defesa_Soberania']
TEST_SET_SIZE = 0.2
RANDOM_STATE = 42
MODEL_PIPELINE_PATH = os.path.join('reports', 'model_pipeline_v3.joblib')

def download_nltk_resources():
    """Verifica e baixa os recursos necessários do NLTK."""
    try:
        stopwords.words('portuguese')
    except LookupError:
        print("Baixando recursos do NLTK (stopwords)...")
        nltk.download('stopwords')

def load_and_prepare_data(filepath):
    """Carrega o Golden Dataset e prepara os dados."""
    if not os.path.exists(filepath):
        print(f"ERRO: Golden Dataset não encontrado em '{filepath}'")
        return None, None, None
    df = pd.read_csv(filepath)
    print(f"Golden Dataset carregado com sucesso. {len(df)} linhas encontradas.")
    for col in TEXT_FEATURES:
        df[col] = df[col].fillna('')
    df['combined_text'] = df[TEXT_FEATURES].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    X = df['combined_text']
    y = df[TARGET_LABELS]
    return X, y, df

def main():
    """
    Função principal que orquestra o pipeline de treinamento com otimização.
    """
    print("Iniciando o pipeline de treinamento do modelo v3 (RandomForest + GridSearchCV)...")
    download_nltk_resources()
    portuguese_stopwords = stopwords.words('portuguese')

    # 1. Carregar e preparar os dados
    X, y, df = load_and_prepare_data(GOLDEN_DATASET_PATH)
    if X is None: return

    # 2. Dividir os dados em conjuntos de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SET_SIZE, random_state=RANDOM_STATE
    )
    print(f"Dados divididos em {len(X_train)} para treino e {len(X_test)} para teste.")

    # 3. Construir o pipeline com o RandomForestClassifier
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words=portuguese_stopwords)),
        ('clf', MultiOutputClassifier(RandomForestClassifier(class_weight='balanced', random_state=RANDOM_STATE)))
    ])

    # 4. Definir o Grid de Hiperparâmetros para o GridSearchCV
    # GridSearchCV irá testar todas as combinações destes parâmetros para encontrar a melhor.
    # A sintaxe 'nome_etapa__parametro' é como acessamos os parâmetros dentro do pipeline.
    parameters = {
        'tfidf__ngram_range': [(1, 1), (1, 2)], # Testa apenas unigramas vs. unigramas e bigramas
        'tfidf__max_features': [2000, 3000],      # Testa diferentes tamanhos de vocabulário
        'clf__estimator__n_estimators': [100, 200], # Testa número de "árvores" na floresta
        'clf__estimator__max_depth': [None, 10],   # Testa profundidade das árvores
    }
    
    # 5. Configurar e executar o GridSearchCV
    # scoring='f1_weighted': Otimiza para o F1-score ponderado, bom para datasets desbalanceados.
    # cv=3: Validação cruzada com 3 folds.
    # n_jobs=-1: Usa todos os processadores disponíveis para acelerar a busca.
    grid_search = GridSearchCV(pipeline, parameters, cv=3, n_jobs=-1, verbose=2, scoring='f1_weighted')
    
    print("\nIniciando a busca por hiperparâmetros (GridSearchCV)...")
    print("Isso vai levar um tempo considerável. Por favor, aguarde.")
    grid_search.fit(X_train, y_train)

    # 6. Exibir os melhores parâmetros encontrados
    print("\nBusca concluída!")
    print("Melhores parâmetros encontrados pelo GridSearchCV:")
    print(grid_search.best_params_)

    # 7. Avaliar o melhor modelo encontrado
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)

    print("\n--- Relatório de Classificação do Modelo v3 (Otimizado) ---\n")
    report = classification_report(
        y_test, 
        y_pred, 
        target_names=TARGET_LABELS, 
        zero_division=0
    )
    print(report)
    
    # 8. Salvar o melhor modelo para uso futuro
    os.makedirs(os.path.dirname(MODEL_PIPELINE_PATH), exist_ok=True)
    joblib.dump(best_model, MODEL_PIPELINE_PATH.replace('_v2', '_v3'))
    print(f"\nMelhor modelo salvo em '{MODEL_PIPELINE_PATH.replace('_v2', '_v3')}'")

if __name__ == "__main__":
    main()
