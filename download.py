import pandas as pd
import requests
import os

# Load the CSV file
file_path = 'download.csv'  # Replace with the path to your CSV file
df = pd.read_csv(file_path)

# Ensure the 'docs' directory exists
os.makedirs('docs', exist_ok=True)

# Function to download a PDF for a given NtsbNo
def download_report(Mkey):
    url = f"https://data.ntsb.gov/carol-repgen/api/Aviation/ReportMain/GenerateNewestReport/{Mkey}/pdf"
    response = requests.get(url)
    
    if response.status_code == 200:
        file_name = os.path.join('docs', f"{Mkey}.pdf")
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_name}")
    else:
        print(f"Failed to download report for NtsbNo: {Mkey}")

# Iterate over the NtsbNo column and download each report
for Mkey in df['Mkey']:
    download_report(Mkey)
