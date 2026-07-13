#We will first clean the data for normalization and validation

import re
import unicodedata
from phonetic_dict import PhoneticEntry, PhoneticDictionary


class DataCleaner:
    #(subset of IPA for Indian languages)
    VALID_IPA_CHARS = set(
        'əɑɑ̃ɛɛ̃ɪɪ̃ʊʊ̃ɔɔ̃ə'  # Vowels
        'pʰptbʰbɖʰɖɖ̪ʰɖ̪ɡʰɡk̚'  # Stops
        'mɱn̪ɳŋ'  # Nasals
        'ʃsʂ'  # Fricatives
        'ɦ'  # Approximants
        'jʋ'  # Glides
        'ɭlɾr'  # Liquids
        'ˈˌː'  # Suprasegmentals
        'ʲ'  # Palatalization
    )
    
    #Telugu Unicode range
    TELUGU_START = 0x0C00
    TELUGU_END = 0x0C7F
    
    def __init__(self, phonetic_dict):
        self.dict = phonetic_dict
        self.issues_log = []
    
    @staticmethod
    def is_valid_telugu(text)
        for char in text:
            code = ord(char)
            if code >= DataCleaner.TELUGU_START and code <= DataCleaner.TELUGU_END:
                return True
        return False
    
    @staticmethod
    def normalize_telugu(text: str) -> str:
    #We shall perform NFC normalization i.e. separating letters and their diacritics into distinct code points and then combining them back together
        return unicodedata.normalize('NFC', text)
    
    @staticmethod
    def clean_ipa(ipa):
        ipa = ipa.strip()
        ipa = re.sub(r'^[/\[\]]', '', ipa)  
        ipa = re.sub(r'[/\[\]]$', '', ipa) 
        
        # Remove HTML entities
        ipa = re.sub(r'&[a-z]+;', '', ipa)
        
        ipa = re.sub(r'\s+', ' ', ipa).strip()
        
        return ipa
    
    @staticmethod
    def validate_ipa(ipa):
        if not ipa or not isinstance(ipa, str):
            return False, "IPA is empty or not a string"
        
        if len(ipa) > 100:
            return False, "IPA is too long"
        
        # Check for common non-IPA characters
        if any(char in ipa for char in '[]{}()<>'):
            return False, "Contains bracketing characters"
        
        # Allow some flexibility - if it has mostly valid characters
        valid_chars = set('ə a ɛ ɪ ʊ ɔ ə ɑ ɦ k ɡ ŋ c ɲ ʨ ʤ ɖ ɳ ɡ b m j ʋ l ɭ ɾ r s ʃ ʂ ɕ ʑ ʈ ŋ̊ ˈ ˌ ː')
        
        return True, None
    
    def clean_entry(self, entry):
        errors = []
        #Steps: normalization, data cleaning, validation
        if not entry.telugu_script:
            return False, "Empty Telugu script", entry
        
        if not self.is_valid_telugu(entry.telugu_script):
            errors.append("Invalid Telugu script")
        
        entry.telugu_script = self.normalize_telugu(entry.telugu_script)
        entry.word = self.normalize_telugu(entry.word)
        
        entry.ipa = self.clean_ipa(entry.ipa)
        is_valid, error = self.validate_ipa(entry.ipa)
        if not is_valid:
            errors.append(f"Invalid IPA: {error}")
        
        # Clean meaning if present
        if entry.english_meaning:
            entry.english_meaning = entry.english_meaning.strip()
            if len(entry.english_meaning) > 200:
                entry.english_meaning = entry.english_meaning[:200]
        
        # Validate word type
        if entry.word_type:
            entry.word_type = entry.word_type.lower().strip()
            valid_types = [
                'noun', 'verb', 'adjective', 'adverb', 'pronoun',
                'preposition', 'conjunction', 'interjection'
            ]
            if entry.word_type not in valid_types:
                entry.word_type = None
        
        if errors:
            error_msg = "; ".join(errors)
            return False, error_msg, entry
        
        return True, None, entry
    
    def clean_dictionary(self, verbose):
        stats = {
            'total_entries': 0,
            'valid_entries': 0,
            'cleaned_entries': 0,
            'removed_entries': 0,
            'errors': []
        }
        
        self.issues_log = []
        entries_to_remove = []
        
        if verbose:
            print("Starting data cleaning...")
        
        for word, entries in self.dict.entries.items():
            for i, entry in enumerate(entries):
                stats['total_entries'] += 1
                
                is_valid, error, cleaned_entry = self.clean_entry(entry)
                
                if is_valid:
                    self.dict.entries[word][i] = cleaned_entry
                    stats['cleaned_entries'] += 1
                    stats['valid_entries'] += 1
                else:
                    self.issues_log.append({
                        'word': word,
                        'error': error,
                        'ipa': entry.ipa
                    })
                    stats['removed_entries'] += 1
                    entries_to_remove.append((word, i))
        
        # Removing the invalid entries
        for word, idx in sorted(entries_to_remove, reverse=True):
            del self.dict.entries[word][idx]
            if not self.dict.entries[word]:
                del self.dict.entries[word]
        
        if verbose:
            print(f"Total entries processed: {stats['total_entries']}")
            print(f"Valid entries: {stats['valid_entries']}")
            print(f"Cleaned entries: {stats['cleaned_entries']}")
            print(f"Removed entries: {stats['removed_entries']}")
            
            if self.issues_log:
                print(f"\nIssues found: {len(self.issues_log)}")
                for issue in self.issues_log[:5]:  
                    print(f"  - {issue['word']}: {issue['error']}")
                if len(self.issues_log) > 5:
                    print(f"  ... and {len(self.issues_log) - 5} more")
            
        
        return stats
    
    def remove_duplicates(self, verbose: bool = True) -> int:
        if verbose:
            print("Removing duplicates...")
        
        duplicates_removed = 0
        
        for word, entries in self.dict.entries.items():
            seen_ipas = set()
            unique_entries = []
            
            for entry in entries:
                if entry.ipa not in seen_ipas:
                    seen_ipas.add(entry.ipa)
                    unique_entries.append(entry)
                else:
                    duplicates_removed += 1
            
            self.dict.entries[word] = unique_entries
        
        if verbose:
            print(f"Removed {duplicates_removed} duplicate entries\n")
        
        return duplicates_removed
    
    def remove_stopwords(self, stopwords):
        if stopwords is None:
            stopwords = [
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
                'to', 'for', 'of', 'is', 'are', 'be', 'was', 'were'
            ]
        
        removed = 0
        words_to_remove = []
        
        for word in self.dict.entries.keys():
            if word.lower() in stopwords:
                words_to_remove.append(word)
                removed += 1
        
        for word in words_to_remove:
            del self.dict.entries[word]
        
        print(f"Removed {removed} stopwords\n")
        
        return removed
    
    def get_issues_report(self):
        if not self.issues_log:
            return "No issues found"
        
        report = ""
        
        for issue in self.issues_log:
            report += f"Word: {issue['word']}\n"
            report += f"IPA: {issue['ipa']}\n"
            report += f"Error: {issue['error']}\n\n"
        
        return report
