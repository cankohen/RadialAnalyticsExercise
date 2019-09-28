import sqlite3
import pandas as pd
import os
import HeaderStrip

# Strip the header of the CSV file (get rid of space between column names)
HeaderStrip.strip_header()

# Path to CSV file
csvfile = os.getcwd() + '/HGI.csv'

# Table name
table_name = 'HGI'

# Path to export CSV file
path_to_export = os.getcwd()

# Import CSV file to Pandas DataFrame
df = pd.read_csv(csvfile, skipinitialspace=True)

# Create new SQLite instance and connection
conn = sqlite3.connect(":memory:")

# Convert Pandas DataFrame to SQLite
df.to_sql(table_name, conn, if_exists='replace', index=False)

# SQL Query that gets all required columns
radial_query = "SELECT DISTINCT (h.CountyName || ', ' || h.State) as county_state, nh.num_hospitals, " \
               "nach.num_acute_care_hospitals, printf(\"%.2f\", " \
               "round(nach.num_acute_care_hospitals * 100) / nh.num_hospitals) as pct_acute_care, " \
               "round(aacr.avg_acute_care_rating, 2) as avg_acute_care_rating, " \
               "macr.median_acute_care_rating " \
               "FROM HGI h " \
               "LEFT JOIN (SELECT CountyName, count(*) as num_hospitals FROM HGI " \
                          "GROUP BY CountyName " \
                          "HAVING num_hospitals > 0) nh " \
               "ON h.CountyName = nh.CountyName " \
               "LEFT JOIN (SELECT CountyName, count(*) as num_acute_care_hospitals " \
                          "FROM HGI " \
                          "WHERE HospitalType LIKE 'Acute%' " \
                          "GROUP BY CountyName) as nach " \
               "ON nh.CountyName = nach.CountyName " \
               "LEFT JOIN (SELECT CountyName, avg(Hospitaloverallrating) as avg_acute_care_rating " \
                          "FROM HGI " \
                          "WHERE HospitalType LIKE 'Acute%' AND Hospitaloverallrating NOT LIKE '%Not%' " \
                          "GROUP BY CountyName) as aacr " \
               "ON nach.CountyName = aacr.CountyName " \
               "LEFT JOIN (SELECT CountyName, avg(Hospitaloverallrating) as median_acute_care_rating " \
                          "FROM (SELECT CountyName, Hospitaloverallrating " \
                                "FROM HGI " \
                                "ORDER BY Hospitaloverallrating " \
                                "LIMIT 2 - (SELECT COUNT(*) FROM HGI) % 2 " \
                                "OFFSET (SELECT (COUNT(*) - 1) / 2 FROM HGI))) as macr " \
               "ON aacr.CountyName = macr.CountyName " \
               "ORDER BY num_hospitals DESC"

# Execute SQL Query
results = pd.read_sql_query(radial_query, conn)

conn.close()

# Write the results of the SQL query onto a CSV file
results.to_csv(path_to_export + '/hospitals_by_county.csv', index = None, header=True)