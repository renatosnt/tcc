import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report
# A biblioteca sentence-transformers é a peça central desta nova abordagem.
from sentence_transformers import SentenceTransformer

# --- CONFIGURAÇÃO ---
GOLDEN_DATASET_PATH = os.path.join('data', 'processed', 'golden_dataset.csv')
TEXT_FEATURES = ['nome_organizacao', 'descricao_organizacao', 'segmento_atuacao', 'tecnologias_disruptivas']
TARGET_LABELS = ['M1_Agro', 'M2_Saude', 'M3_Infra_Mobilidade', 'M4_Transformacao_Digital', 'M5_Bioeconomia_Energia', 'M6_Defesa_Soberania']
TEST_SET_SIZE = 0.2
RANDOM_STATE = 42
MODEL_PIPELINE_PATH = os.path.join('reports', 'model_v4_embeddings.joblib')

# MUDANÇA: Trocamos por um modelo de ponta, especificamente treinado para embeddings semânticos.
# Este modelo é multilíngue e muito eficaz para tarefas como a nossa.
EMBEDDING_MODEL_NAME = 'paraphrase-multilingual-mpnet-base-v2'


def load_and_prepare_data(filepath):
    """Carrega o Golden Dataset e prepara os dados."""
    if not os.path.exists(filepath):
        print(f"ERRO: Golden Dataset não encontrado em '{filepath}'")
        return None, None
    df = pd.read_csv(filepath)
    print(f"Golden Dataset carregado com sucesso. {len(df)} linhas encontradas.")
    for col in TEXT_FEATURES:
        df[col] = df[col].fillna('')
    df['combined_text'] = df[TEXT_FEATURES].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    
    # Prepara os textos e os rótulos
    texts = df['combined_text'].tolist()
    labels = df[TARGET_LABELS].values
    
    return texts, labels, df

def main():
    """
    Função principal que orquestra o pipeline de treinamento com embeddings semânticos.
    """
    print(f"Iniciando o pipeline de treinamento do modelo v4 (Embeddings Semânticos)...")
    
    # 1. Carregar os dados
    texts, labels, df = load_and_prepare_data(GOLDEN_DATASET_PATH)
    if texts is None: return

    # 2. Gerar os Embeddings Semânticos
    # A classe SentenceTransformer carrega o modelo pré-treinado.
    # O download do modelo (aprox. 1.1GB) ocorrerá automaticamente na primeira vez.
    print(f"Carregando o modelo de embedding '{EMBEDDING_MODEL_NAME}'...")
    print("Isso pode demorar e fará o download de um modelo grande na primeira execução.")
    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    
    print("Gerando embeddings para todos os textos... (Isso pode levar alguns minutos)")
    # O método encode() transforma a lista de textos em uma matriz de vetores numéricos.
    X_embeddings = embedding_model.encode(texts, show_progress_bar=True)
    print("Embeddings gerados com sucesso.")

    # 3. Dividir os dados (agora com embeddings) em treino e teste
    # 'y' são os rótulos que carregamos anteriormente.
    X_train, X_test, y_train, y_test = train_test_split(
        X_embeddings, labels, test_size=TEST_SET_SIZE, random_state=RANDOM_STATE
    )
    print(f"Dados divididos em {len(X_train)} para treino e {len(X_test)} para teste.")

    # 4. Treinar o classificador
    # Voltamos para a Regressão Logística, que foi nosso modelo mais equilibrado.
    # A complexidade agora está nos embeddings, não no classificador.
    print("Treinando o classificador sobre os embeddings...")
    classifier = MultiOutputClassifier(
        LogisticRegression(class_weight='balanced', solver='liblinear', random_state=RANDOM_STATE)
    )
    classifier.fit(X_train, y_train)
    print("Treinamento concluído.")

    # 5. Fazer previsões e avaliar
    y_pred = classifier.predict(X_test)

    print("\n--- Relatório de Classificação do Modelo v4.1 (Embeddings Otimizados) ---\n")
    report = classification_report(
        y_test, 
        y_pred, 
        target_names=TARGET_LABELS, 
        zero_division=0
    )
    print(report)
    
    # 6. Salvar o classificador treinado para uso futuro
    os.makedirs(os.path.dirname(MODEL_PIPELINE_PATH), exist_ok=True)
    joblib.dump(classifier, MODEL_PIPELINE_PATH)
    print(f"\nModelo classificador treinado salvo em '{MODEL_PIPELINE_PATH}'")
    print("Para usar o modelo, você precisará gerar embeddings para novos dados e depois usar este classificador.")

if __name__ == "__main__":
    main()
