#!/usr/bin/env python3
"""
Advanced usage examples for the Telugu Phonetic Dictionary.
"""

from phonetic_dict import PhoneticDictionary, PhoneticEntry
from wiktionary_scraper import WiktionaryScraper
from data_cleaner import DataCleaner
from typing import List


def example_1_basic_lookup():
    """Example 1: Basic word lookup."""
    print("\n" + "="*60)
    print("Example 1: Basic Word Lookup")
    print("="*60 + "\n")
    
    # Load dictionary
    phonetic_dict = PhoneticDictionary("telugu_phonetic.json")
    
    # Lookup a word
    word = "నమస్కారం"
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
    """Example 2: Various search operations."""
    print("\n" + "="*60)
    print("Example 2: Search Operations")
    print("="*60 + "\n")
    
    phonetic_dict = PhoneticDictionary("telugu_phonetic.json")
    
    # Search by IPA sound
    print("Words containing 'ə' (schwa) sound:")
    results = phonetic_dict.search("ə", by="ipa")
    for word, entry in results[:5]:
        print(f"  • {word}: {entry.ipa}")
    print(f"  Total: {len(results)} words\n")
    
    # Search by word prefix
    print("Words starting with 'న':")
    results = phonetic_dict.search("న", by="word")
    for word, entry in results[:5]:
        print(f"  • {word}: {entry.ipa}")
    if len(results) > 5:
        print(f"  ... and {len(results) - 5} more\n")
    
    # Search by meaning
    print("Words related to 'time':")
    results = phonetic_dict.search("time", by="meaning")
    for word, entry in results[:5]:
        print(f"  • {word}: {entry.english_meaning}")
    if results:
        print()


def example_3_statistics():
    """Example 3: Dictionary statistics."""
    print("\n" + "="*60)
    print("Example 3: Dictionary Statistics")
    print("="*60 + "\n")
    
    phonetic_dict = PhoneticDictionary("telugu_phonetic.json")
    phonetic_dict.display_stats()


def example_4_add_entries():
    """Example 4: Manually add entries."""
    print("\n" + "="*60)
    print("Example 4: Adding Manual Entries")
    print("="*60 + "\n")
    
    phonetic_dict = PhoneticDictionary("telugu_phonetic_custom.json")
    
    # Create custom entries
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
    """Example 5: Export in different formats."""
    print("\n" + "="*60)
    print("Example 5: Export Formats")
    print("="*60 + "\n")
    
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
    """Example 6: Data cleaning and validation."""
    print("\n" + "="*60)
    print("Example 6: Data Cleaning Pipeline")
    print("="*60 + "\n")
    
    # Create dictionary with some "dirty" data
    phonetic_dict = PhoneticDictionary("telugu_dirty.json")
    
    # Add some entries with issues
    phonetic_dict.add_entry(PhoneticEntry(
        word="నేను",
        telugu_script="నేను",
        ipa="[neːnʊ]",  # Has brackets - will be cleaned
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
        word="నీవు",
        telugu_script="నీవు",
        ipa="niːvʊ",
        english_meaning="you",
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


def example_7_g2p_preparation():
    """Example 7: Prepare data for G2P training."""
    print("\n" + "="*60)
    print("Example 7: G2P Training Data Preparation")
    print("="*60 + "\n")
    
    phonetic_dict = PhoneticDictionary("telugu_phonetic.json")
    
    # Export in G2P format
    phonetic_dict.export_g2p_training("g2p_training_data.txt")
    
    print("G2P training file created: g2p_training_data.txt\n")
    print("Sample usage for training:")
    print("""
    # With Python + TensorFlow
    import tensorflow as tf
    from tensorflow import keras
    
    # Load G2P data
    with open('g2p_training_data.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Parse grapheme-phoneme pairs
    graphemes = []
    phonemes = []
    for line in lines:
        g, p = line.strip().split('\\t')
        graphemes.append(g)
        phonemes.append(p)
    
    # Build and train model...
    """)


def example_8_tts_integration():
    """Example 8: Prepare data for TTS system."""
    print("\n" + "="*60)
    print("Example 8: TTS Integration")
    print("="*60 + "\n")
    
    phonetic_dict = PhoneticDictionary("telugu_phonetic.json")
    
    # Export for TTS
    phonetic_dict.export_tts_format("tts_dictionary.txt")
    
    print("TTS dictionary created: tts_dictionary.txt\n")
    print("Sample usage with TTS engine:")
    print("""
    # Example: Using with a TTS library
    import phoneme_synthesizer  # Your TTS library
    
    # Load dictionary
    tts_dict = {}
    with open('tts_dictionary.txt', 'r', encoding='utf-8') as f:
        for line in f:
            word, ipa = line.strip().split('\\t')
            tts_dict[word] = ipa
    
    # Synthesize speech
    def text_to_speech(text):
        words = text.split()
        for word in words:
            if word in tts_dict:
                ipa = tts_dict[word]
                # Synthesize phonemes to speech
                phoneme_synthesizer.synthesize(ipa)
    
    text_to_speech("నమస్కారం కుటుంబం సమయం")
    """)


def example_9_linguistic_analysis():
    """Example 9: Linguistic analysis."""
    print("\n" + "="*60)
    print("Example 9: Linguistic Analysis")
    print("="*60 + "\n")
    
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
    """Example 10: Batch operations and workflows."""
    print("\n" + "="*60)
    print("Example 10: Batch Operations")
    print("="*60 + "\n")
    
    # Create a new dictionary
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
    
    print("\nBatch workflow complete!")
    batch_dict.display_stats()


def run_all_examples():
    """Run all examples."""
    print("\n\n")
    print("█" * 60)
    print("  Telugu Phonetic Dictionary - Advanced Examples".center(60))
    print("█" * 60)
    
    try:
        example_1_basic_lookup()
    except FileNotFoundError:
        print("(Skipping - dictionary not yet created)\n")
    
    try:
        example_2_search_operations()
    except FileNotFoundError:
        print("(Skipping - dictionary not yet created)\n")
    
    try:
        example_3_statistics()
    except FileNotFoundError:
        print("(Skipping - dictionary not yet created)\n")
    
    example_4_add_entries()
    example_5_export_formats()
    example_6_cleaning_pipeline()
    example_7_g2p_preparation()
    example_8_tts_integration()
    example_9_linguistic_analysis()
    example_10_batch_operations()
    
    print("\n" + "█" * 60)
    print("All examples completed!".center(60))
    print("█" * 60 + "\n")


if __name__ == "__main__":
    run_all_examples()
