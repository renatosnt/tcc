import requests
from lxml import html

url = 'http://buscatextual.cnpq.br/buscatextual/resultadoPesquisaCurriculo.do'

params = {
    'filtro': 'instituicao',
    'valor': 'UFMG'
}

response = requests.get(url, params=params)

tree = html.fromstring(response.content)

# Aqui você pode fazer o parsing da página de resultado para extrair os links dos currículos
print(response.url)  # para ver a URL completa usada
print(response.status_code)  # verificar se retornou 200

# Exemplo: buscar links para os currículos (exemplo genérico, precisa adaptar conforme o HTML)
links = tree.xpath('//a[contains(@href, "curriculo")]//@href')
print(links)
