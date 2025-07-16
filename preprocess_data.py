# Arquivo: preprocess_data.py (versão atualizada)

import json
import re
import pandas as pd
from pathlib import Path

# 1. DEFINIÇÃO DO MAPA DE RENOMEAÇÃO (sem alterações)
RENAME_MAP = {
  # ... (mapa completo como antes) ...
  "Cadastro aprovado?": "cadastro_aprovado",
  "Você concorda em divulgar as informações inseridas neste formulário em estudos sobre o ecossistema de inovação de Minas Gerais e na plataforma do SIMI?": "autorizacao_divulgacao",
  "Qual o nome da sua organização?": "nome_organizacao",
  "Em qual cidade está a sede da organização?": "cidade_sede",
  "Em qual estado (UF) está a sede da organização?": "uf_sede",
  "Qual o link com o logo da organização?": "logo_url",
  "Descrição da organização": "descricao_organizacao",
  "Qual o site da organização?": "site_organizacao",
  "Qual o melhor e-mail para contato?": "email_contato",
  "Em qual categoria sua organização se enquadra?": "categoria_organizacao",
  "Qual fase de investimentos que está captando?": "fase_investimento_busca",
  "Qual(is) incentivo(s) fiscal(is) o município possui para o desenvolvimento de empresas de base tecnológica?": "incentivos_fiscais_municipio",
  "Qual departamento (secretaria, subsecretaria, diretoria, assessoria, etc) é responsável pela pauta/temática de Ciência, Tecnologia e Inovação?": "orgao_responsavel_cti",
  "Qual o tipo de organização?": "tipo_organizacao",
  "Caso sua organização possua um setor ou pessoa responsável por divulgação científica, informe o contato": "contato_divulgacao_cientifica",
  "A organização possui um NIT (Núcleo de Inovação Tecnológica) ou departamento responsável por propriedade intelectual e transferências tecnológicas?": "possui_nit",
  "Quais são as principais áreas do conhecimento em que a organização possui expertise?": "areas_expertise",
  "Qual a tese de investimento da organização?": "tese_investimento",
  "Em quantas startups a organização já investiu?": "num_startups_investidas",
  "Segmento": "segmento_atuacao",
  "Programas de desenvolvimento": "programas_desenvolvimento",
  "Modelo de negócio": "modelo_negocio",
  "Tecnologia disruptiva": "tecnologias_disruptivas",
  "Segmentação de clientes": "segmentacao_clientes",
  "Fase de negócio": "fase_negocio",
  "Número de funcionários": "numero_funcionarios",
  "Fase de investimentos captada/fornecida": "fase_investimento_captada",
  "Está buscando investimento?": "busca_investimento",
  "Linkedin": "linkedin_url",
  "Preferência relativa ao perfil/segmento": "preferencia_segmento",
  "Benefícios dados pelo programa": "beneficios_programa",
  "Investimento médio por startup": "investimento_medio_startup",
  "Exige equity?": "exige_equity",
}

def preprocess_simi_data():
    """
    Lê os dados brutos do SIMI de um arquivo .js, corrige o formato,
    renomeia as colunas e salva como um arquivo CSV processado.
    """
    # 2. DEFINIÇÃO DOS CAMINHOS DOS ARQUIVOS (sem alterações)
    input_path = Path("data/raw/simi_data.js")
    output_path = Path("data/processed/simi_data_processed.csv")
    debug_path = Path("data/processed/debug_corrected_text.json")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Lendo dados brutos de: {input_path}")
    
    # 3. LEITURA E CORREÇÃO DO ARQUIVO (SEÇÃO ATUALIZADA)
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # --- INÍCIO DAS NOVAS CORREÇÕES ---
    # Passo 3.1: Proteger as quebras de linha estruturais (depois de vírgulas)
    # Isso mantém a formatação geral do JSON.
    text_no_newlines = raw_text.replace(',\n', '<COMMA_NEWLINE>')
    text_no_newlines = text_no_newlines.replace('},\n', '}<COMMA_NEWLINE>')
    
    # Passo 3.2: Remover as quebras de linha restantes, que agora são as problemáticas dentro das strings.
    # Também removemos o caractere de tabulação (\t) que pode causar problemas.
    text_no_newlines = text_no_newlines.replace('\n', ' ').replace('\t', ' ')

    # Passo 3.3: Restaurar as quebras de linha estruturais.
    corrected_text = text_no_newlines.replace('<COMMA_NEWLINE>', ',\n')
    # --- FIM DAS NOVAS CORREÇÕES ---
    
    # Passo 3.4: Aplicar a correção de chaves sem aspas (solução anterior)
    corrected_text = re.sub(r'\b([a-zA-Z_][\w]*)\b:', r'"\1":', corrected_text)
    
    # Passo de depuração: Salvar o texto corrigido para inspeção manual
    with open(debug_path, 'w', encoding='utf-8') as f:
        f.write(corrected_text)
    print(f"Arquivo de depuração salvo em: {debug_path}")

    # 4. CARREGAMENTO DOS DADOS PARA O PANDAS (sem alterações)
    try:
        data = json.loads(corrected_text)
        df = pd.DataFrame(data)
        print("Dados carregados com sucesso em um DataFrame.")
    except json.JSONDecodeError as e:
        print(f"\n--- ERRO! O JSON AINDA É INVÁLIDO ---")
        print(f"Erro ao decodificar: {e}")
        print(f"Verifique o arquivo '{debug_path}' na linha/coluna indicada pelo erro.")
        print("Causas comuns: aspas ( \" ) não escapadas dentro de um valor de texto.")
        return

    # O restante do script (5 e 6) permanece o mesmo...
    # 5. RENOMEAÇÃO DAS COLUNAS
    original_cols = set(df.columns)
    map_keys = set(RENAME_MAP.keys())
    unmapped_cols = original_cols - map_keys
    if unmapped_cols:
        print("\nAtenção! As seguintes colunas não foram encontradas no mapa e não serão renomeadas:")
        for col in unmapped_cols:
            print(f"- {col}")
    
    df.rename(columns=RENAME_MAP, inplace=True)
    print("\nColunas renomeadas com sucesso.")

    # 6. SALVANDO O ARQUIVO PROCESSADO EM CSV
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nDados processados e salvos com sucesso em: {output_path}")

if __name__ == "__main__":
    preprocess_simi_data()