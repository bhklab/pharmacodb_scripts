import csv
import datetime
from glob import glob
import re

# declaring the variables and list.
pharmacodb_cell_line = []
cellosaurus_cell_line = []
pharmacodb_file = 'cell_line_pharmacodb.csv'
cellosaurus_file = 'cellosaurus_cell_line.csv'
output_file_cellosaurus = './output_files/output_cellosaurus.csv'
output_file_pharmacodb = './output_files/output_pharmacodb.csv'
output_file_duplicate = './output_files/output_duplicate.csv'
current_year = (datetime.date.today()).strftime('%Y')



# function will read through the file and store the results in unique cell line list.
def readFile(filename):
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for row in csv_reader:
            if filename.split('/')[1] == pharmacodb_file:
                if(row[1]!='cell_name'):
                    pharmacodb_cell_line.append(row[1]+'_'+row[0]+'_'+current_year)
            elif filename.split('/')[1] == cellosaurus_file: 
                if(row[1]!='identifier'):
                    data = {
                        'identifier': row[0],
                        'accession': row[1],
                        'sy': row[3]
                    }
                    cellosaurus_cell_line.append(data)



# function will write the output to the new csv file.
def writeFileCellosauruss(filename):
    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ',')
        csv_writer.writerow(['cellosaurus_ac', 'pharmacodb_id', 'cell_line'])
        for row in pharmacodb_cell_line:
            data = row.split('_')[0]
            pharmacodb_id = row.replace('-','').replace(' ','')
            accession_id = ''
            total_number = 0
            for row in cellosaurus_cell_line:
                sy = row['sy'].split('; ')
                total_number = total_number + 1
                if(row['identifier'] == data or (row['identifier'].replace(' ','')) == data):
                    csv_writer.writerow([row['accession'], pharmacodb_id, data])
                    break
                elif(total_number == cellosaurus_cell_line.__len__() and data in sy):
                    csv_writer.writerow([row['accession'], pharmacodb_id, data])
                elif(data in sy):
                    accession_id = row['accession']
                elif(total_number == cellosaurus_cell_line.__len__()):
                        csv_writer.writerow([accession_id, pharmacodb_id, data])



# function to find the duplicate cell line names whether 
# it's the primary cell id or synonyms in Cellosaurus file.    
def duplicateCellLines(filename):
    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ',')
        csv_writer.writerow(['cell_line', "total_repetitions"])
        for row in pharmacodb_cell_line:
            data = row.split('_')[0]
            total_number = 0
            replicates = 0
            for row in cellosaurus_cell_line:
                sy = row['sy'].split('; ')
                total_number = total_number + 1
                #comment if stament and break and elif and uncomment
                #if statement in order to get all the replicates
                #else we can get the needed replicates which are just replicated
                #in 'sy' but not in the cell id.
                if(row['identifier'] == data):
                    break
                elif((data in sy)):
                #if((row['identifier'] == data) or (data in sy)):
                    replicates = replicates + 1
                elif(total_number == cellosaurus_cell_line.__len__()):
                    if(replicates > 1):
                        csv_writer.writerow([data, str(replicates)])



# this will loop through the files to read in the folder.
# it contains pharmacodb cell line file as well as from cellosaurus.
for entry in glob('input_files/*.csv'):
    readFile(entry)
    

# calling write function.
writeFileCellosauruss(output_file_cellosaurus)


# calling function to find duplicates.
#duplicateCellLines(output_file_duplicate)