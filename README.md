# Análise das letras do Fresno

## Técnica 

- Captura dos dados

    - Baixar todas as letras!
        - httpx + parsel - Genius (https://genius.com/artists/Fresno/albums)

    - Persistir
        - CSV

- Organização
    - DataFrame - Polars / Pandas

- Limpeza / tratamento 

    - Dataframe

    - Repo de stopwords

- Olhar os dados!

    - Spacy
    - WordCloud

#Análise: Perguntas

- Quais são as palavras mais usadas?

    - Por disco
    - Por década
    - Em que contexto?

- Análise léxica

    - Quantas palavras únicas por música? (média por disco?)

    - Quantas palavras por disco?

    - Dispersão (onde a palavra ocorre no disco?)

- Gramatica
    - tag
- Ver
    - Nuvem de palavras
    - Concord