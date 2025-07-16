import pandas as pd
import numpy as np
import os
import joblib # Usado para salvar e carregar o modelo treinado

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
import nltk
from nltk.corpus import stopwords

# --- CONFIGURAÇÃO (deve ser idêntica à do script de treino) ---
GOLDEN_DATASET_PATH = os.path.join('data', 'processed', 'golden_dataset.csv')
TEXT_FEATURES = ['nome_organizacao', 'descricao_organizacao', 'segmento_atuacao', 'tecnologias_disruptivas']
TARGET_LABELS = ['M1_Agro', 'M2_Saude', 'M3_Infra_Mobilidade', 'M4_Transformacao_Digital', 'M5_Bioeconomia_Energia', 'M6_Defesa_Soberania']
TEST_SET_SIZE = 0.2
RANDOM_STATE = 42
MODEL_PIPELINE_PATH = os.path.join('reports', 'model_pipeline_v2.joblib')

def download_nltk_resources():
    """Verifica e baixa os recursos necessários do NLTK."""
    try:
        stopwords.words('portuguese')
    except LookupError:
        print("Baixando recursos do NLTK (stopwords)...")
        nltk.download('stopwords')

def load_and_prepare_data(filepath):
    """Carrega e prepara os dados, exatamente como no script de treino."""
    if not os.path.exists(filepath):
        print(f"ERRO: Golden Dataset não encontrado em '{filepath}'")
        return None, None, None
    df = pd.read_csv(filepath)
    for col in TEXT_FEATURES:
        df[col] = df[col].fillna('')
    df['combined_text'] = df[TEXT_FEATURES].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    X = df['combined_text']
    y = df[TARGET_LABELS]
    return X, y, df

def train_and_save_pipeline_if_not_exists(X_train, y_train):
    """Treina e salva o pipeline se ele ainda não existir."""
    if os.path.exists(MODEL_PIPELINE_PATH):
        print(f"Carregando modelo existente de '{MODEL_PIPELINE_PATH}'...")
        return joblib.load(MODEL_PIPELINE_PATH)

    print("Modelo não encontrado. Treinando e salvando um novo modelo...")
    portuguese_stopwords = stopwords.words('portuguese')
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words=portuguese_stopwords, ngram_range=(1, 2), max_features=3000)),
        ('clf', MultiOutputClassifier(LogisticRegression(solver='liblinear', class_weight='balanced', random_state=RANDOM_STATE)))
    ])
    pipeline.fit(X_train, y_train)
    
    os.makedirs(os.path.dirname(MODEL_PIPELINE_PATH), exist_ok=True)
    joblib.dump(pipeline, MODEL_PIPELINE_PATH)
    print(f"Modelo salvo em '{MODEL_PIPELINE_PATH}'.")
    return pipeline

def main():
    """
    Função principal que carrega o modelo, faz previsões e analisa os erros.
    """
    print("Iniciando a análise de erros do modelo...")
    download_nltk_resources()
    X, y, df = load_and_prepare_data(GOLDEN_DATASET_PATH)
    if X is None:
        return

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SET_SIZE, random_state=RANDOM_STATE
    )

    # Garante que o modelo esteja treinado e salvo
    pipeline = train_and_save_pipeline_if_not_exists(X_train, y_train)

    # Faz previsões no conjunto de teste
    y_pred_array = pipeline.predict(X_test)
    
    # Cria um DataFrame com os resultados para fácil comparação
    df_results = df.loc[X_test.index].copy()
    df_results['prediction_text'] = X_test
    
    for i, label in enumerate(TARGET_LABELS):
        df_results[f'true_{label}'] = y_test.iloc[:, i]
        df_results[f'pred_{label}'] = y_pred_array[:, i]

    # Compara o array de rótulos verdadeiros com o de previsões
    # np.any(y_test.values != y_pred_array, axis=1) retorna True para linhas com qualquer erro
    error_mask = np.any(y_test.values != y_pred_array, axis=1)
    df_errors = df_results[error_mask]
    
    print(f"\n--- Análise de {len(df_errors)} Erros de Classificação Encontrados ---\n")

    for index, row in df_errors.iterrows():
        print(f"Empresa: {row['nome_organizacao']}")
        
        true_labels = [label for label in TARGET_LABELS if row[f'true_{label}'] == 1]
        pred_labels = [label for label in TARGET_LABELS if row[f'pred_{label}'] == 1]
        
        print(f"  - Rótulo Correto...: {true_labels if true_labels else ['Nenhuma']}")
        print(f"  - Previsão do Modelo: {pred_labels if pred_labels else ['Nenhuma']}")
        print("-" * 50)


if __name__ == "__main__":
    main()

