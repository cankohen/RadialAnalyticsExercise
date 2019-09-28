# Radial Analytics - Coding Exercise
Python script that works in the following criteria:

 - Use a single file from the Hospital Compare dataset as your input: “Hospital General Information.csv”. 
	 - Assumes that this file is present in the same directory as the code itself.
- Generates a single comma-separated value file as output, named “hospitals_by_county.csv” containing the following fields:  
	- county_state
	- num_hospitals – total number of hospitals in the county
	- num_acute_care_hospitals – number of acute care hospitals in the county
	- pct_acute_care - the percentage of hospitals in the county that are acute care hospitals (scale: 0-100%, rounded to hundredths)
	- avg_acute_care_rating – the average overall rating for acute care hospitals in the county
	- median_acute_care_rating – the median overall rating for acute care hospitals in the county
-   The output file is sorted by descending order of **num_hospitals**

User Guide:
--------

 1. This python script requires the 'pandas' library to be installed.
	 -	In order to install pandas, you can run the command: 'pip3 install pandas' in your preferred command line interface.
 2. CD to the directory where this project is cloned or downloaded.
 3. Run the script by running the command: 'Python3 RadialSolution.py'


Note:
-------

 - Unfortunately I was not able to make the median column work in the script despite making it work in SQLite 3.27.2. 
	- Python's native SQLite3 library is SQLite 3.22.0 and does not support window functions yet.
- You can see the query that returns the 'median_acute_care_rating' as well in the main script (RadialSolution.py) marked as: **'radial_query_w_median'**
	- You can try running this query on [https://sqliteonline.com](https://sqliteonline.com/) by importing the included HGI.sql table and running the script on it. 
