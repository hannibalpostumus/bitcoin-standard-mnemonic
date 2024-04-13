import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re

def load_bip39_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return set([line.strip() for line in file.readlines()])

def is_chapter_file(item_name):
    # Adjust the pattern if chapter file naming is different
    pattern = re.compile(r'^c\d{2}\.xhtml$')
    return bool(pattern.match(item_name))

def check_bip39_words_in_epub(epub_path, bip39_words):
    book = epub.read_epub(epub_path)
    found_words = set()

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT and is_chapter_file(item.get_name()):
            soup = BeautifulSoup(item.content, 'html.parser')
            text = soup.get_text().lower()  # Convert to lower case to ensure case-insensitive matching

            # Check each word only if it's not already found
            words_to_check = bip39_words - found_words
            for word in words_to_check:
                if word in text:
                    found_words.add(word)
                    # Early exit for the word if found
                    if len(found_words) == len(bip39_words):
                        break  # All words found, no need to check further
            if len(found_words) == len(bip39_words):
                break  # All words found, exit early

    print(f"Found {len(found_words)} of the {len(bip39_words)} BIP39 words in the book.")

# Example usage
bip39_words_path = './files/bip39.txt'
epub_path = './files/btc_std.epub'

bip39_words = load_bip39_words(bip39_words_path)
check_bip39_words_in_epub(epub_path, bip39_words)
