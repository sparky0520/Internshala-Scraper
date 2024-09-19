import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from extract import extract_data

csv_file = 'jobs_data_updated.csv'
sites = ["https://internshala.com/sitemap-internships.xml", "https://internshala.com/sitemap-jobs.xml"]
links = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

for i in sites:
    try:
        response = requests.get(i, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'xml')
        print("Finding locs in XML of: " + i)
        loc_tags = soup.find_all('loc')
        print(f"Appending {len(loc_tags)} job postings to links array")
        for loc in loc_tags:
            links.append(loc.string)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching site {i}: {e}")
        continue  # Skip to the next site in case of an error

print("Links extraction completed")

# Write the extracted data to CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    # Define the CSV columns
    fieldnames = [
        'Big Heading', 'Job Title', 'Company Name', 'Location', 'Stipend',
        'Salary', 'Experience Required', 'Apply By (Internship)', 'Apply By (Job)', 'Apply Link'
    ]

    # Create a CSV writer object
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Loop through the list of links and extract the data
    for link in links:
        print("Processing: " + link)
        retries = 3  # Number of retries for each request
        for attempt in range(retries):
            try:
                job_data = extract_data(link)
                writer.writerow(job_data)
                # Random delay between requests to avoid detection
                time.sleep(random.uniform(2, 5))
                break  # Exit retry loop on success
            except requests.exceptions.RequestException as e:
                print(f"Error fetching job details from {link}: {e}")
                if attempt < retries - 1:
                    sleep_time = 2 ** attempt  # Exponential backoff
                    print(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    print(f"Failed to retrieve data from {link} after {retries} attempts")
print(f"Data extraction complete. Saved to {csv_file}.")
