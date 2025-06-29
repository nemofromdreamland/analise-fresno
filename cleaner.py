import polars as pl
import re

# Carrega os dados do arquivo CSV
fr = pl.read_csv('fresno.csv', try_parse_dates=True)

# --- ETAPA DE REMOÇÃO DE NULOS ---
# Remove todas as linhas em que o valor na coluna 'letra' é nulo.
# Esta é a melhor abordagem para garantir a qualidade dos dados.
fr = fr.drop_nulls(subset=['letra'])

def clean_lyrics(text):
    """
    Função para limpar o texto das letras:
    - Remove tags entre colchetes (ex: [Refrão]).
    - Substitui múltiplos espaços por um único.
    - Corrige caracteres especiais.
    - Converte todo o texto para minúsculas.
    """
    # A verificação 'if text is None' não é mais estritamente necessária
    # pois já removemos os nulos, mas é uma boa prática mantê-la.
    if text is None:
        return ''
    text = re.sub(r'\[.*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\u2005', ' ').replace('\u205f', ' ').replace('\x92', "'").replace('\xa0', '')
    return text.strip().lower()

# Aplica as transformações de limpeza e normalização nas colunas
fr = fr.with_columns(
    pl.col('album').str.to_lowercase(),
    pl.col('musica').str.to_lowercase(),
    pl.col('letra').map_elements(clean_lyrics, return_dtype=pl.String)
)

# Salva o DataFrame limpo em um novo arquivo CSV
fr.write_csv('fresno_limpo.csv')

print("Processo concluído! O arquivo 'fresno_limpo.csv' foi criado sem as linhas que continham letras nulas.")