import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re

def load_bip39_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # Load words and extract the first up to four letters of each word
        return set(line.strip().lower()[:4] if len(line.strip()) >= 4 else line.strip().lower() for line in file.readlines())

def is_chapter_file(item_name):
    # Adjust the pattern if chapter file naming is different
    pattern = re.compile(r'^c\d{2}\.xhtml$')
    return bool(pattern.match(item_name))

def check_bip39_words_in_epub(epub_path, bip39_words):
    book = epub.read_epub(epub_path)
    found_substrings = set()

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT and is_chapter_file(item.get_name()):
            soup = BeautifulSoup(item.content, 'html.parser')
            text = soup.get_text().lower()  # Convert to lower case to ensure case-insensitive matching

            # Split the text into words to ensure we are searching within words, not across them
            words = text.split()
            words_to_check = bip39_words - found_substrings

            for substring in words_to_check:
                for word in words:
                    if substring in word:  # Check if the substring is part of the word
                        found_substrings.add(substring)
                        break  # Stop searching once the substring is found within any word
                if len(found_substrings) == len(bip39_words):
                    break  # All substrings found, no need to check further

            if len(found_substrings) == len(bip39_words):
                break  # All substrings found, exit early

    print(f"Found {len(found_substrings)} of the {len(bip39_words)} BIP39 word substrings in the book.")

# Usage
bip39_words_path = './files/bip39.txt'
epub_path = './files/btc_std.epub'

bip39_words = load_bip39_words(bip39_words_path)
check_bip39_words_in_epub(epub_path, bip39_words)
