#!/bin/bash

# This script extract the 10 highest temperature and save it in a file

# File paths
satelite_location="../raw_data/satelite_temperature_data.csv"
highest_temp_loc="../analyzed_data/highest_temp.csv"

# Extract top 10 highest temperatures and save to highrest_temp.csv
echo "Top 10 highest temperatures" > $highest_temp_loc

cut -d, -f3 $satelite_location | sort -nr | head -n 10 >> $highest_temp_loc

