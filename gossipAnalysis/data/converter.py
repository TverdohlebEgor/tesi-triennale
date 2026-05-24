import subprocess
import os

datasets = [
    ("gossip-20201014.gsp.bz2", 1602633600, "snapshot_2020_10.graphml"),
    ("gossip-20201102.gsp.bz2", 1604275200, "snapshot_2020_11.graphml"),
    ("gossip-20201203.gsp.bz2", 1606953600, "snapshot_2020_12.graphml"),
    ("gossip-20210104.gsp.bz2", 1609718400, "snapshot_2021_01.graphml"),
    ("gossip-20210908.gsp.bz2", 1631059200, "snapshot_2021_09.graphml"),
    ("gossip-20220823.gsp.bz2", 1661212800, "snapshot_2022_08.graphml"),
    ("gossip-20230924.gsp.bz2", 1695513600, "snapshot_2023_09.graphml"),
]

if __name__ == "__main__":
    for gsp_file, timestamp, output_file in datasets:
        gsp_file = "gossip/"+gsp_file
        output_file = "graphml/"+ output_file 
        if not os.path.exists(gsp_file):
            print(f"Skipping {gsp_file} — file not found")
            continue
    
        if os.path.exists(output_file):
            print(f"Skipping {output_file} — already exists")
            continue
    
        print(f"Processing {gsp_file} -> {output_file} ...")
        with open(output_file, "w") as f:
            result = subprocess.run(
                ["python", "../lntopo/__main__.py", "timemachine", "restore", gsp_file, str(timestamp), "--fmt", "graphml"],
                stdout=f,
                stderr=subprocess.PIPE,
            )
        
        if result.returncode != 0:
            print(f"ERROR on {gsp_file}: {result.stderr.decode()}")
            os.remove(output_file)
        else:
            print(f"Done: {output_file}")
