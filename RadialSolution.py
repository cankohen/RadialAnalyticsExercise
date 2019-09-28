import os
import sqlite3

import pandas as pd

import HeaderStrip


def main():
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

    # Execute SQL Query and save it to the DataFrame
    results = pd.read_sql_query(radial_query, conn)

    # Close connection to database
    conn.close()

    # Write the results of the SQL query onto a CSV file
    results.to_csv(path_to_export + '/hospitals_by_county.csv', index=None, header=True)


# SQL Query that gets all required columns
radial_query_w_median = """SELECT DISTINCT nh.county_state, nh.num_hospitals, nach.num_acute_care_hospitals, 
printf("%.2f", round(nach.num_acute_care_hospitals * 100) / nh.num_hospitals) as pct_acute_care, 
round(aacr.avg_acute_care_rating, 2) as avg_acute_care_rating,
macr.median_acute_care_rating
FROM 
(SELECT (CountyName || ', ' || State) as county_state, count(*) as num_hospitals
		  FROM HGI
		  GROUP BY county_state
		  HAVING num_hospitals > 0) nh
JOIN (SELECT (CountyName || ', ' || State) as county_state, count(*) as num_acute_care_hospitals
		 FROM HGI
		 WHERE HospitalType LIKE 'Acute%'
		 GROUP BY county_state) as nach
ON nh.county_state = nach.county_state
JOIN (SELECT (CountyName || ', ' || State) as county_state, avg(Hospitaloverallrating) as avg_acute_care_rating
		 FROM HGI
		 WHERE HospitalType LIKE 'Acute%' AND Hospitaloverallrating NOT LIKE '%Not%'
		 GROUP BY county_state) as aacr
ON nach.county_state = aacr.county_state
JOIN (SELECT (CountyName || ', ' || State) as county_state , AVG(Hospitaloverallrating) as median_acute_care_rating
FROM (SELECT CountyName, State, Hospitaloverallrating,
			ROW_NUMBER() OVER (
				PARTITION BY CountyName
				ORDER BY Hospitaloverallrating ASC, ProviderID ASC) AS RowAsc,
			ROW_NUMBER() OVER (
				PARTITION BY CountyName
				ORDER BY Hospitaloverallrating DESC, ProviderID DESC) AS RowDesc
		FROM HGI) x
WHERE
   RowAsc IN (RowDesc, RowDesc - 1, RowDesc + 1)
GROUP BY CountyName
ORDER BY CountyName) as macr
ON nh.county_state = macr.county_state
ORDER BY nh.num_hospitals DESC"""

# SQL Query that gets all required columns except median
radial_query = """SELECT DISTINCT nh.county_state, nh.num_hospitals, nach.num_acute_care_hospitals, 
printf("%.2f", round(nach.num_acute_care_hospitals * 100) / nh.num_hospitals) as pct_acute_care, 
round(aacr.avg_acute_care_rating, 2) as avg_acute_care_rating
FROM 
(SELECT (CountyName || ', ' || State) as county_state, count(*) as num_hospitals
		  FROM HGI
		  GROUP BY county_state
		  HAVING num_hospitals > 0) nh
JOIN (SELECT (CountyName || ', ' || State) as county_state, count(*) as num_acute_care_hospitals
		 FROM HGI
		 WHERE HospitalType LIKE 'Acute%'
		 GROUP BY county_state) as nach
ON nh.county_state = nach.county_state
JOIN (SELECT (CountyName || ', ' || State) as county_state, avg(Hospitaloverallrating) as avg_acute_care_rating
		 FROM HGI
		 WHERE HospitalType LIKE 'Acute%' AND Hospitaloverallrating NOT LIKE '%Not%'
		 GROUP BY county_state) as aacr
ON nach.county_state = aacr.county_state
ORDER BY nh.num_hospitals DESC"""

if __name__ == '__main__':
    main()