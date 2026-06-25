#!/usr/bin/env python3
"""
Main script for building a Telugu phonetic dictionary from Wiktionary.

Usage:
    python main.py
"""

import os
from phonetic_dict import PhoneticDictionary, PhoneticEntry
from wiktionary_scraper import WiktionaryScraper
from data_cleaner import DataCleaner


def sample_words():
    """Return a list of sample Telugu words to scrape."""
    return [
        'నమస్కారం',  # hello/greetings
        'భరత',  # name/India
        'కనుస్సుకో',  # to see
        'చెప్పు',  # to say
        'నీ',  # you
        'నా',  # my
        'అందరూ',  # everyone
        'ఆ',  # that
        'ఇది',  # this
        'ఎంత',  # how much
        'కుటుంబం',  # family
        'విద్య',  # education
        'పని',  # work
        'సమయం',  # time
        'ఆనందం',  # joy
    ]


def main():
    """Main workflow for building the dictionary."""
    
    print("\n" + "="*60)
    print("   Telugu Phonetic Dictionary Builder".center(60))
    print("   (Wiktionary Data Extraction & Processing)".center(60))
    print("="*60 + "\n")
    
    # Step 1: Initialize dictionary
    print("STEP 1: Initializing phonetic dictionary...")
    dict_file = "telugu_phonetic.json"
    phonetic_dict = PhoneticDictionary(dict_file)
    print(f"✓ Dictionary initialized (storage: {dict_file})\n")
    
    # Step 2: Initialize scraper
    print("STEP 2: Setting up Wiktionary scraper...")
    scraper = WiktionaryScraper(phonetic_dict)
    print("✓ Scraper ready\n")
    
    # Step 3: Scrape words
    print("STEP 3: Scraping Telugu words from Wiktionary...")
    words = sample_words()
    print(f"Preparing to scrape {len(words)} words...\n")
    
    entries = scraper.scrape_words(words)
    
    if not entries:
        print("✗ No entries were scraped. Network issue or words not found.")
        return
    
    # Step 4: Save raw data
    print("STEP 4: Saving raw scraped data...")
    phonetic_dict.save()
    print()
    
    # Step 5: Clean data
    print("STEP 5: Cleaning and validating data...")
    cleaner = DataCleaner(phonetic_dict)
    stats = cleaner.clean_dictionary(verbose=True)
    
    # Remove duplicates
    cleaner.remove_duplicates()
    
    print()
    
    # Step 6: Save cleaned data
    print("STEP 6: Saving cleaned dictionary...")
    phonetic_dict.save()
    print()
    
    # Step 7: Display statistics
    print("STEP 7: Dictionary statistics...")
    phonetic_dict.display_stats()
    
    # Step 8: Export in different formats
    print("STEP 8: Exporting dictionary in multiple formats...")
    phonetic_dict.export_tts_format("telugu_tts.txt")
    phonetic_dict.export_g2p_training("telugu_g2p.txt")
    phonetic_dict.export_csv("telugu_phonetic.csv")
    phonetic_dict.export_json("telugu_phonetic_full.json")
    print()
    
    # Step 9: Example queries
    print("STEP 9: Example queries...")
    print("-" * 60)
    
    # Search for a word
    test_word = words[0]
    result = phonetic_dict.get_word(test_word)
    if result:
        print(f"\nLookup '{test_word}':")
        for entry in result:
            print(f"  IPA: {entry.ipa}")
            if entry.english_meaning:
                print(f"  Meaning: {entry.english_meaning}")
            if entry.word_type:
                print(f"  Type: {entry.word_type}")
    
    # Search by IPA
    search_results = phonetic_dict.search("ə", by="ipa")
    if search_results:
        print(f"\nWords with 'ə' sound: {len(search_results)} found")
        for word, entry in search_results[:3]:
            print(f"  - {word}: {entry.ipa}")
    
    print("\n" + "-" * 60)
    print("\n✓ Dictionary building complete!")
    print(f"\nFiles generated:")
    print(f"  • {dict_file} - Main dictionary (JSON format)")
    print(f"  • telugu_tts.txt - TTS-ready format (word\\tIPA)")
    print(f"  • telugu_g2p.txt - G2P training format")
    print(f"  • telugu_phonetic.csv - Spreadsheet format")
    print(f"  • telugu_phonetic_full.json - Full data export")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
