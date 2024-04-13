# Bitcoin Standard Mnemonic

Transform "The Bitcoin Standard" by Saifedean Ammous into more than just a gift by embedding a unique Bitcoin mnemonic seed within its pages. Highlight 12 or 24 special words throughout the book, and lead your friends and family to a delightful financial surprise waiting in a wallet formed by these words, when entered in sequence.

## Contents

- [Getting Started](#getting-started)
- [How To Use](#how-to-use)
- [Please Note](#please-note)
- [Get Involved](#get-involved)
- [Rights and Use](#rights-and-use)

## Getting Started

1. Start with cloning the project repository.
    ```bash
    git clone https://github.com/hannibalpostumus/bitcoin-standard-mnemonic.git
    ```

2. Proceed by setting up the environment and installing the required dependencies.
    ```bash
    pip install -r requirements.txt
    ```

## How To Use

1. Place the .epub file of "The Bitcoin Standard" in the /files directory. This method relies on the ePub's formatting closely matching the printed book's layout, including page numbers and chapters. The standard settings have been tweaked to match the first edition epub of The Bitcoin Standard.
2. Tweak settings in the `extract_bip_list.py` script accordingly:
    - Specify the ePub file name and its directory path.
    - Estimate the average number of words per line in the printed version.
    - Determine the exact format of the page break element within your ePub.
3. Execute `extract_bip_list.py`:
    - A CSV file with all the BIP39 words found and their locations in the book will be generated.
    - Be patient; this task is resource-intensive and may take some time.
4. Run `generate_wallet.py`:
    - Select a 12 or 24 word seed phrase within the script.
5. Highlight the book in the specified order, **front to back**. The 12/24 seed words **read from front to back** will generate a real, checksum compliant (although incredibly insecure) wallet.
6. To generate an arranged JSON list with all the BIP39 words that occur in the epub, run bip_database.py
    - The outpud for the first edition Bitcoin Standard is already included in 'bip39_word_locations.json'
7. bip_count.py is imprecise but attempts to count the number of BIP39 words that appear in the chapter bulk of any epub to give a quick idea of how many of the words are already there.

## Please Note
- The script uses Python's `secrets` library to create a seed that's random to a reasonable extent but doesn't conform to the entropy-based, BIP-approved method.
- The resultant seed will pass the checksum validation BUT it is not generated in a secure fashion!
- It's crucial to use the BIP44 standard derivation path: **m/44'/0'/0'/0/0**
- ChatGPT was heavily leveraged to save time, I take no credit for any great (or awful) coding conventions.
- The provided bip30_word_locations.csv is based on the first edition Bitcoin Standard epub. For best results, use whatever epub version you have that most closely corresponds to the printed copy you're giving away.
- This script can easily be modified for any book that is available in print and epub, provided that the page numbering has been correctly implemented and modifications have been made to the script to account for any differences.
- The word locations are only approximate - most epubs differ at least slightly from their printed counterparts. Look around +-5/10 lines for the word and you'll usually find it. An approximate average for words/line has been used to indiciate rough location.
- Only chapters are parsed to prevent anyone from having to highlight anything written by Taleb (in the first edition) - for other books, modify 'extract_bip_list.py' as required.
- The script can be expanded to search for just the 4 first letters of any BIP39 word, therefore increasing the total number of bip words.
    - An attempt has been made in 'bip_four_match.py', ammend and expand as neccesary.
- For reference, the Bitcoin Standard contains around 1100 complete words from the full 2048 list. This ammounts toa reduction in security of about 250x. Significant, but still astronomical.

## Get Involved
- This project is open for anyone interested in tweaking, improving, or playing with the concept. It's designed for fun and learning.

## Rights and Use
- Share, modify, and use as you wish. Dive into the world of Bitcoin with creativity and curiosity!
