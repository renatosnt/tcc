import pandas as pd
import re
import os

def process_mission_labels(df, mission_col_name):
    """
    Processa a coluna de texto das missões para criar colunas binárias (0 ou 1) para cada missão.
    """
    # Garante que a coluna de missão seja uma string para evitar erros
    missions_text = df[mission_col_name].astype(str)
    
    # Extrai todos os dígitos da string para cada linha
    mission_numbers_list = missions_text.apply(lambda x: re.findall(r'(\d)', x))
    
    # Cria uma coluna para cada missão (M1 a M6)
    for i in range(1, 7):
        mission_label = f'M{i}'
        df[mission_label] = mission_numbers_list.apply(lambda nums: 1 if str(i) in nums else 0)
        
    return df

def main():
    """
    Função principal para criar o Golden Dataset a partir de um arquivo CSV rotulado.
    """
    print("Iniciando a criação do Golden Dataset (a partir do CSV rotulado)...")
    
    # 1. Carregar os dados rotulados do arquivo CSV
    labeled_data_path = os.path.join('data', 'processed', 'rotulados.csv')
    if not os.path.exists(labeled_data_path):
        print(f"ERRO: Arquivo de dados rotulados não encontrado em '{labeled_data_path}'")
        return
        
    df_labels = pd.read_csv(labeled_data_path)
    print(f"{len(df_labels)} registros rotulados foram carregados de '{labeled_data_path}'.")

    # 2. Processar a coluna de texto das missões para criar os rótulos binários
    df_labels = process_mission_labels(df_labels, 'Missões da Nova Indústria Brasil')
    
    # Renomeia a coluna 'Organização' para corresponder ao dataset original
    df_labels = df_labels.rename(columns={'Organização': 'nome_organizacao'})
    
    # 3. Carregar o dataset original completo para obter as outras features
    original_data_path = os.path.join('data', 'processed', 'df_executores.csv')
    if not os.path.exists(original_data_path):
        print(f"ERRO: Dataset original não encontrado em '{original_data_path}'")
        return
        
    df_original = pd.read_csv(original_data_path)
    print(f"Dataset original com {len(df_original)} empresas carregado.")

    # 4. Preparar para a junção (merge)
    # Criamos chaves de junção normalizadas para evitar problemas com maiúsculas/minúsculas ou espaços
    # Mantemos o nome original em uma coluna separada para a verificação de erros
    df_labels['nome_organizacao_original_rotulada'] = df_labels['nome_organizacao'] 
    df_labels['join_key'] = df_labels['nome_organizacao'].str.lower().str.strip()
    df_original['join_key'] = df_original['nome_organizacao'].str.lower().str.strip()

    # Seleciona as colunas relevantes do df_original para evitar duplicatas
    cols_to_merge = ['join_key', 'descricao_organizacao', 'segmento_atuacao', 'tecnologias_disruptivas', 'fase_negocio']
    
    # 5. Juntar os datasets
    # Usamos um 'left merge' para manter todas as empresas do dataset rotulado
    # e trazer as informações do dataset original.
    df_golden = pd.merge(df_labels, df_original[cols_to_merge], on='join_key', how='left')
    
    # Verificar se alguma empresa rotulada não foi encontrada no arquivo original
    unmatched_rows = df_golden[df_golden['descricao_organizacao'].isnull()]
    if not unmatched_rows.empty:
        print(f"\nAVISO: {len(unmatched_rows)} empresas rotuladas não foram encontradas no CSV original.")
        print("Verifique os nomes abaixo ou possíveis inconsistências:")
        
        unmatched_names = unmatched_rows['nome_organizacao_original_rotulada'].tolist()
        print("\n--- Empresas não encontradas ---")
        for name in unmatched_names:
            print(f"- {name}")
        print("------------------------------\n")


    # 6. Limpar o DataFrame final
    # Remove colunas intermediárias e desnecessárias
    df_golden = df_golden.drop(columns=['join_key', 'Missões da Nova Indústria Brasil', 'nome_organizacao_original_rotulada'])
    
    # Renomeia as colunas de missão para o formato final
    mission_map = {
        'M1': 'M1_Agro', 'M2': 'M2_Saude', 'M3': 'M3_Infra_Mobilidade',
        'M4': 'M4_Transformacao_Digital', 'M5': 'M5_Bioeconomia_Energia', 'M6': 'M6_Defesa_Soberania'
    }
    df_golden = df_golden.rename(columns=mission_map)
    
    # 7. Salvar o Golden Dataset
    output_dir = os.path.join('data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'golden_dataset.csv')
    
    df_golden.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print("-" * 50)
    print("Golden Dataset criado com sucesso!")
    print(f"Arquivo salvo em: '{output_path}'")
    print(f"Total de empresas no Golden Dataset: {len(df_golden)}")


if __name__ == "__main__":
    main()
