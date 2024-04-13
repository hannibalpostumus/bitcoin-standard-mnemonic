import csv
import sys
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re

def load_bip39_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def is_chapter_file(item_name):
    # Adjust the pattern if chapter file naming is different
    pattern = re.compile(r'^c\d{2}\.xhtml$')
    return bool(pattern.match(item_name))

def find_bip39_words_with_approx_lines_to_csv(epub_path, bip39_words, csv_path, words_per_line=11):
    book = epub.read_epub(epub_path)
    current_page = 'Unknown'
    words_count_since_pagebreak = 0
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Word', 'Location'])

        chapter_counter = 0
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT and is_chapter_file(item.get_name()):
                chapter_counter += 1
                print(f"\rProcessing chapter {item.get_name()}...")  # Simplified progress update
                sys.stdout.flush()
                
                soup = BeautifulSoup(item.content, 'html.parser')
                # Within the BeautifulSoup parsing loop:
                for element in soup.find_all(['span', 'div']):  # Look for <span> and <div> tags which might contain page breaks
                    if 'pagebreak' in element.get('epub:type', '') or element.get('id', '').startswith('Page_'):
                        # Attempt to extract the page number from either the 'title' attribute or the 'id' attribute
                        page_number = element.get('title') or element.get('id').split('_')[-1]
                        current_page = page_number
                        words_count_since_pagebreak = 0  # Reset word count for the new page
                        print(f"Detected page break, now at page {current_page}.")  # Debug output
                        # break  # If a page break is found, no need to check further elements for this loop iteration

                    else:
                        text_elements = element.text.split()
                        for text in text_elements:
                            words_count_since_pagebreak += 1
                            for word in bip39_words:
                                if re.fullmatch(word, text, flags=re.IGNORECASE):
                                    line_number = (words_count_since_pagebreak // words_per_line) + 1
                                    location = f"Page {current_page}, Line ~{line_number}"
                                    # Record the word and its location
                                    csvwriter.writerow([word, location])
                                    # Print the found word information immediately
                                    print(f"Found '{word}' in {item.get_name()}, {location}")
                                    sys.stdout.flush()

    # Clear the last progress message and move to a new line at the end
    print("\r" + " " * 100 + "\r", end='')
    print("Process completed. Word locations saved to the CSV file.")

# Paths to your files
bip39_words_path = './files/bip39.txt'
epub_path = './files/btc_std.epub'
csv_path = 'bip39_word_locations.csv'

bip39_words = load_bip39_words(bip39_words_path)
find_bip39_words_with_approx_lines_to_csv(epub_path, bip39_words, csv_path)
