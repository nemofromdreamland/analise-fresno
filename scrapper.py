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
    # print(letra) # Descomente para ver a letra no console
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
    discos = s.css('.ddfKcW') # Seletor para os álbuns na página do artista

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

    # Seletor para o nome do álbum
    nome_album = s.css('h1.header_with_cover_art-primary_info-title::text').get()
    if nome_album:
        nome_album = nome_album.strip()
    else:
        nome_album = "Nome do Álbum Desconhecido" # Fallback

    # Seletor para o ano do álbum. Pode precisar de ajuste!
    # Inspecione o HTML da página do álbum para confirmar o seletor exato.
    # Exemplo de seletor comum para a data de lançamento:
    ano_album_raw = s.css('span.metadata_unit-info::text').getall()
    ano_album = None
    for text_content in ano_album_raw:
        if 'Released' in text_content: # Busca por texto "Released" ou similar
            parts = text_content.split(' ')
            for part in parts:
                if part.isdigit() and len(part) == 4: # Procura um número de 4 dígitos (ano)
                    ano_album = part
                    break
            if ano_album:
                break
    
    if not ano_album:
        # Tenta pegar de uma meta tag, ou de outro local comum
        meta_date = s.css('meta[property="og:title"]::attr(content)').get()
        if meta_date:
            parsed_date = dateparser.parse(meta_date)
            if parsed_date:
                ano_album = str(parsed_date.year)


    # Se tudo falhar, ou se você quiser definir manualmente para este caso:
    if not ano_album:
         ano_album = "2001-12-22" # Data de lançamento confirmada para "O acaso do erro"

    return (url_album, nome_album, ano_album)

# ---

url_fresno_albuns = 'https://genius.com/artists/Fresno/albums'
url_o_acaso_do_erro = 'https://genius.com/albums/Fresno/O-acaso-do-erro'

with open('fresno.csv', 'w', encoding='utf-8', newline='') as f:
    writer = DictWriter(f, ['album', 'data', 'musica', 'letra'])
    writer.writeheader()

    # Processa os álbuns encontrados na página principal de álbuns do artista
    for disco in discos(url_fresno_albuns):
        # A URL do disco, o nome do disco e o ano do disco
        disco_url, disco_nome, disco_ano = disco 
        
        for faixa_nome, faixa_url in faixas(disco_url):
            row = {
                'album': disco_nome,
                'data': dateparser.parse(disco_ano).strftime('%Y-%m-%d') if disco_ano else None,
                'musica': faixa_nome,
                'letra': letra(faixa_url)
            }
            print(f"Adicionando: Álbum '{row['album']}', Música '{row['musica']}'")
            writer.writerow(row)

    # ---

    # Adiciona o álbum "O acaso do erro" separadamente
    # Primeiro, extraímos as informações do álbum "O acaso do erro"
    disco_url_acaso, disco_nome_acaso, disco_ano_acaso = extrair_info_album_individual(url_o_acaso_do_erro)
    
    for faixa_nome, faixa_url in faixas(disco_url_acaso):
        row = {
            'album': disco_nome_acaso,
            'data': dateparser.parse(disco_ano_acaso).strftime('%Y-%m-%d') if disco_ano_acaso else None,
            'musica': faixa_nome,
            'letra': letra(faixa_url)
        }
        print(f"Adicionando: Álbum '{row['album']}', Música '{row['musica']}'")
        writer.writerow(row)

print("Scraping concluído! Verifique o arquivo 'fresno.csv'.")