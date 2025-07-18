import pandas as pd
import os

print("Iniciando script de enriquecimento de dados...")

# --- 1. Definir os Caminhos ---
# Caminhos relativos à localização do script (dentro da pasta 'scripts')
JSON_COMPLETO_PATH = './data/processed/simi_data.json'
PASTA_REPORTS = './reports/'

# Lista dos arquivos CSV que queremos enriquecer
arquivos_csv_para_enriquecer = [
    'classificacao_final_revisada.csv',
    'base_conhecimento_pd.csv',
    'demais_organizacoes.csv'
]

# --- 2. Carregar o DataFrame "Fonte da Verdade" (o JSON) ---
try:
    # O JSON parece ser uma lista de registros (dicionários)
    df_fonte = pd.read_json(JSON_COMPLETO_PATH, orient='records')
    print(f"Fonte de dados '{os.path.basename(JSON_COMPLETO_PATH)}' carregada. Contém {df_fonte.shape[0]} registros e {df_fonte.shape[1]} colunas.")
except Exception as e:
    print(f"ERRO ao carregar o arquivo JSON: {e}")
    exit() # Interrompe o script se não conseguir carregar a fonte principal

# Selecionar apenas as colunas que queremos adicionar, mais a chave de junção.
# Isso evita duplicar colunas que já existem no CSV.
colunas_fonte = list(df_fonte.columns)
# Vamos remover colunas que já sabemos que estão no CSV para evitar conflitos no merge
colunas_para_evitar_duplicar = ['descricao_organizacao', 'categoria_organizacao', 'segmento_atuacao', 'tecnologias_disruptivas', 'fase_negocio']
colunas_para_adicionar = [col for col in colunas_fonte if col not in colunas_para_evitar_duplicar or col == 'nome_organizacao']
df_fonte_selecionada = df_fonte[colunas_para_adicionar]


# --- 3. Fazer o Loop, Enriquecer e Salvar cada CSV ---
for nome_arquivo in arquivos_csv_para_enriquecer:
    caminho_csv = os.path.join(PASTA_REPORTS, nome_arquivo)
    print(f"\nProcessando arquivo: {nome_arquivo}...")
    
    try:
        df_alvo = pd.read_csv(caminho_csv)
    except FileNotFoundError:
        print(f"-> AVISO: Arquivo '{nome_arquivo}' não encontrado. Pulando.")
        continue

    # A mágica acontece aqui: pd.merge()
    # Usamos 'how="left"' para garantir que todas as organizações do nosso CSV
    # de alvo sejam mantidas, mesmo que não encontrem uma correspondência no JSON.
    df_enriquecido = pd.merge(
        left=df_alvo,                 # O DataFrame que queremos enriquecer
        right=df_fonte_selecionada,    # O DataFrame com as colunas extras
        on='nome_organizacao',       # A coluna chave para a junção
        how='left'                   # Tipo de junção
    )

    # Sobrescreve o arquivo CSV original com a versão enriquecida
    df_enriquecido.to_csv(caminho_csv, index=False)
    
    print(f"-> Sucesso! '{nome_arquivo}' foi atualizado. Novas dimensões: {df_enriquecido.shape[0]} linhas, {df_enriquecido.shape[1]} colunas.")

print("\nProcesso de enriquecimento concluído com sucesso!")