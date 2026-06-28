import pyarrow.parquet as pq
import igraph as ig
import gcsfs

years = ["2025"]

for y in years:
    print("="*30)
    print(y)
    fs = gcsfs.GCSFileSystem()
    files = fs.glob(f"tesi-triennale/Complete-bitcoin-2025-mg2/*.parquet")
    print(f"Found {len(files)} files")

    edge_list = []

    # Process files one by one to prevent MemoryError
    for i, file_path in enumerate(files):
        if i % 50 == 0:
            print(f"Processing file {i}/{len(files)}...")
            
        try:
            # Read a single file using pyarrow.dataset
            # Specify columns to read only what you absolutely need
            dataset = pq.ParquetDataset(file_path, filesystem=fs)
            table = dataset.read()
            
            # Convert to a lightweight list of tuples and extend our edge master list
            # Adjust column order to match what TupleList expects: (source, target, attr1, attr2, ...)
            df_batch = table.to_pandas()
            for row in df_batch.itertuples(index=False):
                edge_list.append(row)
                
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

    print(f"Total edges collected: {len(edge_list)}")
    print("Building graph...")
    
    # Build the graph from the accumulated lightweight tuple list
    g = ig.Graph.TupleList(
        edge_list,
        directed=True,
        edge_attrs=["total_value", "num_transactions"]
    )

    print(f"Nodes: {g.vcount()}, Edges: {g.ecount()}")
    
    # NOTE: Ensure this path is accessible on your Windows machine 
    # (C:/... instead of /mnt/data/ if you are running natively on Windows cmd)
    output_path = f"complete_bitcoin_{y}.graphml" 
    g.save(output_path)
    print(f"Saved to {output_path}!")
    print("="*30)
