import requests  # Import the requests library to make HTTP requests
import os
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing
import csv  # Import the csv library to work with CSV files
import argparse  # Import argparse to handle command-line arguments
import warnings  # Import warnings to handle warnings
from urllib3.exceptions import InsecureRequestWarning  # Import InsecureRequestWarning to ignore insecure request warnings
import subprocess  # Import subprocess to run external processes

# Ignore insecure request warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

# Function to clear the terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to load the model from a file
def load_model(file_path):
    config = {}  # Dictionary to store the configuration
    with open(file_path, 'r') as file:  # Open the file in read mode
        for line in file:  # Iterate over each line in the file
            if line.strip() and not line.startswith('#'):  # Skip empty lines and comments
                key, value = line.strip().split('=', 1)  # Split the line into key and value
                config[key.strip()] = value.strip()  # Add key and value to the dictionary
    return config  # Return the configuration

# Function to fetch the content of a page
def fetch_page(url, headers):
    try:
        response = requests.get(url, headers=headers, verify=False)  # Make the HTTP request
        response.raise_for_status()  # Raise an exception if the request was not successful
        return response.text  # Return the page content
    except requests.exceptions.RequestException as e:  # Handle request exceptions
        # print(f"Error fetching {url}: {e}")  # Print the error
        return None  # Return None in case of error

# Function to scrape the main page
def scrape_page(html_content, config, headers, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')  # Parse the HTML content
    items = soup.select(config['item_selector'])  # Select items using the selector from the model
    data = []  # List to store data
    count = 0  # Initialize the counter
    
    main_fields = [key for key in config.keys() if key.endswith('_selector')]

    for item in items:  # Iterate over each item
        row = {}  # Dictionary to store row data
        detail_url = ''  # Initialize the detail link
        for field in main_fields:  # Iterate over main fields
            field_name = field.replace('_selector', '')  # Extract the field name
            selector = config[field]  # Get the CSS selector from the model
            element = item.select_one(selector)  # Find the element using the selector
            if field == 'link_selector' and element:  # If the field is the link
                detail_url = element.get('href', 'N/A')  # Get the link URL
                detail_url = base_url.rstrip('/') + '/' + detail_url.lstrip('/')  # Construct the full URL
                row[field_name] = detail_url  # Add the link to the row
            else:
                if not "item" in field:
                    row[field_name] = element.get_text(strip=True) if element else 'N/A'  # Get the element text

        count += 1  # Increment the counter
        print(f'Row number {count} completed.', end='\r')  # Print progress
        data.append(row)  # Add the row to the data list
    return data, main_fields  # Return the data and field names

# Function to save data to a CSV file
def save_to_csv(data, fieldnames, file_name):
    filtered_fieldnames = [field.replace('_selector', '') for field in fieldnames if 'item' not in field]
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:  # Open the CSV file in write mode
        writer = csv.DictWriter(csvfile, fieldnames=filtered_fieldnames)  # Write data to the CSV file
        writer.writeheader()  # Write the header
        for row in data:  # Iterate over the data
            filtered_row = {key: value for key, value in row.items() if 'item' not in key}
            writer.writerow(filtered_row)  # Write each row to the CSV file

# Main function
def main():
    # Headers for accessing "url = https://animp.it/associati/elenco-soci/" | Ignore if webiste != animp
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,it-IT;q=0.8,it;q=0.7,fr;q=0.6,es;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    parser = argparse.ArgumentParser(description="Web scraping tool")  # Create a parser for command-line arguments
    parser.add_argument('-u', '--url', type=str, required=True, help="Base URL to scrape")  # Add argument for URL
    parser.add_argument('-p', '--pages', type=int, default=1, help="Number of pages to scrape")  # Add argument for number of pages
    parser.add_argument('-f', '--file', type=str, required=True, help="Model file")  # Add argument for model file
    args = parser.parse_args()  # Parse command-line arguments

    config = load_model(args.file)  # Load the model from the file
    url_template = args.url  # Get the base URL from arguments
    num_pages = args.pages  # Get the number of pages from arguments
    output_file = 'Output.csv'  # Name of the output file

    all_data = []  # List to store all data
    fieldnames = []  # List to store field names

    for page_num in range(1, num_pages + 1):  # Iterate over the number of pages
        url = f"{url_template}?_pgn={page_num}"  # Construct the page URL
        if "animp" in url:
            print(f"URL: animp - Leaving main file.")
            subprocess.run(["python", "animp_scraper.py"])
            clear_terminal()
            print(f"Scraping completed.")
        else:  
            html_content = fetch_page(url, headers)  # Fetch the page content
            if html_content:
                page_data, fieldnames = scrape_page(html_content, config, headers, url_template)  # Scrape the page
                clear_terminal()  # Clear the terminal after printing
                all_data.extend(page_data)  # Add data to the list
                print(f"Scraping completed.")
            save_to_csv(all_data, fieldnames, output_file)  # Save data to the CSV file
    
    clear_terminal()  # Clear the terminal after printing    
    print(f"Data has been saved to {output_file}")  # Print confirmation message

# Main entry point
if __name__ == "__main__":
    main()  # Call the main function
