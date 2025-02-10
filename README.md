# 3cx-to-bicom
This repository contains a Python script to convert contacts from 3CX to BICOM SYSTEMS format.

## Prerequisites
- Python 3.x (https://www.python.org/downloads/)
- `unidecode` library (`pip install unidecode`)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/skoozz/3cx-to-bicom
   cd 3cx-to-bicom
2. Export your 3CX contacts as .csv (Advanced > Contacts > Export)
3. Include it in this folder ("3cx-to-bicom") and rename it "contacts_3cx.csv"
4. Run the convert.py file:
    ```py
    python convert.py
5. Import the “contacts_bicom.csv” file to BICOM SYSTEMS
    ```
    1. Go to PBX Settings
    2. Click on "Business Directory" (phonebook)
    3. Click on "Import CSV" (**DISCLAIMER: this erases all of your already saved contacts**)