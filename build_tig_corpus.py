from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import os

# Base URL and page range
base_url = "https://shabait.com/category/newspapers/haddas-ertra-news/page/"
start_page = 15
end_page = 41
target_year = "2023"
links = []


links_file = "newspaper_links_2023.txt"


if os.path.exists(links_file) and os.path.getsize(links_file) > 0:
    print("Loading links from file...")
    with open(links_file, "r") as file:
        links = file.read().splitlines()
else:
    print("Scraping website for links...")
    # Initialize the Selenium WebDriver (assuming you have ChromeDriver installed)
    driver = webdriver.Chrome()

    # Loop through the specified range of pages
    for page in range(start_page, end_page + 1):
        url = f"{base_url}{page}/"
        driver.get(url)
        time.sleep(3)  # Wait for JavaScript to load the content

        soup = BeautifulSoup(driver.page_source, "html.parser")
        # Find all links that match the pattern
        for a_tag in soup.find_all("a", class_="post-title post-url"):
            href = a_tag.get("href")
            if target_year in href:
                links.append(href)

    # Close the WebDriver
    driver.quit()


    with open(links_file, "w") as file:
        for link in links:
            file.write(link + "\n")


save_directory = "tig_corpus"


os.makedirs(save_directory, exist_ok=True)

# Extract and download PDFs
for link in links:
    # Extract the date from the link to construct the PDF URL
    date_part = link.split("/")[5:2:-1]
    date_str = "".join(date_part)
    
    # Construct the PDF URL (e.g., http://50.7.16.234/hadas-eritrea/haddas_eritra_29122023.pdf)
    pdf_url = f"http://50.7.16.234/hadas-eritrea/haddas_eritra_{date_str}.pdf"

    # Send a GET request to download the PDF
    response = requests.get(pdf_url)
    
    # Define the file name based on the URL
    pdf_filename = f"haddas_eritra_{date_str}.pdf"
    
    # Save the PDF to the specified directory
    with open(os.path.join(save_directory, pdf_filename), "wb") as pdf_file:
        pdf_file.write(response.content)
    
    print(f"Downloaded: {pdf_filename}")
