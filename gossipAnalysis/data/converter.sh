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
    cd "$SCRIPT_DIR/.." && python3 -m lntopo timemachine restore "$input" "$timestamp" --fmt graphml --no-pruning > "$output"

    if [ $? -ne 0 ]; then
        echo "ERROR on $gsp_file"
        rm -f "$output"
    else
        echo "Done: $output_file"
    fi
}

process "gossip-20201014.gsp.bz2" 1546300800 "snapshot_2019_01.graphml"
process "gossip-20201014.gsp.bz2" 1561939200 "snapshot_2019_07.graphml"
process "gossip-20201014.gsp.bz2" 1577836800 "snapshot_2020_01.graphml"
process "gossip-20201014.gsp.bz2" 1593561600 "snapshot_2020_07.graphml"
process "gossip-20210104.gsp.bz2" 1609459200 "snapshot_2021_01.graphml"
process "gossip-20220823.gsp.bz2" 1625097600 "snapshot_2021_07.graphml"
process "gossip-20220823.gsp.bz2" 1640995200 "snapshot_2022_01.graphml"
process "gossip-20220823.gsp.bz2" 1656633600 "snapshot_2022_07.graphml"
process "gossip-20230924.gsp.bz2" 1672531200 "snapshot_2023_01.graphml"
process "gossip-20230924.gsp.bz2" 1688169600 "snapshot_2023_07.graphml"
