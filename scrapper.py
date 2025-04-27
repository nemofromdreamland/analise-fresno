"""

CSV =

Album: Eu nunca fui ...
Data: 2024
Musica: Quando o Pesadelo Acabar
letra: Desastre, tragédia, beirando a comédia

Eu nunca fui ...,2024,Quando o Pesadelo Acabar,Desastre...
"""

from httpx import get
from parsel import Selector

response = get('https://genius.com/Fresno-quando-o-pesadelo-acabar-lyrics')

if response.status_code == 200:
    # Salvar o HTML em um arquivo
    with open('letra_fresno.html', 'w', encoding='utf-8') as f:  # Nome alterado
        f.write(response.text)
    print("Arquivo salvo com sucesso!")
else:
    print(f"Erro: Status code {response.status_code}")