# Airpim Web Scraper Documentation

## Overview

This project contains a generic web scraper designed to fetch data from different websites based on user-defined models. The scraper reads configuration from a model file, which specifies the CSS selectors needed to extract relevant data from web pages. This README provides details on how to set up, configure, and run the scraper, along with an example of a specific scraper for the website "animp.it".

## File Structure

- **web_scraper_gen.py**: The main generic web scraper script.
- **animp_scraper.py**: A specific web scraper for the "animp.it" website.
- **model_ebay.txt**: Example model file for scraping eBay.
- **model_animp.txt**: Example model file for scraping "animp.it".

## Requirements

- Python 3.x
- `requests` library
- `BeautifulSoup` library (`bs4`)
- `argparse` library (standard with Python)
- `urllib3` library
- `csv` library (standard with Python)
- `subprocess` library (standard with Python)

## Installation

Install the required libraries using pip:

```bash
pip install requests beautifulsoup4 urllib3
```

## Usage

### Command Line Arguments

- `-u` or `--url`: Base URL to scrape (required).
- `-p` or `--pages`: Number of pages to scrape (default is 1).
- `-f` or `--file`: Model file (required).

### Running the Scraper

To run the web scraper:

```bash
python web_scraper_gen.py -u "<URL>" -p <NUM_PAGES> -f "<MODEL_FILE>"
```

Example:

```bash
python web_scraper_gen.py -u "https://www.ebay.it/e/campagne-speciali/apple" -p 1 -f "model_ebay.txt"
```

## Model File Structure

The model file defines the selectors for extracting data from the web pages. Below are examples of model files for eBay and "animp.it":

### model_ebay.txt

```txt
url = https://www.ebay.it/e/campagne-speciali/apple
num_pages = 1
item_selector = .s-item
title_selector = .s-item__title
price_selector = .s-item__price
link_selector = .s-item__link
```

### model_animp.txt

```txt
url = https://animp.it/associati/elenco-soci/
num_pages = 1
item_selector = .card-body
name_selector = .card-title
link_selector = .readmore a
detail_page_selector = .rightCol
detail_name_selector = h2.h4
detail_phone_selector = h3:contains('Telefono') 
detail_email_selector = h3:contains('E-mail') a
detail_website_selector = h3:contains('Sito web') a
```

## Detailed Explanation

### web_scraper_gen.py

This script is a generic web scraper that can be configured using a model file. It performs the following steps:

1. **Load the Model**: Reads the configuration from the specified model file.
2. **Fetch Pages**: Fetches the HTML content of the specified number of pages.
3. **Scrape Data**: Uses BeautifulSoup to parse the HTML and extract data based on the selectors defined in the model file.
4. **Save Data**: Saves the extracted data to a CSV file.

### animp_scraper.py

This script is a specific scraper designed to scrape member information from "animp.it". It performs the following steps:

1. **Get Member Links**: Extracts member names and links to their detail pages from the main directory page.
2. **Extract Member Info**: Visits each member's detail page and extracts information such as address, phone number, fax number, and website.
3. **Save Data**: Saves the extracted data to a CSV file.

### Example Usage

To scrape data from eBay and save it to a CSV file:

1. Create a model file (e.g., `model_ebay.txt`) with the following content:

    ```txt
    url = https://www.ebay.it/e/campagne-speciali/apple
    num_pages = 1
    item_selector = .s-item
    title_selector = .s-item__title
    price_selector = .s-item__price
    link_selector = .s-item__link
    ```
2. Create an output file (e.g., `Output.csv`) to recieve the scraped data.

3. Run the scraper:

    ```bash
    python web_scraper_gen.py -u "https://www.ebay.it/e/campagne-speciali/apple" -p 1 -f "model_ebay.txt"
    ```

## Notes

- The scraper currently ignores SSL verification warnings for simplicity. This is not recommended for production use.
- There might be a problem related to the dealing of number of pages scraped. This is currently being worked on.
- Customize the model file to suit the structure of the target website.
- Ensure that the CSS selectors in the model file accurately match the elements you wish to scrape from the target website.

## Contributions
Contributions are welcome! Feel free to submit a pull request or open an issue to discuss any changes or improvements.
