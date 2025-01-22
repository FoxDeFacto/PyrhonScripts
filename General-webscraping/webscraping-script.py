import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time
import json
import datetime
import re

def google_search(query):
    search_results = []
    # Limit the number of results to 20 manually
    for j in search(query):
        if len(search_results) >= 20:
            break
        search_results.append(j)
    return search_results

def clean_text(text):
    # Normalize text: remove extra spaces and punctuation, and convert to lowercase
    return re.sub(r'\s+', ' ', text).strip()

def is_substring_or_similar(current_text, texts_set):
    # Check if the current text is a substring of any existing texts
    for existing_text in texts_set:
        if current_text in existing_text or existing_text in current_text:
            return True
    return False

def is_valid_text(text):
    # Check if the text has at least 4 words and no word longer than 20 characters
    words = text.split()
    return len(words) >= 4 and all(len(word) <= 20 for word in words)

def scrape_text(url, existing_texts):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check if there's a main element
        main_element = soup.find('main')
        
        if main_element:
            # If main element exists, scrape only from it
            text_elements = main_element.find_all(['div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li', 'a', 'td', 'th'])
        else:
            # If no main element, scrape from the whole page
            text_elements = soup.find_all(['div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li', 'a', 'td', 'th'])

        new_texts = []  # List for storing new unique text elements
        unique_texts_set = set(existing_texts)  # Convert existing texts to a set for quick lookup

        # Extract text from each element
        for element in text_elements:
            current_text = clean_text(element.get_text(strip=True))

            # Check if the current text is valid, not a duplicate, not a substring, and is substantial
            if current_text and is_valid_text(current_text) and not is_substring_or_similar(current_text, unique_texts_set):
                # Add a space at the end of the current text to ensure separation between elements
                current_text += ' '
                new_texts.append(current_text)
                unique_texts_set.add(current_text)

        # Join all new texts and remove any double spaces that might have been introduced
        combined_text = re.sub(r'\s+', ' ', ''.join(new_texts)).strip()

        # Split the combined text into sentences or meaningful chunks
        chunks = re.split(r'(?<=[.!?])\s+', combined_text)

        # Filter chunks again to ensure they meet the criteria
        valid_chunks = [chunk for chunk in chunks if is_valid_text(chunk)]

        return valid_chunks
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return []

def main():
    query = input("Enter your search query: ")

    print("Searching Google...")
    search_results = google_search(query)

    scraped_data = []  # List to store scraped results

    print("Scraping search results...")
    for url in search_results:
        print(f"Scraping: {url}")

        # Get existing texts for the current URL (empty if it's the first time scraping this URL)
        existing_texts = []
        for entry in scraped_data:
            if entry['url'] == url:
                existing_texts = entry['scraped_texts']
                break

        # Scrape new, unique text elements
        new_texts = scrape_text(url, existing_texts)
        # Update or append the URL data with the new unique text elements
        if new_texts:
            if existing_texts:  # If the URL already has scraped data, update it
                for entry in scraped_data:
                    if entry['url'] == url:
                        entry['scraped_texts'].extend(new_texts)
                        break
            else:  # If the URL is new, append the data as a new record
                scraped_data.append({
                    "url": url,
                    "scraped_texts": new_texts  # List of new unique elements
                })

        time.sleep(2)  # Be polite to servers

    # Save the scraped data to a JSON file with a unique timestamp-based filename
    filename = f"scraped_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, ensure_ascii=False, indent=4)

    print("Scraping completed and saved to", filename)

if __name__ == "__main__":
    main()