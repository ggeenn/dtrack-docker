import csv

# Open the CSV file
with open('import/deeprisk.csv', mode='r', encoding='utf-8') as csvfile:
    # Create a DictReader object
    reader = csv.DictReader(csvfile)
    
    # Iterate over the rows in the CSV file
    for row in reader:
        # Access fields by column names
        print(f"{row}")
