"""

CSV =

Album: Eu nunca fui ...
Data: 2024
Musica: Quando o Pesadelo Acabar
letra: Desastre, tragédia, beirando a comédia

Eu nunca fui ...,2024,Quando o Pesadelo Acabar,Desastre...
"""

from csv import DictWriter
import dateparser
from httpx import get
from parsel import Selector

def letra(url: str) -> str:
    """Pega a letra de uma música"""
    response = get(url)
    s = Selector(response.text)
    letra = '\n'.join(s.css('[data-lyrics-container] *::text').getall())
    return letra

def faixas(url: str) -> list[tuple[str, str]]:
    """Pega as faixas de um álbum ou chart"""
    response = get(url)
    s = Selector(response.text)
    musicas = s.css('div.chart_row-content')

    return [
        (musica.css('h3::text').get().strip(), musica.css('a').attrib['href'])
        for musica in musicas
    ]

def discos(url: str) -> list[tuple[str | None, ...]]:
    """Pega os discos da página de álbuns do artista"""
    response = get(url)
    s = Selector(response.text)
    discos = s.css('.ddfKcW')

    resultado = []

    for disco in discos:
        disco_url = disco.css('.jsXEqK').attrib['href']
        disco_nome = disco.css('.gSnatN::text').get()
        disco_ano = disco.css('.ixmAQP::text').get()
        
        resultado.append(
            (disco_url, disco_nome, disco_ano)
        )
    return resultado

def extrair_info_album_individual(url_album: str) -> tuple[str, str, str | None]:
    """Extrai nome e ano de um álbum específico a partir da sua URL"""
    response = get(url_album)
    s = Selector(response.text)

    nome_album = s.css('h1.header_with_cover_art-primary_info-title::text').get()
    if nome_album:
        nome_album = nome_album.strip()
    else:
        nome_album = "Nome do Álbum Desconhecido"

    ano_album_raw = s.css('span.metadata_unit-info::text').getall()
    ano_album = None
    for text_content in ano_album_raw:
        if 'Released' in text_content:
            parts = text_content.split(' ')
            for part in parts:
                if part.isdigit() and len(part) == 4:
                    ano_album = part
                    break
            if ano_album:
                break
    
    if not ano_album:
        meta_date = s.css('meta[property="og:title"]::attr(content)').get()
        if meta_date:
            parsed_date = dateparser.parse(meta_date)
            if parsed_date:
                ano_album = str(parsed_date.year)

    if not ano_album:
        ano_album = "2001-12-22"

    return (url_album, nome_album, ano_album)

# ---

url_fresno_albuns = 'https://genius.com/artists/Fresno/albums'
url_o_acaso_do_erro = 'https://genius.com/albums/Fresno/O-acaso-do-erro'

with open('fresno.csv', 'w', encoding='utf-8', newline='') as f:
    writer = DictWriter(f, ['album', 'data', 'musica', 'letra'])
    writer.writeheader()

    for disco in discos(url_fresno_albuns):
        disco_url, disco_nome, disco_ano = disco 
        
        # Parse the date and format it as a full datetime string
        parsed_date = dateparser.parse(disco_ano) if disco_ano else None
        # Format as YYYY-MM-DD HH:MM:SS (or just YYYY-MM-DD 00:00:00 if no time)
        formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S') if parsed_date else None

        for faixa_nome, faixa_url in faixas(disco_url):
            row = {
                'album': disco_nome,
                'data': formatted_date, # Use the full datetime string here
                'musica': faixa_nome,
                'letra': letra(faixa_url)
            }
            print(f"Adicionando: Álbum '{row['album']}', Música '{row['musica']}'")
            writer.writerow(row)

    # ---

    disco_url_acaso, disco_nome_acaso, disco_ano_acaso = extrair_info_album_individual(url_o_acaso_do_erro)
    
    # Parse and format for "O acaso do erro" as well
    parsed_date_acaso = dateparser.parse(disco_ano_acaso) if disco_ano_acaso else None
    formatted_date_acaso = parsed_date_acaso.strftime('%Y-%m-%d %H:%M:%S') if parsed_date_acaso else None

    for faixa_nome, faixa_url in faixas(disco_url_acaso):
        row = {
            'album': disco_nome_acaso,
            'data': formatted_date_acaso, # Use the full datetime string here
            'musica': faixa_nome,
            'letra': letra(faixa_url)
        }
        print(f"Adicionando: Álbum '{row['album']}', Música '{row['musica']}'")
        writer.writerow(row)

print("Scraping concluído! Verifique o arquivo 'fresno.csv'.")