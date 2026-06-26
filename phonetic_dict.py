#Phonetic Dictionary to store and retrieve Telugu pronunciation data in multiple formats such as JSON, CSV


import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class PhoneticEntry:
    word: str
    telugu_script: str  # Original Telugu script
    ipa: str  # International Phonetic Alphabet
    devanagari: Optional[str] = None  # Transliteration
    english_meaning: Optional[str] = None  # English translation
    word_type: Optional[str] = None  # part of speech such as noun, verb, adjective
    source: str = "wiktionary"  # Source of the data
    timestamp: str = None  # When it was added
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class PhoneticDictionary:
    """
    Manages a phonetic dictionary for Telugu words.
    Supports storage, retrieval, and export in multiple formats.
    """
    
    def __init__(self, filepath: str = "telugu_phonetic.json"):
        """
        Initialize the phonetic dictionary.
        
        Args:
            filepath: Path to the JSON file for storing the dictionary
        """
        self.filepath = filepath
        self.entries: Dict[str, List[PhoneticEntry]] = {}
        self.load()
    
    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convert dictionaries back to PhoneticEntry objects
                    self.entries = {}
                    for word, entries in data.items():
                        self.entries[word] = [
                            PhoneticEntry(**entry) for entry in entries
                        ]
                print(f"✓ Loaded {self._total_entries()} entries from {self.filepath}")
            except Exception as e:
                print(f"✗ Error loading dictionary: {e}")
                self.entries = {}
        else:
            self.entries = {}
    
    def save(self):
        """Save dictionary to file."""
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                data = {
                    word: [asdict(entry) for entry in entries]
                    for word, entries in self.entries.items()
                }
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✓ Saved {self._total_entries()} entries to {self.filepath}")
        except Exception as e:
            print(f"✗ Error saving dictionary: {e}")
    
    def add_entry(self, entry: PhoneticEntry):
        """
        Add a single entry to the dictionary.
        
        Args:
            entry: PhoneticEntry object to add
        """
        word = entry.word
        if word not in self.entries:
            self.entries[word] = []

        existing_ipas = {e.ipa for e in self.entries[word]}
        if entry.ipa not in existing_ipas:
            self.entries[word].append(entry)
    
    def add_entries(self, entries: List[PhoneticEntry]):
        """
        Add multiple entries to the dictionary.
        
        Args:
            entries: List of PhoneticEntry objects
        """
        for entry in entries:
            self.add_entry(entry)
    
    def get_word(self, word: str) -> Optional[List[PhoneticEntry]]:
        """
        Retrieve all pronunciations for a word.
        
        Args:
            word: The word to look up
            
        Returns:
            List of PhoneticEntry objects or None if not found
        """
        return self.entries.get(word)
    
    def get_ipa(self, word: str) -> Optional[str]:
        """
        Get the IPA pronunciation for a word (first entry).
        
        Args:
            word: The word to look up
            
        Returns:
            IPA string or None if not found
        """
        entries = self.get_word(word)
        return entries[0].ipa if entries else None
    
    def search(self, query: str, by: str = "word") -> List[Tuple[str, PhoneticEntry]]:
        results = []
        query_lower = query.lower()
        
        for word, entries in self.entries.items():
            for entry in entries:
                match = False
                
                if by == "word":
                    match = query_lower in word.lower()
                elif by == "ipa":
                    match = query_lower in entry.ipa.lower()
                elif by == "meaning" and entry.english_meaning:
                    match = query_lower in entry.english_meaning.lower()
                elif by == "type" and entry.word_type:
                    match = query_lower in entry.word_type.lower()
                
                if match:
                    results.append((word, entry))
        
        return results
    
    def export_tts_format(self, filepath: str):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for word, entries in sorted(self.entries.items()):
                    # Use first (primary) pronunciation
                    ipa = entries[0].ipa
                    f.write(f"{word}\t{ipa}\n")
            print(f"Exported TTS format to {filepath}")
        except Exception as e:
            print(f"Error exporting TTS format: {e}")
    
    def export_g2p_training(self, filepath: str):
        """
        Export dictionary for G2P (Grapheme-to-Phoneme) training.
        Format: grapheme phoneme pairs per line
        
        Args:
            filepath: Output file path
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for word, entries in sorted(self.entries.items()):
                    ipa = entries[0].ipa
                    # Simple format: word IPA
                    f.write(f"{word}\t{ipa}\n")
            print(f"Exported G2P training format to {filepath}")
        except Exception as e:
            print(f"Error exporting G2P format: {e}")
    
    def export_csv(self, filepath: str):
        try:
            import csv
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Word', 'Telugu Script', 'IPA', 'Devanagari',
                    'English Meaning', 'Word Type', 'Source', 'Timestamp'
                ])
                
                for word, entries in sorted(self.entries.items()):
                    for entry in entries:
                        writer.writerow([
                            entry.word,
                            entry.telugu_script,
                            entry.ipa,
                            entry.devanagari or '',
                            entry.english_meaning or '',
                            entry.word_type or '',
                            entry.source,
                            entry.timestamp
                        ])
            print(f"Exported CSV to {filepath}")
        except Exception as e:
            print(f"Error exporting CSV: {e}")
    
    def export_json(self, filepath: str):

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                data = {
                    word: [asdict(entry) for entry in entries]
                    for word, entries in self.entries.items()
                }
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✓ Exported JSON to {filepath}")
        except Exception as e:
            print(f"✗ Error exporting JSON: {e}")
    
    def get_stats(self) -> Dict:
        total_entries = self._total_entries()
        total_words = len(self.entries)
        
        word_types = {}
        for entries in self.entries.values():
            for entry in entries:
                if entry.word_type:
                    word_types[entry.word_type] = word_types.get(entry.word_type, 0) + 1
        
        return {
            "total_words": total_words,
            "total_entries": total_entries,
            "word_types": word_types,
            "entries_per_word": total_entries / total_words if total_words > 0 else 0
        }
    
    def _total_entries(self) -> int:
        """Get total number of entries across all words."""
        return sum(len(entries) for entries in self.entries.values())
    
    def display_stats(self):
        """Display formatted statistics."""
        stats = self.get_stats()
        print("\n=== Dictionary Statistics ===")
        print(f"Total words: {stats['total_words']}")
        print(f"Total entries: {stats['total_entries']}")
        print(f"Avg entries per word: {stats['entries_per_word']:.2f}")
        if stats['word_types']:
            print("Word types:")
            for wtype, count in sorted(stats['word_types'].items()):
                print(f"  - {wtype}: {count}")
        print()
