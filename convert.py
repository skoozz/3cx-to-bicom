import csv
import re
import uuid
from unidecode import unidecode

input_file = 'contacts_3cx.csv' # Path to CSV file exported from 3CX
output_file = 'contacts_bicom.csv' # Path to output CSV file for BICOM

# List of columns required by BICOM
bicom_columns = ['first_name', 'middle_name', 'last_name', 'email', 'company', 'type1:number1', 'type2:number2']

# Column Matching Dictionary
column_mapping = {
    'FirstName': 'first_name',
    'LastName': 'last_name',
    'Company': 'company',
    'Email': 'email',
    'Mobile': 'type1:number1',
    'Business': 'type2:number2'
}

# Function to clean phone numbers
def clean_phone_number(phone):
    return re.sub(r'\D', '', phone)

# Function to convert non-UTF-8 characters to readable characters
def sanitize_text(text):
    if text is None:
        return ''
    return unidecode(text)

# Read input CSV file
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

# Prepare the new lines for BICOM
new_rows = []

for row in rows:
    new_row = {col: '' for col in bicom_columns}
    
    mobile_value = row.get('Mobile', '')
    business_value = row.get('Business', '')
    
    # Logic for phone numbers
    if mobile_value and business_value:
        # If both numbers are present, put mobile first, then work
        new_row['type1:number1'] = f"mobile:{clean_phone_number(mobile_value)}"
        new_row['type2:number2'] = f"work:{clean_phone_number(business_value)}"
    elif mobile_value:
        # If only the "mobile" is present
        new_row['type1:number1'] = f"mobile:{clean_phone_number(mobile_value)}"
        new_row['type2:number2'] = ''  # Aucun numéro de travail
    elif business_value:
        # If only "work" is present, put it on mobile
        new_row['type1:number1'] = f"mobile:{clean_phone_number(business_value)}"
        new_row['type2:number2'] = ''  # Aucun autre numéro
    else:
        # No number is present
        new_row['type1:number1'] = ''
        new_row['type2:number2'] = ''

    # Process for other fields
    for key, value in row.items():
        if key in column_mapping:
            if key not in ['Mobile', 'Business']:  # Ignore Mobile and Business here
                new_row[column_mapping[key]] = sanitize_text(value)

    # Logic for the first name
    if not new_row['first_name']:
        if new_row['last_name']:
            new_row['first_name'] = new_row['last_name']
        elif new_row['company']:
            new_row['first_name'] = new_row['company']
        else:
            new_row['first_name'] = "A definir"

    # Check if the contact has at least one phone number
    if new_row['type1:number1'] or new_row['type2:number2']:
        new_rows.append(new_row)

# Sort new lines alphabetically by first name
new_rows.sort(key=lambda x: x['first_name'])

# Write to output CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=bicom_columns, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(new_rows)

print(f"Conversion complete. The contacts were saved in {output_file}. Number of contacts: {len(new_rows)}.")