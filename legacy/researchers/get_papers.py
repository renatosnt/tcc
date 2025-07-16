import requests
import time
import json
import os
import time
start_time = time.time()
BASE_PAPER_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
BASE_AUTHOR_URL = "https://api.semanticscholar.org/graph/v1/author/"
DELAY_BETWEEN_REQUESTS = 2
WAIT_ON_429 = 60
DELAY_BETWEEN_INSTITUTIONS = 10  # segundos

CHECKPOINT_PAGES = 5      # Salvar artigos a cada 5 páginas
CHECKPOINT_AUTORES = 20   # Salvar autores a cada 20 coletados
institutions_mg = [
    "Universidade Federal de Minas Gerais",
    "UFMG",
    "Universidade Federal de Uberlândia",
    "UFU",
    "Universidade Federal de Viçosa",
    "UFV",
    "Universidade Federal de Juiz de Fora",
    "UFJF",
    "Universidade Federal de Lavras",
    "UFLA",
    "Universidade Federal de São João del-Rei",
    "UFSJ",
    "Universidade Federal de Itajubá",
    "UNIFEI",
    "Universidade Estadual de Montes Claros",
    "UNIMONTES",
    "Universidade do Estado de Minas Gerais",
    "UEMG",
    "Centro Federal de Educação Tecnológica de Minas Gerais",
    "CEFET-MG",
    "Instituto Federal de Educação, Ciência e Tecnologia de Minas Gerais",
    "IFMG",
    "Instituto Federal do Sudeste de Minas Gerais",
    "IF Sudeste MG",
    "Instituto Federal do Norte de Minas Gerais",
    "IFNMG",
    "Instituto Federal do Triângulo Mineiro",
    "IFTM",
    "Instituto Federal de Ciência e Tecnologia do Sul de Minas Gerais",
    "IF Sul de Minas",
    "Fundação Oswaldo Cruz - Fiocruz Minas",
    "Fundação Ezequiel Dias",
    "Centro de Desenvolvimento da Tecnologia Nuclear - CDTN",
    "Centro de Desenvolvimento Tecnológico em Saúde - CDTS",
    "Instituto de Ciências Exatas - ICE UFMG",
    "Fundação de Amparo à Pesquisa do Estado de Minas Gerais",
    "FAPEMIG",
    "Fundação Centro Tecnológico de Minas Gerais",
    "CETEC",
    # Adicione outras instituições específicas conforme necessário
]


anos = list(range(2025, 1999, -1))  # Intervalo de anos para quebrar a busca

def salvar_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Checkpoint salvo em {filename}")

def carregar_json(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Checkpoint carregado de {filename}, {len(data)} itens.")
        return data
    else:
        return []

def buscar_artigos_por_ano(instituicao, anos, page_size=100):
    artigos = []
    arquivo_artigos = f"artigos_{instituicao.lower().replace(' ', '_').replace('-', '_')}.json"
    artigos = carregar_json(arquivo_artigos)
    ids_existentes = {artigo.get('paperId') for artigo in artigos if artigo.get('paperId')}

    for ano in anos:
        offset = 0
        while True:
            params = {
                "query": f"{instituicao} year:{ano}",
                "limit": page_size,
                "offset": offset,
                "fields": "title,authors,year"
            }

            print(f"Buscando artigos de {instituicao} no ano {ano}, offset {offset}...")
            response = requests.get(BASE_PAPER_URL, params=params)

            if response.status_code == 200:
                data = response.json()
                novos_artigos = data.get("data", [])
                novos_unicos = [a for a in novos_artigos if a.get("paperId") not in ids_existentes]
                artigos.extend(novos_unicos)
                ids_existentes.update(a.get("paperId") for a in novos_unicos)
                print(f"  + {len(novos_unicos)} novos artigos")
                salvar_json(artigos, arquivo_artigos)
                offset += page_size
                time.sleep(DELAY_BETWEEN_REQUESTS)

                if len(novos_artigos) < page_size or offset >= 1000:
                    break

            elif response.status_code == 429:
                print("Rate limit atingido. Esperando...")
                time.sleep(WAIT_ON_429)

            else:
                print(f"Erro {response.status_code} em {instituicao} ano {ano}. Pulando...")
                break

    return artigos

def buscar_detalhes_autor(author_id):
    url = f"{BASE_AUTHOR_URL}{author_id}"
    params = {
        "fields": "name,affiliations,homepage,url,paperCount,citationCount,hIndex"
    }
    while True:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            res = response.json()
            print(res)
            return res
        elif response.status_code == 429:
            print(f"Limite atingido para autor {author_id}, aguardando...")
            time.sleep(WAIT_ON_429)
        else:
            return None

def filtrar_autores_por_afiliacao(autor, instituicao):
    if not autor:
        return False
    afiliacoes = autor.get("affiliations", [])
    for afil in afiliacoes:
        if instituicao.lower() in afil.lower():
            return True
    return False

def coletar_autores_filtrados(artigos, instituicao):
    autores_filtrados = []
    visitados = set()
    arquivo_autores = f"autores_{instituicao.lower().replace(' ', '_').replace('-', '_')}.json"
    autores_filtrados = carregar_json(arquivo_autores)
    visitados = {a.get("authorId") for a in autores_filtrados if a.get("authorId")}

    for artigo in artigos:
        for autor in artigo.get("authors", []):
            author_id = autor.get("authorId")
            if not author_id or author_id in visitados:
                continue
            visitados.add(author_id)
            detalhes = buscar_detalhes_autor(author_id)
            # if filtrar_autores_por_afiliacao(detalhes, instituicao):
            autores_filtrados.append(detalhes)
            if len(autores_filtrados) % CHECKPOINT_AUTORES == 0:
                salvar_json(autores_filtrados, arquivo_autores)
            time.sleep(DELAY_BETWEEN_REQUESTS)

    salvar_json(autores_filtrados, arquivo_autores)
    return autores_filtrados

if __name__ == "__main__":
  # for instituicao in institutions_mg:
      # print(f"\n### Iniciando coleta para: {instituicao}")
      # artigos = buscar_artigos_por_ano(instituicao, anos)
  instituicao = "Universidade Federal de Minas Gerais"
  artigos = carregar_json("artigos_universidade_federal_de_minas_gerais.json")
  
  autores = coletar_autores_filtrados(artigos, instituicao)
  print(f"Finalizado {instituicao}. Aguardando {DELAY_BETWEEN_INSTITUTIONS}s...")
  time.sleep(DELAY_BETWEEN_INSTITUTIONS)
  end_time = time.time()
  total_sec = end_time - start_time
  minutos, segundos = divmod(int(total_sec), 60)
  print(f"Tempo total de execução: {minutos}min {segundos}s")