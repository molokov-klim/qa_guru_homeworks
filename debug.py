import csv
import os

WORKING_DIR = os.getcwd()
print(WORKING_DIR)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
print(SCRIPT_DIR)




if not os.path.exists('resources'):
    os.makedirs('resources')

with open('resources/eggs.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(['Anna', 'Pavel', 'Peter'])
    csvwriter.writerow(['Alex', 'Serj', 'Yana'])

with open('resources/eggs.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        print(row)

