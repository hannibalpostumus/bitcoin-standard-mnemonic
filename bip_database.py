import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import json

def load_bip39_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def is_chapter_file(item_name):
    pattern = re.compile(r'^c\d{2}\.xhtml$')
    return bool(pattern.match(item_name))

def extract_page_number(element):
    title = element.get('title', '')
    if title.isdigit():
        return int(title)
    return None  # Return None if no valid page number is found

def find_bip39_words_and_save_to_json(epub_path, bip39_words, output_path, words_per_line=11):
    book = epub.read_epub(epub_path)
    words_locations = {}

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT and is_chapter_file(item.get_name()):
            print(f"Processing chapter {item.get_name()}...")
            soup = BeautifulSoup(item.content, 'html.parser')
            current_page = 1 
            words_count_since_pagebreak = 0 

            for element in soup.find_all(['span', 'div']):  # Looking for page breaks and text in span or div tags
                if 'pagebreak' in element.get('epub:type', '') or element.get('id', '').startswith('Page_'):
                    new_page = extract_page_number(element)
                    if new_page is not None:
                        current_page = new_page
                        words_count_since_pagebreak = 0  # Reset word count for the new page
                        print(f"Debug: Page number updated to {current_page} at {element}")

                text_elements = element.text.split()
                for text in text_elements:
                    words_count_since_pagebreak += 1  # Update the word count
                    for word in bip39_words:
                        if re.fullmatch(word, text, flags=re.IGNORECASE):
                            line_number = (words_count_since_pagebreak // words_per_line) + 1
                            location = f"Page: {current_page}, Line (approx): {line_number}"
                            if word not in words_locations:
                                words_locations[word] = []
                            words_locations[word].append(location)
                            print(f"Found '{word}' in {item.get_name()}, {location}")

    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(words_locations, json_file, indent=4, ensure_ascii=False)

    print(f"Process completed. {len(words_locations)} unique BIP39 words found.")
    print(f"Word locations saved to {output_path}")

# Usage
bip39_words_path = './files/bip39.txt'
epub_path = './files/btc_std.epub'
output_path = 'bip39_word_locations.json'

bip39_words = load_bip39_words(bip39_words_path)
find_bip39_words_and_save_to_json(epub_path, bip39_words, output_path)
