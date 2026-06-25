"""
Wiktionary scraper for Telugu words and their pronunciations.
Downloads pages and extracts phonetic information.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple
import re
from urllib.parse import quote
from phonetic_dict import PhoneticEntry, PhoneticDictionary


class WiktionaryScraper:
    """Scrapes Telugu word data from Wiktionary."""
    
    BASE_URL = "https://te.wiktionary.org/wiki/"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    def __init__(self, phonetic_dict: Optional[PhoneticDictionary] = None):
        """
        Initialize the scraper.
        
        Args:
            phonetic_dict: PhoneticDictionary instance to add entries to
        """
        self.dict = phonetic_dict or PhoneticDictionary()
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def fetch_page(self, word: str) -> Optional[str]:
        """
        Fetch a Wiktionary page for a word.
        
        Args:
            word: Telugu word to fetch
            
        Returns:
            HTML content or None if failed
        """
        try:
            url = self.BASE_URL + quote(word)
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.text
            else:
                print(f"✗ Failed to fetch {word} (Status: {response.status_code})")
                return None
        except Exception as e:
            print(f"✗ Error fetching {word}: {e}")
            return None
    
    def extract_pronunciation(self, html: str) -> Optional[str]:
        """
        Extract IPA pronunciation from Wiktionary page HTML.
        
        Args:
            html: HTML content of the page
            
        Returns:
            IPA string or None
        """
        soup = BeautifulSoup(html, 'lxml')
        
        # Look for pronunciation/IPA sections
        patterns = [
            r'IPA[:\s]+([^\n<]+)',
            r'ఉచ్చారణ[:\s]+([^\n<]+)',  # Telugu word for pronunciation
            r'\/([ə a ɛ ɪ ʊ ɔ ɦ k ɡ ŋ c ɲ ɖ ɳ ɡ b m j w ɭ l ɽ r s ʃ ʈ ɾ]+)\/',
        ]
        
        # Search in the entire page text
        text = soup.get_text()
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0].strip()
        
        # Try to find in specific sections
        for section in soup.find_all(['p', 'dd', 'div']):
            section_text = section.get_text()
            if 'IPA' in section_text or 'ఉచ్చారణ' in section_text:
                for pattern in patterns:
                    matches = re.findall(pattern, section_text)
                    if matches:
                        return matches[0].strip()
        
        return None
    
    def extract_definition(self, html: str) -> Optional[str]:
        """
        Extract English definition from Wiktionary page.
        
        Args:
            html: HTML content of the page
            
        Returns:
            Definition string or None
        """
        soup = BeautifulSoup(html, 'lxml')
        
        # Look for definition sections
        for heading in soup.find_all(['h3', 'h4']):
            if 'అర్థం' in heading.get_text() or 'Definition' in heading.get_text():
                # Get the next list or paragraph
                next_elem = heading.find_next(['ul', 'ol', 'p', 'dd'])
                if next_elem:
                    text = next_elem.get_text().strip()
                    # Clean up the text
                    text = text.split('\n')[0].strip()
                    if text:
                        return text
        
        return None
    
    def extract_word_type(self, html: str) -> Optional[str]:
        """
        Extract word type (noun, verb, etc.) from Wiktionary page.
        
        Args:
            html: HTML content of the page
            
        Returns:
            Word type or None
        """
        soup = BeautifulSoup(html, 'lxml')
        
        word_types = ['noun', 'verb', 'adjective', 'adverb', 'pronoun', 'preposition']
        word_types_te = ['నామవాచకం', 'క్రియ', 'విశేషణం', 'క్రియా విశేషణం']
        
        text = soup.get_text().lower()
        
        for wtype in word_types + word_types_te:
            if wtype.lower() in text:
                return wtype
        
        return None
    
    def scrape_word(self, word: str) -> Optional[PhoneticEntry]:
        """
        Scrape a single word from Wiktionary and create a PhoneticEntry.
        
        Args:
            word: Telugu word to scrape
            
        Returns:
            PhoneticEntry or None if scraping failed
        """
        print(f"Scraping: {word}...", end=" ")
        
        html = self.fetch_page(word)
        if not html:
            print("✗")
            return None
        
        ipa = self.extract_pronunciation(html)
        if not ipa:
            print("✗ (No pronunciation found)")
            return None
        
        definition = self.extract_definition(html)
        word_type = self.extract_word_type(html)
        
        entry = PhoneticEntry(
            word=word,
            telugu_script=word,  # Already in Telugu script
            ipa=ipa,
            english_meaning=definition,
            word_type=word_type,
            source="wiktionary"
        )
        
        print(f"✓ ({ipa})")
        return entry
    
    def scrape_words(self, words: List[str]) -> List[PhoneticEntry]:
        """
        Scrape multiple words from Wiktionary.
        
        Args:
            words: List of Telugu words to scrape
            
        Returns:
            List of successfully scraped PhoneticEntry objects
        """
        entries = []
        successful = 0
        failed = 0
        
        print(f"\n{'='*50}")
        print(f"Starting to scrape {len(words)} words...")
        print(f"{'='*50}\n")
        
        for word in words:
            entry = self.scrape_word(word)
            if entry:
                entries.append(entry)
                self.dict.add_entry(entry)
                successful += 1
            else:
                failed += 1
        
        print(f"\n{'='*50}")
        print(f"Scraping complete!")
        print(f"✓ Successful: {successful}")
        print(f"✗ Failed: {failed}")
        print(f"{'='*50}\n")
        
        return entries
    
    def scrape_category(self, category: str, limit: int = 50) -> List[PhoneticEntry]:
        """
        Scrape words from a Wiktionary category.
        
        Args:
            category: Category name (e.g., "అర్థవంతమైన_పదాలు")
            limit: Maximum number of words to scrape
            
        Returns:
            List of scraped PhoneticEntry objects
        """
        print(f"\nFetching category: {category}")
        
        url = f"https://te.wiktionary.org/wiki/విభాగం:{category}"
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                print(f"✗ Failed to fetch category")
                return []
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find all word links in the category
            words = []
            for link in soup.find_all('a', limit=limit):
                href = link.get('href', '')
                if href.startswith('/wiki/') and ':' not in href:
                    word = href.replace('/wiki/', '')
                    if word and word not in words:
                        words.append(word)
            
            print(f"Found {len(words)} words in category")
            
            return self.scrape_words(words)
        
        except Exception as e:
            print(f"✗ Error fetching category: {e}")
            return []
