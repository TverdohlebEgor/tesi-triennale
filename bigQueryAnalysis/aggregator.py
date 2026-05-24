import pyarrow.parquet as pq
import igraph as ig
import gcsfs

years = [
"2016",
"2017",
"2018",
"2019",
"2020",
"2021",
"2022",
"2023",
"2024",
"2025"
        ]

for y in years:
    print("="*30)
    print(y)
    fs = gcsfs.GCSFileSystem()
    files = fs.glob(f"tesi-triennale/Dogecoin-{y}-mg2/*.parquet")
    print(f"Found {len(files)} files")

    dataset = pq.ParquetDataset(files, filesystem=fs)
    table = dataset.read()
    print(f"Rows: {table.num_rows}")

    df = table.to_pandas()

    print("Building graph...")
    g = ig.Graph.TupleList(
        df.itertuples(index=False),
        directed=True,
        edge_attrs=["total_value", "num_transactions"]
    )

    print(f"Nodes: {g.vcount()}, Edges: {g.ecount()}")
    g.save(f"/mnt/data/dogecoin_{y}.graphml")
    print("Saved!")
    print("="*30)
