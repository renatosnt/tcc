import json

# Caminho do arquivo JSON
caminho_arquivo = 'artigos_universidade_federal_de_minas_gerais.json'

# Abrir e carregar o conteúdo do JSON
with open(caminho_arquivo, 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Verifica se é uma lista e imprime o tamanho
if isinstance(dados, list):
    print(f'Tamanho do array: {len(dados)}')
else:
    print('O conteúdo do JSON não é um array de objetos.')
