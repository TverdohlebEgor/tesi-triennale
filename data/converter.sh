###############################
#   Author: Tverdohleb Egor   #
###############################
#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
GOSSIP_DIR="$SCRIPT_DIR/gossip"
GRAPHML_DIR="$SCRIPT_DIR/graphml"

mkdir -p "$GRAPHML_DIR"

process() {
    local gsp_file="$1"
    local timestamp="$2"
    local output_file="$3"
    local input="$GOSSIP_DIR/$gsp_file"
    local output="$GRAPHML_DIR/$output_file"

    if [ ! -f "$input" ]; then
        echo "Skipping $gsp_file — file not found"
        return
    fi

    if [ -f "$output" ]; then
        echo "Skipping $output_file — already exists"
        return
    fi

    echo "Processing $gsp_file -> $output_file ..."
    cd "$SCRIPT_DIR/.." && python3 -m lntopo timemachine restore "$input" "$timestamp" --fmt graphml > "$output"

    if [ $? -ne 0 ]; then
        echo "ERROR on $gsp_file"
        rm -f "$output"
    else
        echo "Done: $output_file"
    fi
}

process "gossip-20201014.gsp.bz2" 1602633600 "snapshot_2020_10.graphml"
process "gossip-20201102.gsp.bz2" 1604275200 "snapshot_2020_11.graphml"
process "gossip-20201203.gsp.bz2" 1606953600 "snapshot_2020_12.graphml"
process "gossip-20210104.gsp.bz2" 1609718400 "snapshot_2021_01.graphml"
process "gossip-20210908.gsp.bz2" 1631059200 "snapshot_2021_09.graphml"
process "gossip-20220823.gsp.bz2" 1661212800 "snapshot_2022_08.graphml"
process "gossip-20230924.gsp.bz2" 1695513600 "snapshot_2023_09.graphml"
