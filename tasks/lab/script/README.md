Steps by steps resolutions breakdown

Task 1:  Clean the repository after cloning it to your sandbox

- Adding Collaborators
- Cloning the repository to the sandbox: git clone https://github.com/tifarekaseke/lab-1_sateliteDataAnalysis.git
- Removing lab-1_sateliteDataAnalysis/dummy,lab-1_sateliteDataAnalysis/raw_data/dummy-2, and lab-1_sateliteDataAnalysis/rename_directory/dummy-3.txt using rm command
- Move satelite_temperature_data.csv to raw_data/ using mv: mv satelite_temperature_data.csv raw_data/satelite_temperature.csv
- Renaming rename_directory, which will hold the ouput of our analyzis, to analyzed_data using mv command: mv rename_directory analyzed_data

End Task 1

Task 2:  Analyze the data with the use of Linux skills

Script 1: 

- Combining cut, sort, and head with pipe to extract, sort, and select the 10 highest temperature values. Then, redirect the result to the file analyzed_data/highest_temp.csv

- Make the script executable for the owner, group users, and others: chmod a+x temp_script.sh

Script 2:

- Select a country: South Africa
- Combining awk and sort to extract South Africa data (select rows), and sort from the highest to the lowest values of humidity. 
- Save the output into analyzed_data/humidity_data_south_africa.csv
- Make the script executable for the owner, group users, everyone else with:
chmod a+x country_sort_script.sh

Script 3:
 
- Combines contents of script 1 and script 2, and redirect the output into a file analyzed_data/summary_result.csv
- Make the script executable for owner, group users, and everyone else: 
chmod a+x bonus_task.sh

End task 2

Contributors: Bode Murairi <b.murairi@alustudent.com>, Faith Irakoze <f.irakoze2@alustudent.com>, Pascal Nsigo <p.nsigo@alustudent.com>, Maurice Nshimyumukiza <m.nshimyumu@alustudent.com>, Tifare Kaseke <t.kaseke@alustudent.com>
 
