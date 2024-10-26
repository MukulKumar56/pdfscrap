


import requests
from bs4 import BeautifulSoup
import os

def fetch_website_info(url):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the title of the page
        title = soup.title.string.strip() if soup.title else 'No title found'
        print(f"Title of the page: {title}")

        # Search for the <div> with id "PDFF"
        pdf_div = soup.find('div', id='PDFF')
        if pdf_div:
            source_link = pdf_div.get('source')
            if source_link:
                print(f"Source link found: {source_link}")
                download_pdf(source_link, title)
            else:
                print("No 'source' attribute found in the <div> with id 'PDFF'.")
        else:
            print("No <div> found with id 'PDFF'.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def download_pdf(pdf_url, title):
    try:
        # Send a GET request to download the PDF
        pdf_response = requests.get(pdf_url)
        pdf_response.raise_for_status()  # Raise an error for bad responses

        # Create a safe filename from the title
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_title}.pdf"

        # Save the PDF to the current directory
        with open(filename, 'wb') as pdf_file:
            pdf_file.write(pdf_response.content)
            print(f"Downloaded PDF: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the PDF: {e}")

def extract_and_format_url(user_input):
    keyword = "selfstudys.com/"
    start_index = user_input.find(keyword)

    if start_index != -1:
        # Extract the URL part after "selfstudys.com/"
        extracted_path = user_input[start_index + len(keyword):].strip()
        full_url = f"https://www.selfstudys.com/{extracted_path}"
        return full_url
    else:
        print("No valid URL found. Targeting selfstudys.com.")
        return None



if __name__ == "__main__":
    user_input = input("Please enter your request (or type 'exit' to quit): ")
    if user_input.lower() != 'exit':
        formatted_url = extract_and_format_url(user_input)
        if formatted_url:
            print(f"Extracted URL: {formatted_url}")
            fetch_website_info(formatted_url)