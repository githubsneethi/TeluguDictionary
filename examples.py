from phonetic_dict import PhoneticDictionary, PhoneticEntry
from wiktionary_scraper import WiktionaryScraper
from data_cleaner import DataCleaner

def example_1_basic_lookup():
    # Load dictionary
    phonetic_dict = PhoneticDictionary("telugu_phonetic.json")
    
    # Lookup a word
    word = "పర్వతం"
    entries = phonetic_dict.get_word(word)
    
    if entries:
        print(f"Found {len(entries)} pronunciation(s) for '{word}':\n")
        for i, entry in enumerate(entries, 1):
            print(f"  [{i}] IPA: {entry.ipa}")
            if entry.english_meaning:
                print(f"      Meaning: {entry.english_meaning}")
            if entry.word_type:
                print(f"      Type: {entry.word_type}")
    else:
        print(f"No pronunciation found for '{word}'")


def example_2_search_operations():    
    phonetic_dict = PhoneticDictionary("telugu_phonetic.json")
    
    # Search by sound
    print("Words containing 'ə' (schwa) sound:")
    results = phonetic_dict.search("ə", by="ipa")
    for word, entry in results[:5]:
        print(f"   {word}: {entry.ipa}")
    print(f"  Total: {len(results)} words\n")
    
    # Search by prefix
    print("Words starting with 'న':")
    results = phonetic_dict.search("న", by="word")
    for word, entry in results[:5]:
        print(f"   {word}: {entry.ipa}")
    
    # Search by meaning
    print("Words related to 'time':")
    results = phonetic_dict.search("time", by="meaning")
    for word, entry in results[:5]:
        print(f"   {word}: {entry.english_meaning}")
    if results:
        print()


def example_3_statistics():  
    phonetic_dict = PhoneticDictionary("telugu_phonetic.json")
    phonetic_dict.display_stats()


def example_4_add_entries():
   phonetic_dict = PhoneticDictionary("telugu_phonetic_custom.json")

    entries_to_add = [
        PhoneticEntry(
            word="మన",
            telugu_script="మన",
            ipa="mənə",
            english_meaning="our/ours",
            word_type="pronoun",
            source="manual"
        ),
        PhoneticEntry(
            word="దిశ",
            telugu_script="దిశ",
            ipa="dɪʃə",
            english_meaning="direction",
            word_type="noun",
            source="manual"
        ),
        PhoneticEntry(
            word="రేపు",
            telugu_script="రేపు",
            ipa="reːpʊ",
            english_meaning="tomorrow",
            word_type="noun",
            source="manual"
        ),
    ]
    
    print(f"Adding {len(entries_to_add)} entries...")
    for entry in entries_to_add:
        phonetic_dict.add_entry(entry)
        print(f"  ✓ {entry.word} ({entry.ipa})")
    
    print(f"\nSaving dictionary...")
    phonetic_dict.save()
    
    print("\nDictionary contents:")
    phonetic_dict.display_stats()


def example_5_export_formats():
    phonetic_dict = PhoneticDictionary("telugu_phonetic.json")
    
    print("Exporting dictionary in multiple formats:\n")
    
    # TTS format
    phonetic_dict.export_tts_format("output_tts.txt")
    print("  Format: word\\tIPA")
    print("  Use for: Text-to-Speech systems\n")
    
    # G2P format
    phonetic_dict.export_g2p_training("output_g2p.txt")
    print("  Format: grapheme\\tphoneme")
    print("  Use for: G2P model training\n")
    
    # CSV format
    phonetic_dict.export_csv("output_phonetic.csv")
    print("  Format: Spreadsheet with all metadata")
    print("  Use for: Excel, database import\n")
    
    # Full JSON
    phonetic_dict.export_json("output_full.json")
    print("  Format: Complete JSON with timestamps")
    print("  Use for: Backup, data integration\n")


def example_6_cleaning_pipeline():
# Create dictionary with some dirty data
    phonetic_dict = PhoneticDictionary("telugu_dirty.json")
    
    # Add some entries with issues
    phonetic_dict.add_entry(PhoneticEntry(
        word="నేను",
        telugu_script="నేను",
        ipa="[neːnʊ]",  # will be cleaned as it is having brackets
        english_meaning="I/me",
        word_type="pronoun"
    ))
    
    phonetic_dict.add_entry(PhoneticEntry(
        word="ఈయ్",
        telugu_script="ఈయ్",
        ipa="invalid!!!ipa",  # Invalid IPA
        english_meaning="hey",
        word_type="interjection"
    ))
    
    phonetic_dict.add_entry(PhoneticEntry(
        word="నవు",
        telugu_script="నవు",
        ipa="navʊ",
        english_meaning="?",
        word_type="unknown_type"  # Invalid word type
    ))
    
    phonetic_dict.save()
    
    print("Dictionary before cleaning:")
    print(f"  Total entries: {sum(len(e) for e in phonetic_dict.entries.values())}\n")
    
    # Clean the data
    cleaner = DataCleaner(phonetic_dict)
    stats = cleaner.clean_dictionary(verbose=True)
    
    # Remove duplicates
    cleaner.remove_duplicates(verbose=True)
    
    phonetic_dict.save()
    
    print("\nIssues found during cleaning:")
    report = cleaner.get_issues_report()
    print(report)

def example_9_linguistic_analysis():
    phonetic_dict = PhoneticDictionary("telugu_phonetic.json")
    
    print("Analyzing phonetic patterns...\n")
    
    # Count phoneme frequencies
    phoneme_freq = {}
    for entries in phonetic_dict.entries.values():
        for entry in entries:
            ipa = entry.ipa
            for char in ipa:
                phoneme_freq[char] = phoneme_freq.get(char, 0) + 1
    
    print("Most common phonemes:")
    sorted_phonemes = sorted(phoneme_freq.items(), key=lambda x: x[1], reverse=True)
    for phoneme, count in sorted_phonemes[:10]:
        print(f"  {phoneme}: {count} occurrences")
    
    print("\n\nWord type distribution:")
    word_types = {}
    for entries in phonetic_dict.entries.values():
        for entry in entries:
            if entry.word_type:
                word_types[entry.word_type] = word_types.get(entry.word_type, 0) + 1
    
    for wtype, count in sorted(word_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  {wtype}: {count} words")


def example_10_batch_operations():
    batch_dict = PhoneticDictionary("telugu_batch.json")
    
    # Batch 1: Scrape words
    print("Batch 1: Scraping words...")
    scraper = WiktionaryScraper(batch_dict)
    words = ['రాత్రి', 'పగటి', 'ఉదయం']
    scraper.scrape_words(words)
    
    print("\nBatch 2: Cleaning data...")
    cleaner = DataCleaner(batch_dict)
    cleaner.clean_dictionary(verbose=False)
    cleaner.remove_duplicates(verbose=False)
    
    print("\nBatch 3: Exporting data...")
    batch_dict.export_tts_format("batch_tts.txt")
    batch_dict.export_csv("batch_data.csv")
    batch_dict.export_json("batch_full.json")
    
    batch_dict.display_stats()

    run_all_examples()
