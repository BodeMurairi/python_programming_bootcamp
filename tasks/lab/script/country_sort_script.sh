#!/bin/bash

# This script extracts and sorts satellite data for South Africa, retaining the header.

# Define file paths
south_africa_data="../analyzed_data/humidity_data_south_africa.csv"
satelite_location="../raw_data/satelite_temperature_data.csv"

# Extract the header
header=$(head -n 1 "$satelite_location")

# Extract South Africa data and sort by column 4 in descending order
awk -F, 'NR==1 || $1 == "South Africa"' "$satelite_location" | sort -t, -k4 -nr > "$south_africa_data"

# Ensure the header remains at the top
sed -i "1s/.*/$header/" "$south_africa_data"

