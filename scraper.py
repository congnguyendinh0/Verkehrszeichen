# -*- coding: utf-8 -*-
"""Scraper

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xLe8rmsAzAk2G4gUqkU_g6E6JkWXHnw6
"""

!pip install requests beautifulsoup4

import os
import re
import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://www.dvr.de/service/verkehrszeichen"

# Send a GET request to the website
response = requests.get(url)

# Function to sanitize filenames
def sanitize_filename(filename):
    # Remove or replace invalid characters
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# Function to download images
def download_image(img_url, title, downloaded_files):
    # Get the image content
    img_response = requests.get(img_url)
    if img_response.status_code == 200:
        # Create a sanitized filename by replacing spaces with underscores
        sanitized_title = sanitize_filename(title.replace(' ', '_'))
        filename = f"{sanitized_title}.png"
        if filename not in downloaded_files:
            # Write the image content to a file
            with open(filename, 'wb') as img_file:
                img_file.write(img_response.content)
            downloaded_files.add(filename)
            print(f"Downloaded {filename}")
        else:
            print(f"Skipping duplicate file {filename}")
    else:
        print(f"Failed to download image {img_url}")

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Set to keep track of downloaded files
    downloaded_files = set()

    # Find all 'a' elements with 'href' and 'title' attributes
    a_elements = soup.find_all('a', href=True, title=True)

    for a in a_elements:
        # Extract the href and title attributes
        href = a['href']
        title = a['title']

        # Check if the href is a link to a verkehrszeichen image
        if "/fileadmin/downloads/verkehrszeichen/" in href:
            # Construct the full image URL
            img_url = f"https://www.dvr.de{href}"
            # Download the image
            download_image(img_url, title, downloaded_files)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

from zipfile import ZipFile

# Name of the zip file
zip_filename = "verkehrszeichen_images.zip"

# Create a zip file
with ZipFile(zip_filename, 'w') as zipf:
    for filename in os.listdir('.'):
        if filename.endswith('.png'):
            zipf.write(filename)

# Download the zip file
from google.colab import files
files.download(zip_filename)