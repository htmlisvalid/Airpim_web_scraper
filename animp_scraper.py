import requests  # Import the requests library to make HTTP requests
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing
import csv  # Import the csv library to work with CSV files
import warnings  # Import warnings to handle warnings
from urllib3.exceptions import InsecureRequestWarning  # Import InsecureRequestWarning to ignore insecure request warnings

warnings.simplefilter('ignore', InsecureRequestWarning)  # Ignore insecure request warnings

# Function to extract information from a member card
def extract_socio_info(socio_url):
    try:
        response = requests.get(socio_url, verify=False)  # Disable SSL verification
        soup = BeautifulSoup(response.content, 'html.parser')  # Parse the HTML content

        # Extract information
        address = soup.find_all('h3')[0].find_next_sibling(string=True).strip()  # Extract address
        phone = soup.find_all('h3')[1].find_next_sibling(string=True).strip()  # Extract phone number
        fax = soup.find_all('h3')[2].find_next_sibling(string=True).strip()  # Extract fax number
        website = soup.find_all('h3')[3].find_next_sibling('a').text.strip()  # Extract website name
        website_url = soup.find_all('h3')[3].find_next_sibling('a')['href']  # Extract website URL

        return {
            'address': address,
            'phone': phone,
            'fax': fax,
            'website': website,
            'website_url': website_url
        }
    except Exception as e:
        return None  # Return None in case of error

# Function to extract names and links to member cards from the main page
def get_socio_links_and_names(main_url):
    try:
        response = requests.get(main_url, verify=False)  # Disable SSL verification
        soup = BeautifulSoup(response.content, 'html.parser')  # Parse the HTML content

        # Find all member card links and names
        soci = []
        for entry in soup.find_all('div', class_='list-entry'):
            card = entry.find('a', class_='readmore')  # Find the member card link
            name = entry.find('h5', class_='card-title').text.strip()  # Find the member name
            if card:
                link = f"https://www.animp.it{card['href']}"  # Construct the full link
                soci.append({'name': name, 'link': link})  # Add the name and link to the list
        return soci  # Return the list of member names and links
    except Exception as e:
        print(f"Error retrieving links: {e}")  # Print the error
        return []  # Return an empty list in case of error

# Function to save data to a CSV file
def save_to_csv(data, file_name):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:  # Open the CSV file in write mode
        writer = csv.DictWriter(csvfile, fieldnames=['name', 'address', 'phone', 'fax', 'website', 'website_url'])  # Write data to the CSV file
        writer.writeheader()  # Write the header
        for row in data:  # Iterate over the data
            writer.writerow(row)  # Write each row to the CSV file

# URL of the main page listing members
main_url = "https://www.animp.it/associati/elenco-soci/"

# Get member names and links
soci_links_and_names = get_socio_links_and_names(main_url)

# Extract information for each member
soci_data = []
count = 0  # Counter for completed rows
for socio in soci_links_and_names:
    info = extract_socio_info(socio['link'])  # Extract member information
    count += 1  # Increment the counter
    print(f'Row number {count} completed.', end='\r')  # Print progress
    if info:
        info['name'] = socio['name']  # Add the member name to the info
        soci_data.append(info)  # Add the info to the data list

# Save data to a CSV file
output_file = 'Output.csv'  # Name of the output file
save_to_csv(soci_data, output_file)  # Save the data to the CSV file
