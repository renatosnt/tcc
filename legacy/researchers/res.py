import requests
import time
import json

BASE_PAPER_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
BASE_AUTHOR_URL = "https://api.semanticscholar.org/graph/v1/author/"
DELAY_BETWEEN_REQUESTS = 2
WAIT_ON_429 = 60

# Lista de instituições de MG para filtro por afiliação
institutions_mg = [
    "Universidade Federal de Minas Gerais",
    "UFMG",
    "Universidade Federal de Uberlândia",
    "UFU",
    "Pontifícia Universidade Católica de Minas Gerais",
    "PUC Minas",
    "Universidade Federal de Viçosa",
    "UFV",
    "Centro Federal de Educação Tecnológica de Minas Gerais",
    "CEFET-MG",
    # Adicione mais conforme necessário
]

def buscar_artigos(instituicao, total_limite=50, page_size=20):
    offset = 0
    artigos = []

    while offset < total_limite:
        limit = min(page_size, total_limite - offset)
        params = {
            "query": instituicao,
            "limit": limit,
            "offset": offset,
            "fields": "title,authors,year,venue"
        }

        print(f"Buscando artigos {offset + 1} a {offset + limit}...")

        while True:
            response = requests.get(BASE_PAPER_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                artigos.extend(data.get("data", []))
                offset += limit
                time.sleep(DELAY_BETWEEN_REQUESTS)
                break
            elif response.status_code == 429:
                print(f"Limite atingido. Aguardando {WAIT_ON_429} segundos...")
                time.sleep(WAIT_ON_429)
            else:
                print(f"Erro inesperado: {response.status_code}")
                return artigos

    return artigos

def buscar_detalhes_autor(author_id):
    url = f"{BASE_AUTHOR_URL}{author_id}"
    params = {
        "fields": "name,affiliations,homepage,url,paperCount,citationCount,hIndex"
    }

    while True:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"Limite atingido na consulta do autor {author_id}. Aguardando {WAIT_ON_429} segundos...")
            time.sleep(WAIT_ON_429)
        else:
            print(f"Erro na consulta do autor {author_id}: {response.status_code}")
            return None

def filtrar_autores_por_afiliacao(autor):
    if not autor:
        return False
    afiliacoes = autor.get("affiliations", [])
    for afil in afiliacoes:
        for inst in institutions_mg:
            if inst.lower() in afil.lower():
                return True
    return False

def coletar_autores_filtrados(artigos):
    autores_filtrados = []
    visitados = set()

    for artigo in artigos:
        for autor in artigo.get("authors", []):
            author_id = autor.get("authorId")
            if not author_id or author_id in visitados:
                continue
            visitados.add(author_id)
            print(f"Buscando detalhes do autor ID {author_id} - {autor.get('name')}")
            detalhes = buscar_detalhes_autor(author_id)
            if filtrar_autores_por_afiliacao(detalhes):
                autores_filtrados.append(detalhes)
            time.sleep(DELAY_BETWEEN_REQUESTS)

    return autores_filtrados

def salvar_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Dados salvos em {filename}")

if __name__ == "__main__":
    instituicao = "Universidade Federal de Minas Gerais"
    total_limite = 50  # ajustar conforme necessidade para menos chamadas

    artigos = buscar_artigos(instituicao, total_limite=total_limite)
    salvar_json(artigos, "artigos.json")

    autores_filtrados = coletar_autores_filtrados(artigos)
    salvar_json(autores_filtrados, "autores_filtrados_mg.json")
