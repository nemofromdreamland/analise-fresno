import spacy
import polars as pl

nlp = spacy.load('pt_core_news_lg')

def tokens(text: str) -> int:
    """Quantidade de tokens em um texto."""
    doc = nlp(text)
    return len([t.text for t in doc if not t.is_punct])


def types(text: str) -> int:
    """Quantidade de types em um texto."""
    doc = nlp(text)
    return len(set([t.text for t in doc if not t.is_punct]))


def ttr(cols) -> float:
    """Type-token ratio."""
    return (cols['types'] / cols['tokens']) * 100


def lemmas(text: str) -> int:
    """Quantidade de lemmas."""
    doc = nlp(text)
    return len(set([t.lemma_ for t in doc if not t.is_punct]))

fr = pl.read_csv('fresno_limpo.csv')

new_fr = fr.with_columns(
    (
        pl.col('letra')
        .alias('tokens')
        .map_elements(tokens, return_dtype=int)
    ),
    (
        pl.col('letra')
        .alias('types')
        .map_elements(types, return_dtype=int)
    ),
    (
        pl.col('letra')
        .alias('lemmas')
        .map_elements(lemmas, return_dtype=int)
    ),
).with_columns(
    (
        pl.struct(
            ['types', 'tokens']
        ).alias('ttr').map_elements(ttr, return_dtype=float)
    ),
    (
        pl.struct(
            ['lemmas', 'tokens']
        )
        .alias('ltor')
        .map_elements(
            lambda cols: (cols['lemmas'] / cols['tokens']) * 100,
            return_dtype=float
        )
    ),
    (
        pl.struct(
            ['lemmas', 'types']
        )
        .alias('ltyr')
        .map_elements(
            lambda cols: (cols['lemmas'] / cols['types']) * 100,
            return_dtype=float
        )
    ),
)

new_fr.write_csv('fresno_stats.csv')