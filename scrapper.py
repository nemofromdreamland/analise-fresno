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

def letra(url: str) -> str:
    """Pega a letra de uma música"""
    response = get(url) 
    s = Selector(response.text)
    letra = '\n'.join(s.css('[data-lyrics-container] *::text').getall())
    print(letra)
    return letra

def faixas(url: str) -> list[tuple[str, str]]:
    response = get(url)
    s = Selector(response.text)
    musicas = s.css('div.chart_row-content')

    return [
        (musica.css('h3::text').get().strip(), musica.css('a').attrib['href'])
        for musica in musicas
    ]