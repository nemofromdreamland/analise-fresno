import matplotlib.pyplot as plt
import polars as pl

df = pl.read_csv('fresno_stats2.csv')

"""
Contagem de faixas por disco
"""

# counter = df.group_by('album').len().sort('len')
# fig, ax = plt.subplots()
# ax.barh(counter['album'], counter['len'])
# plt.show()

"""
Estatísticas gerais por album
"""

# for album in df.sort('data').partition_by('album'):
#     album = album.sort('tokens')

#     mean = album['ttr'].mean()

#     fig, ax = plt.subplots()

#     ax.barh(album['musica'], album['tokens'])
#     ax.barh(album['musica'], album['types'])
#     ax.barh(album['musica'], album['ttr'])
#     ax.axvline(x=mean)

#     ax.set_title(f"{album['album'][0]} - {album['data'][0]}")

#     ax.set_xlabel('Estatísticas de texto')
#     ax.set_ylabel('Nome da música')

#     ax.legend(
#         (
#             'Média de TTR',
#             'Tokens (N): Quantidade de palavras',
#             'Types (N): Quantidade de palavras únicas',
#             'TTR (%): Relação entre Tokens e Types',
#         )
#     )

#     plt.show()

"""
Estatísticas gerais por target
"""

boxes = {}

target = 'types'

for album in df.sort('data').partition_by('album'):
    boxes |= {
        album['album'][0]: album[target].drop_nulls()
    }


fig, ax = plt.subplots()

mean = df[target].mean()
ax.axhline(y=mean)

ax.boxplot(boxes.values())
ax.set_xticklabels(boxes.keys())

plt.show()