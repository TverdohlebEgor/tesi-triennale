import sys
import pyarrow.dataset as ds
import gcsfs

# ==============================================================================
# 1. INITIALIZATION & GOOGLE CLOUD STORAGE LOADING
# ==============================================================================
# Adjust this path if your bucket root structure is named slightly differently
BUCKET_PATH = "tesi-triennale/Complete-bitcoin-2025-mg2/"

print("==========================================================================")
print("Connecting to Google Cloud Storage and Initializing PyArrow Dataset...")
try:
    # Initialize GCS filesystem with a 1MB block size to prevent SSL memory spikes
    fs = gcsfs.GCSFileSystem(block_size=1024 * 1024)
    
    # Pass the GCS filesystem instance explicitly into PyArrow
    dataset = ds.dataset(BUCKET_PATH, filesystem=fs, format="parquet")
except Exception as e:
    print(f"Error loading dataset at {BUCKET_PATH}: {e}")
    print("\nTip: Verify your cloud credentials, internet connection, or path naming.")
    sys.exit(1)

# ==============================================================================
# 2. EDGE COUNT (Original Print Requirement)
# ==============================================================================
print("Fetching dataset metadata from cloud...")
try:
    total_rows = dataset.count_rows()
    print(f"Total Edges (Rows): {total_rows:,}")
except Exception as e:
    print(f"Failed to fetch metadata count: {e}")
    sys.exit(1)

print("Scanning source and target columns for unique nodes...")
print("--------------------------------------------------------------------------")

# ==============================================================================
# 3. MEMORY-SAFE BATCH STREAMING LOOP
# ==============================================================================
unique_nodes = set()
batch_count = 0

# Stream columns explicitly mapping to your schema: from_address and to_address
for batch in dataset.to_batches(columns=["from_address", "to_address"]):
    batch_count += 1
    
    # Extract unique string tokens from the current batch's 'from_address'
    from_chunk = batch.column("from_address").unique().to_pylist()
    unique_nodes.update(from_chunk)
    
    # Extract unique string tokens from the current batch's 'to_address'
    to_chunk = batch.column("to_address").unique().to_pylist()
    unique_nodes.update(to_chunk)
    
    # ==========================================================================
    # 4. REAL-TIME RAM ESTIMATION
    # ==========================================================================
    # sys.getsizeof(unique_nodes) returns the allocation overhead of the hash set.
    # We add 40 bytes per string to approximate the underlying CPython string object data.
    set_structure_bytes = sys.getsizeof(unique_nodes)
    estimated_string_bytes = len(unique_nodes) * 40
    total_ram_bytes = set_structure_bytes + estimated_string_bytes
    ram_mb = total_ram_bytes / (1024 * 1024)
    
    # Progress feedback boundary: prints every 50 batches to maintain high throughput
    if batch_count % 50 == 0:
        print(f"Processed {batch_count:4d} batches | Unique nodes: {len(unique_nodes):,d} | Est. RAM: {ram_mb:.2f} MB")

# ==============================================================================
# 5. FINAL METRICS REPORT
# ==============================================================================
print("============================== SCAN COMPLETE ==============================")
final_ram_gb = (sys.getsizeof(unique_nodes) + (len(unique_nodes) * 40)) / (1024 ** 3)

print(f"Grand Total Patched Batches: {batch_count:,}")
print(f"Total Unique Nodes Found:    {len(unique_nodes):,}")
print(f"Final RAM footprint of Set:  {final_ram_gb:.2f} GB")
print("==========================================================================")
