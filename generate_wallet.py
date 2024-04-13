import csv
import secrets
from mnemonic import Mnemonic

csv_path = 'bip39_word_locations.csv'
num_words = 12  # Change as required

def load_words_from_csv(csv_path, cutoff_page):
    early_words_with_locations, late_words_with_locations = [], []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            word, location = row['Word'], row['Location']
            page = int(location.split(',')[0].split(' ')[-1])
            if page <= cutoff_page:
                early_words_with_locations.append((word, location))
            else:
                late_words_with_locations.append((word, location))
    return early_words_with_locations, late_words_with_locations

def generate_mnemonic_with_locations(early_words_with_locations, late_words_with_locations):
    mnemo = Mnemonic("english")
    # Sort the early words by location
    sorted_early_words = sorted(early_words_with_locations, key=lambda wl: int(wl[1].split(',')[0].split(' ')[-1]))
    # Select 11 words from the sorted early part of the book using secure randomness
    selected_indices = sorted(secrets.randbelow(len(sorted_early_words)) for _ in range(num_words - 1))
    selected_words_with_locations = [sorted_early_words[i] for i in selected_indices]

    mnemonic, word_locations = None, []
    while not mnemonic:
        final_word_with_location = secrets.choice(late_words_with_locations)
        test_words_with_locations = selected_words_with_locations + [final_word_with_location]
        test_mnemonic = ' '.join(word for word, _ in test_words_with_locations)
        if mnemo.check(test_mnemonic):
            mnemonic = test_mnemonic
            word_locations = test_words_with_locations
    return mnemonic, word_locations

# Determine the cutoff page based on the total number of pages in the book - 1- pages at the end should be sufficient
cutoff_page = 250  # For first edition Bitcoin Standard this works well

early_words_with_locations, late_words_with_locations = load_words_from_csv(csv_path, cutoff_page)
mnemonic, word_locations = generate_mnemonic_with_locations(early_words_with_locations, late_words_with_locations)

print(f"Generated Mnemonic: {mnemonic}")
print("Words and locations for highlighting:")
for word, location in word_locations:
    print(f"'{word}' at {location}")
