import json

with open("form_data.json", "r", encoding="utf-8") as f:
  data = json.load(f)

rename_map = {
  "_id": "_id",
  "unidade": "nome_organizacao",
  "sigla": "sigla_unidade",
  "tema": "tema_principal", # TODO: alinhar com o Lucas o que é exatamente
  "frentes": "principais_frentes", # frentes de pesquisa
  "pontoFocal": "responsavel_tecnico",
  "tel": "telefone", # TODO: telefone do ponto focal ou da unidade?
  "email": "email_contato",
  "areaP": "area_prioritaria", # TODO: area prioritaria ou areas de pesquisa?
  "politica": "missao_nib", # missão do programa Nova Indústria Brasil
  "linhaspesquisa": "linhas_de_pesquisa",
  "cidade": "cidade_sede",
  "uf": "uf_sede",
  "tipo": "area_de_conhecimento", # TODO:  (campo ou area de conhecimento, me parece tipo exatas, saude, engenharia, humanas) 
  "site": "site_organizacao",
  "instituicao": "instituicao_de_ensino",
  "coordenadas": "coordenadas"  # tratamos separadamente
}

# TODO
# O que é:
# tema?
# areaP?
# tipo? 
# Telefone é o telefone da unidade ou do ponto Focal?

# TODO
# preciso saber as principais diferenças entre  tema, areaP, tipo e linhas de pesquisa

# TODO
# o que usar pra derivar missao_nib

# TODO
# tratar dados vazios


def transform_data(data):
  new_data = {}

  for key, value in data.items():
    if key == "coordenadas":
      new_data["latitude"] = value.get("lat")
      new_data["longitude"] = value.get("lon")
    elif key in rename_map:
      new_data[rename_map[key]] = value
    else:
      print(key)
      new_data[key] = value
  
  return new_data

transformed_data = [transform_data(d) for d in data]

with open("transformed_form_data.json", "w", encoding="utf-8") as f:
  json.dump(transformed_data, f, indent=2, ensure_ascii=False)
