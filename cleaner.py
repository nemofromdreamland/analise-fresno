import polars as pl
import re

fr = pl.read_csv('fresno.csv', try_parse_dates=True)

def clean_lyrics(text):
    if text is None:
        return ''
    text = re.sub(r'\[.*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\u2005', ' ').replace('\u205f', ' ').replace('\x92', "'").replace('\xa0', '')
    return text.strip().lower()

fr = fr.with_columns(
    fr.get_column('album').str.to_lowercase(),
    fr.get_column('musica').str.to_lowercase(),
    fr.get_column('letra').map_elements(clean_lyrics, return_dtype=pl.String)
)

fr.write_csv('fresno_limpo.csv')
