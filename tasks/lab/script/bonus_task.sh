#!/bin/bash

# Relative file path for satelite_location

satelite_location="../raw_data/satelite_temperature_data.csv"

# Relative file path for summary_result
file_location="../analyzed_data/summary_result.csv"

echo "Top 10 temperatures" > $file_location

echo "
" >> $file_location
# Extract the top 10 highest temperature and save the result inside summary_result

cut -d, -f3 $satelite_location | sort -nr | head -n 10 >> $file_location

echo "________________________________________________________________________________________________" >> $file_location

# Extract South Africa data and sort based on highest humidity

echo "South Africa data" >> $file_location
echo " " >> $file_location
awk -F, '$1 == "South Africa" {print}' $satelite_location | sort -t, -k4 -nr >> $file_location

