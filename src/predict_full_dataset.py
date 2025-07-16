import pandas as pd
import os
import joblib
from sentence_transformers import SentenceTransformer

# --- CONFIGURAÇÃO ---
# Caminho para o dataset completo que queremos classificar
FULL_DATASET_PATH = os.path.join('data', 'processed', 'df_executores.csv')

# Caminho para o nosso melhor classificador treinado (que foi treinado sobre os embeddings)
CLASSIFIER_MODEL_PATH = os.path.join('reports', 'model_v4_embeddings.joblib')

# Nome do modelo de embedding que foi usado no treinamento (deve ser o mesmo)
EMBEDDING_MODEL_NAME = 'paraphrase-multilingual-mpnet-base-v2'

# Caminho para o arquivo de saída com a classificação final
FINAL_OUTPUT_PATH = os.path.join('reports', 'classificacao_final_bert.csv')

# As features de texto e os nomes dos rótulos devem ser os mesmos do treinamento
TEXT_FEATURES = ['nome_organizacao', 'descricao_organizacao', 'segmento_atuacao', 'tecnologias_disruptivas']
TARGET_LABELS = ['M1_Agro', 'M2_Saude', 'M3_Infra_Mobilidade', 'M4_Transformacao_Digital', 'M5_Bioeconomia_Energia', 'M6_Defesa_Soberania']


def predict_full_dataset():
    """
    Carrega o modelo treinado com embeddings e o utiliza para classificar o dataset completo.
    """
    print("Iniciando a classificação do dataset completo com o modelo BERT...")

    # --- Etapa 1: Carregar os modelos ---
    try:
        # Carrega o classificador (e.g., Regressão Logística) que foi treinado
        classifier = joblib.load(CLASSIFIER_MODEL_PATH)
        print(f"Classificador carregado com sucesso de '{CLASSIFIER_MODEL_PATH}'.")
        
        # Carrega o modelo de embedding da biblioteca SentenceTransformer
        print(f"Carregando o modelo de embedding '{EMBEDDING_MODEL_NAME}'...")
        embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print("Modelo de embedding carregado.")
        
    except FileNotFoundError as e:
        print(f"ERRO: Arquivo de modelo não encontrado: {e}")
        print("Por favor, execute o script 'train_evaluate_model_v4.py' primeiro.")
        return

    # --- Etapa 2: Carregar e preparar o dataset completo ---
    try:
        df_full = pd.read_csv(FULL_DATASET_PATH)
        print(f"Dataset completo com {len(df_full)} empresas carregado.")
    except FileNotFoundError:
        print(f"ERRO: Dataset completo não encontrado em '{FULL_DATASET_PATH}'.")
        return

    # Prepara o campo de texto combinado, assim como foi feito no treino
    for col in TEXT_FEATURES:
        df_full[col] = df_full[col].fillna('')
    texts_to_predict = df_full[TEXT_FEATURES].apply(lambda row: ' '.join(row.values.astype(str)), axis=1).tolist()

    # --- Etapa 3: Gerar Embeddings para o dataset completo ---
    print("\nGerando embeddings para todo o dataset... (Isso pode levar alguns minutos)")
    X_embeddings_full = embedding_model.encode(texts_to_predict, show_progress_bar=True)
    print("Embeddings gerados com sucesso.")

    # --- Etapa 4: Fazer as previsões usando o classificador ---
    print("Realizando previsões...")
    y_pred_full = classifier.predict(X_embeddings_full)
    print("Previsões concluídas.")

    # --- Etapa 5: Integrar as previsões e salvar o resultado ---
    df_predictions = pd.DataFrame(y_pred_full, columns=TARGET_LABELS)
    df_final = pd.concat([df_full.reset_index(drop=True), df_predictions.reset_index(drop=True)], axis=1)
    
    # Cria uma coluna de resumo para facilitar a leitura humana
    df_final['missoes_previstas'] = df_final[TARGET_LABELS].apply(
        lambda row: ', '.join([mission.replace('_', ' ') for mission, assigned in row.items() if assigned]),
        axis=1
    )
    
    os.makedirs(os.path.dirname(FINAL_OUTPUT_PATH), exist_ok=True)
    df_final.to_csv(FINAL_OUTPUT_PATH, index=False, encoding='utf-8-sig')

    print("-" * 50)
    print("Processo finalizado com sucesso!")
    print(f"O arquivo com a classificação completa de todas as empresas foi salvo em: '{FINAL_OUTPUT_PATH}'")

if __name__ == "__main__":
    predict_full_dataset()
