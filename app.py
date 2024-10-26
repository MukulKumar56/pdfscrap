import os
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_website_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else 'No title found'

        pdf_div = soup.find('div', id='PDFF')
        if pdf_div:
            source_link = pdf_div.get('source')
            if source_link:
                return title, source_link, "PDF found and ready to download."
            else:
                return title, None, "No 'source' attribute found."
        else:
            return title, None, "No <div> found with id 'PDFF'."

    except requests.exceptions.RequestException as e:
        return None, None, f"An error occurred: {e}"

def extract_and_format_url(user_input):
    keyword = "selfstudys.com/"
    start_index = user_input.find(keyword)

    if start_index != -1:
        extracted_path = user_input[start_index + len(keyword):].strip()
        full_url = f"https://www.selfstudys.com/{extracted_path}"
        return full_url
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    user_input = ""
    formatted_url = ""
    title = ""
    pdf_link = None  # Initialize as None
    message = "Welcome! Please enter a URL from selfstudys.com to fetch the PDF."

    if request.method == 'POST':
        user_input = request.form['url']
        formatted_url = extract_and_format_url(user_input)
        
        if formatted_url:
            title, pdf_link, message = fetch_website_info(formatted_url)
        else:
            message = "No valid URL found."

    return render_template('index.html', user_input=user_input, formatted_url=formatted_url,
                           title=title, pdf_link=pdf_link, message=message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
