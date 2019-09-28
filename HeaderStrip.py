import csv

def strip_header():
    input_file_name = "Hospital General Information.csv"
    output_file_name = "HGI.csv"

    with open(input_file_name, 'r') as inFile, open(output_file_name, 'w') as outfile:
        r = csv.reader(inFile)
        w = csv.writer(outfile)

        next(r)

        w.writerow(['Provider ID', 'Hospital Name', 'Address', 'City', 'State', 'ZIP Code',
                    'CountyName', 'PhoneNumber', 'HospitalType', 'HospitalOwnership',
                    'EmergencyServices', 'MeetscriteriaformeaningfuluseofEHRs',
                    'Hospitaloverallrating', 'Hospitaloverallratingfootnote',
                    'Mortalitynationalcomparison',
                    'Mortalitynationalcomparisonfootnote',
                    'Safetyofcarenationalcomparison',
                    'Safetyofcarenationalcomparisonfootnote',
                    'Readmissionnationalcomparison',
                    'Readmissionnationalcomparisonfootnote',
                    'Patientexperiencenationalcomparison',
                    'Patientexperiencenationalcomparisonfootnote',
                    'Effectivenessofcarenationalcomparison',
                    'Effectivenessofcarenationalcomparisonfootnote',
                    'Timelinessofcarenationalcomparison',
                    'Timelinessofcarenationalcomparisonfootnote',
                    'Efficientuseofmedicalimagingnationalcomparison',
                    'Efficientuseofmedicalimagingnationalcomparisonfootnote'])

        # copy the rest
        for row in r:
            w.writerow(row)


if __name__ == '__main__':
   strip_header()