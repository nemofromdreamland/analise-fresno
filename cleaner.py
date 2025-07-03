import polars as pl
import re

# Carrega os dados do arquivo CSV
fr = pl.read_csv('fresno.csv', try_parse_dates=True)


fr = fr.drop_nulls(subset=['letra'])

def clean_lyrics(text):
    """
    Função para limpar o texto das letras:
    - Remove tags entre colchetes (ex: [Refrão]).
    - Substitui múltiplos espaços por um único.
    - Corrige caracteres especiais.
    - Converte todo o texto para minúsculas.
    """

    if text is None:
        return ''
    text = re.sub(r'\[.*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\u2005', ' ').replace('\u205f', ' ').replace('\x92', "'").replace('\xa0', '')
    return text.strip().lower()

fr = fr.with_columns(

    pl.col('album').str.to_lowercase(),
    
    # --- COLUNA 'musica' COM LIMPEZA APRIMORADA ---
    pl.col('musica')
      .str.replace_all(r'\([^)]*\)', '')  # Remove texto entre parênteses
      .str.strip_chars()                    # Remove espaços em branco do início e fim
      .str.to_lowercase(),                  # Converte para minúsculas
      
    pl.col('letra').map_elements(clean_lyrics, return_dtype=pl.String)
)

# Aplica as transformações de limpeza e normalização nas colunas
fr = fr.with_columns(
    pl.col('album').str.to_lowercase(),
    pl.col('musica').str.to_lowercase(),
    pl.col('letra').map_elements(clean_lyrics, return_dtype=pl.String)
)

# 3. Remove as linhas onde o valor na coluna 'musica' é duplicado, mantendo a primeira ocorrência.
fr = fr.unique(subset=['musica'], keep='first')

# Salva o DataFrame limpo em um novo arquivo CSV
fr.write_csv('fresno_limpo2.csv')

print("Processo concluído! O arquivo 'fresno_limpo.csv' foi criado sem as linhas que continham letras nulas.")