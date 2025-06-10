import polars as pl

fr = pl.read_csv('fresno.csv', try_parse_dates=True)

print(fr)