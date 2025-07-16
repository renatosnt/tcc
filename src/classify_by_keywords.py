# -*- coding: utf-8 -*-
"""
Script para classificação de organizações com base nas 6 Missões da Nova Indústria Brasil.

Autor: Dr. Rafael Cortez (Assistente de IA)
Data: 27 de Junho de 2025
Versão: 4.0 (Saída alterada para JSON)

Metodologia:
Este script utiliza uma abordagem de linha de base (baseline) baseada em dicionários de
palavras-chave. Para cada uma das 6 missões, um conjunto de termos relevantes foi definido.
O script analisa os campos textuais de cada organização (`descricao_organizacao`,
`segmento_atuacao`, `tecnologias_disruptivas`) e atribui uma ou mais missões se
palavras-chave correspondentes forem encontradas.

Este método é:
- Rápido: Permite uma classificação inicial de todo o dataset sem a necessidade de modelos complexos.
- Interpretável: As razões para a classificação de uma empresa são transparentes e diretamente
  ligadas às palavras-chave encontradas.
- Iterativo: As listas de palavras-chave podem e devem ser refinadas para melhorar a precisão.

Como usar:
1. Certifique-se de ter o arquivo `df_executores.csv` no diretório `data/processed/`.
2. Execute este script a partir da raiz do seu projeto (e.g., `python src/classify_by_keywords.py`).
3. O resultado será salvo em `reports/classificacao_missoes_keywords_v4.json`.
"""

import pandas as pd
import os
import re
import json

# --- CONFIGURAÇÃO ---
# Define os caminhos de entrada e saída com base na estrutura do projeto
INPUT_FILE_PATH = os.path.join('data', 'processed', 'df_executores.csv')
OUTPUT_DIR = 'reports'
OUTPUT_FILE_PATH = os.path.join(OUTPUT_DIR, 'classificacao_missoes_keywords_v4.json')

# Colunas a serem analisadas para a classificação
TEXT_COLUMNS_TO_ANALYZE = [
    'descricao_organizacao',
    'segmento_atuacao',
    'tecnologias_disruptivas'
]

# --- DICIONÁRIO DE PALAVRAS-CHAVE POR MISSÃO (VERSÃO 2.0) ---
# Dicionário expandido com base no feedback do usuário.
# As palavras-chave são convertidas para minúsculas e duplicatas são removidas para consistência.

raw_keywords = {
    "M1_Agro": [
        'agro', 'agronegócio', 'agrícola', 'agricultura', 'pecuária', 'alimentos',
        'fertilizante', 'bioinsumo', 'colheita', 'safra', 'fazenda', 'rural',
        'maquinário agrícola', 'agropecuário', 'agrotech', 'agricultura de precisão',
        'bioinsumos', 'biofertilizantes', 'mecanização agrícola', 'armazenagem de grãos',
        'processamento de alimentos', 'etanol de milho', 'segurança alimentar',
        'rastreabilidade de alimentos', 'cooperativa agroindustrial'
    ],
    "M2_Saude": [
        'saúde', 'medicina', 'farmacêutica', 'biofarma', 'hospital', 'clínica',
        'diagnóstico', 'terapia', 'vacina', 'medicamento', 'sus', 'healthtech',
        'biossinais', 'telemedicina', 'dispositivos médicos', 'e-health', 'exames',
        'biotecnologia', 'ifa', 'vacinas', 'equipamentos médicos',
        'diagnóstico clínico', 'terapias gênicas', 'radiofármacos', 'pdp saúde'
    ],
    "M3_Infra_Mobilidade": [
        'infraestrutura', 'saneamento', 'moradia', 'mobilidade', 'transporte',
        'logística', 'construção civil', 'ferroviário', 'rodoviário', 'urbano',
        'cidades inteligentes', 'smart cities', 'saneamento básico', 'mobilidade elétrica',
        'ônibus elétrico', 'baterias de lítio', 'materiais de construção sustentáveis',
        'energia solar fotovoltaica', 'indústria ferroviária'
    ],
    "M4_Transformacao_Digital": [
        'digital', 'software', 'iot', 'internet das coisas', 'big data', 'analytics',
        'ia', 'inteligência artificial', 'machine learning', 'plataforma',
        'indústria 4.0', 'automação', 'cibersegurança', 'cybersecurity', 'cloud',
        'nuvem', 'ti', 'tecnologia da informação', 'fintech', 'edtech',
        'transformação digital', 'semicondutores', 'chips', 'automação industrial',
        'robótica', 'software as a service', 'saas', 'computação em nuvem',
        'manufatura aditiva', 'gêmeos digitais'
    ],
    "M5_Bioeconomia_Energia": [
        'bioeconomia', 'descarbonização', 'energia renovável', 'transição energética',
        'sustentável', 'meio ambiente', 'crédito de carbono', 'eólica', 'solar',
        'biocombustível', 'hidrogênio verde', 'reciclagem', 'economia circular',
        'esg', 'ambiental', 'energias renováveis', 'créditos de carbono',
        'aço verde', 'biometano', 'saf', 'minerais críticos'
    ],
    "M6_Defesa_Soberania": [
        'defesa', 'soberania', 'aeroespacial', 'segurança', 'militar', 'satélite',
        'radar', 'naval', 'tecnologia dual', 'deftech', 'cyberdefesa', 'aeronáutica',
        'indústria de defesa', 'aviação militar', 'sistemas de armas', 'propulsão', 'nuclear'
    ]
}

# Processa o dicionário para garantir consistência (lowercase, sem duplicatas)
MISSION_KEYWORDS = {
    mission: sorted(list(set([keyword.lower() for keyword in keywords])))
    for mission, keywords in raw_keywords.items()
}


def clean_text(text):
    """
    Função auxiliar para limpar o texto antes da análise.
    Converte para minúsculas e remove caracteres não alfanuméricos.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text) # Remove pontuação
    text = re.sub(r'\s+', ' ', text).strip() # Remove espaços extras
    return text


def classify_organization(row, mission_keywords):
    """
    Classifica uma única organização (uma linha do DataFrame) com base nos dicionários.
    Retorna um dicionário com o resultado da classificação (1 para sim, 0 para não).
    """
    combined_text = ' '.join([str(row.get(col, '')) for col in TEXT_COLUMNS_TO_ANALYZE])
    cleaned_text = clean_text(combined_text)
    classification = {mission: 0 for mission in mission_keywords.keys()}
    
    for mission, keywords in mission_keywords.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', cleaned_text):
                classification[mission] = 1
                break
                
    return classification

def main():
    """
    Função principal que orquestra o processo de carga, classificação e salvamento.
    """
    print("Iniciando o script de classificação por palavras-chave (v4.0)...")

    if not os.path.exists(INPUT_FILE_PATH):
        print(f"ERRO: Arquivo de entrada não encontrado em '{INPUT_FILE_PATH}'")
        return

    # Carrega o dataset a partir do arquivo CSV
    try:
        print(f"Carregando dados do arquivo CSV: {INPUT_FILE_PATH}")
        df = pd.read_csv(INPUT_FILE_PATH)
        print(f"Dataset carregado com sucesso. {len(df)} linhas encontradas.")
    except Exception as e:
        print(f"ERRO: Falha ao carregar ou processar o arquivo CSV. Detalhes: {e}")
        return

    print("Aplicando a lógica de classificação em cada organização...")
    classifications = df.apply(lambda row: classify_organization(row, MISSION_KEYWORDS), axis=1)
    
    classifications_df = pd.DataFrame(list(classifications))
    
    df_final = pd.concat([df, classifications_df], axis=1)
    
    mission_names = list(MISSION_KEYWORDS.keys())
    df_final['missoes_atribuidas'] = df_final[mission_names].apply(
        lambda row: ', '.join([mission.replace('_', ' ') for mission, assigned in row.items() if assigned]),
        axis=1
    )
    print("Classificação concluída.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Salva o resultado em formato JSON
    try:
        df_final.to_json(
            OUTPUT_FILE_PATH,
            orient='records',  # Salva como uma lista de objetos JSON
            indent=4,          # Adiciona indentação para melhor legibilidade
            force_ascii=False  # Garante que caracteres acentuados (e.g., ç, ã) sejam salvos corretamente
        )
        print(f"Resultados salvos com sucesso em formato JSON em '{OUTPUT_FILE_PATH}'")
    except Exception as e:
        print(f"ERRO: Falha ao salvar o arquivo de saída JSON. Detalhes: {e}")

if __name__ == "__main__":
    main()
