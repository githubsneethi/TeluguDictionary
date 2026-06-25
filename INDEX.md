# Telugu Phonetic Dictionary - Complete Index

## 🔧 Programs Included

#### 1. **phonetic_dict.py** - Dictionary Manager
- `PhoneticEntry` dataclass
- `PhoneticDictionary` class
- Features:
  - Load/save operations
  - Word lookup
  - Advanced search
  - Multiple export formats

**Usage:**
```python
from phonetic_dict import PhoneticDictionary
dict = PhoneticDictionary("telugu_phonetic.json")
entries = dict.get_word("నమస్కారం")
```

#### 2. **wiktionary_scraper.py** - Data Collection
- `WiktionaryScraper` class
- Features:
  - Download Wiktionary pages
  - Extract IPA pronunciations
  - Parse definitions
  - Extract word types

**Usage:**
```python
from wiktionary_scraper import WiktionaryScraper
scraper = WiktionaryScraper(phonetic_dict)
scraper.scrape_words(['నమస్కారం', 'కనుస్సుకో'])
```

#### 3. **data_cleaner.py** - Data Quality
- `DataCleaner` class
- Features:
  - Unicode normalization
  - IPA validation
  - Duplicate removal
  - Quality reporting

**Usage:**
```python
from data_cleaner import DataCleaner
cleaner = DataCleaner(phonetic_dict)
cleaner.clean_dictionary()
cleaner.remove_duplicates()
```

---

## 📊 Generated Output Files

After running `python main.py`, you'll get:

| File | Format | Use Case |
|------|--------|----------|
| `telugu_phonetic.json` | JSON | Primary storage, easy integration |
| `telugu_phonetic.csv` | CSV | Excel, database, analysis |
| `telugu_phonetic_full.json` | JSON | Complete backup with metadata |
| `telugu_tts.txt` | Text | Text-to-Speech systems (word\tIPA) |
| `telugu_g2p.txt` | Text | G2P model training (grapheme\tphoneme) |

---

## 🚀 Quick Commands

### Installation
```bash
cd telugu_phonetic_dict
pip install -r requirements.txt
```

### Run Full Pipeline
```bash
python main.py
```

### Run Examples
```bash
python examples.py
```

### Interactive Shell
```bash
python -i main.py
```

---

## 💡 Usage Examples

### Example 1: Basic Lookup
```python
from phonetic_dict import PhoneticDictionary

dict = PhoneticDictionary("telugu_phonetic.json")
entries = dict.get_word("నమస్కారం")
for entry in entries:
    print(f"{entry.word} ({entry.ipa}): {entry.english_meaning}")
```

### Example 2: Search
```python
# Search by IPA sound
results = dict.search("ə", by="ipa")

# Search by meaning
results = dict.search("time", by="meaning")

# Search by word type
results = dict.search("noun", by="type")
```

### Example 3: Add Manual Entry
```python
from phonetic_dict import PhoneticEntry

entry = PhoneticEntry(
    word="నీవు",
    telugu_script="నీవు",
    ipa="niːvʊ",
    english_meaning="you",
    word_type="pronoun"
)
dict.add_entry(entry)
dict.save()
```

### Example 4: Export Formats
```python
# For TTS systems
dict.export_tts_format("my_tts.txt")

# For G2P training
dict.export_g2p_training("my_g2p.txt")

# To spreadsheet
dict.export_csv("my_data.csv")

# Full backup
dict.export_json("backup.json")
```

### Example 5: Data Cleaning
```python
from data_cleaner import DataCleaner

cleaner = DataCleaner(dict)
stats = cleaner.clean_dictionary()
print(f"Valid: {stats['valid_entries']}")
print(f"Removed: {stats['removed_entries']}")
```

---

## 📋 Feature Matrix

| Feature | Status | Details |
|---------|--------|---------|
| Download Wiktionary | ✅ | Full page scraping |
| Extract IPA | ✅ | International Phonetic Alphabet |
| Extract Meaning | ✅ | English definitions |
| Extract Word Type | ✅ | noun, verb, adj, etc. |
| Unicode Normalization | ✅ | NFC normalization |
| Duplicate Removal | ✅ | Efficient deduplication |
| IPA Validation | ✅ | Comprehensive checks |
| Phonetic Search | ✅ | Fast in-memory search |
| JSON Export | ✅ | Structured backup |
| CSV Export | ✅ | Spreadsheet compatible |
| TTS Format | ✅ | word → IPA mapping |
| G2P Format | ✅ | Training data |
| Statistics | ✅ | Distribution analysis |
| Error Reporting | ✅ | Detailed issues log |

---

## 🎯 Use Cases

### 1. Text-to-Speech (TTS)
- Feed `telugu_tts.txt` to TTS engine
- Maps Telugu words to phonemes

### 2. G2P Training
- Use `telugu_g2p.txt` for training data
- Train seq2seq or transformer models
- Predict pronunciations for new words

### 3. Linguistic Research
- Analyze phonetic patterns
- Study word distributions
- Export to CSV for analysis

### 4. Language Learning
- Create interactive apps
- Support pronunciation validation in speech to text models

## 📁 Project Structure

```
telugu_phonetic_dict/
├── Core Modules
│   ├── main.py                 # Main script
│   ├── phonetic_dict.py        # Dictionary class
│   ├── wiktionary_scraper.py   # Scraper class
│   └── data_cleaner.py         # Cleaner class
│
├── Configuration
│   └── requirements.txt        # Dependencies
│
├── Documentation
│   ├── INDEX.md               # This file
│   ├── QUICKSTART.md          # Quick start
│   ├── README.md              # Full docs
│   ├── PROJECT_STRUCTURE.md   # Architecture
│   └── examples.py            # Code examples
│
└── Generated Output
    ├── telugu_phonetic.json   # Main dictionary
    ├── telugu_phonetic.csv    # CSV export
    ├── telugu_tts.txt         # TTS format
    ├── telugu_g2p.txt         # G2P format
    └── telugu_phonetic_full.json
```

### Installation Steps
```bash
# 1. Navigate to project
cd telugu_phonetic_dict

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the pipeline
python main.py
```

### Verification
```bash
# Check if dictionary was created
ls -la telugu_phonetic.json

# Try importing the modules
python -c "from phonetic_dict import PhoneticDictionary; print('✓ Import successful')"
```

---

## 📊 Performance Metrics

- **Scrape per word:** 2-5 seconds (network dependent)
- **Scrape 15 words:** ~30-75 seconds total
- **Data cleaning:** <2 seconds for 100+ entries
- **Export all formats:** <1 second
- **Memory usage:** <50MB for 1000+ entries
- **Search query:** <100ms for 1000+ entries

---

## ⚠️ Troubleshooting

### Network Errors
- Check internet connection
- Wiktionary may be temporarily unavailable
- Try again later

### No Pronunciation Found
- Word may not exist on Wiktionary
- Try different words
- Check Wiktionary manually

### Unicode Issues
- Set: `export PYTHONIOENCODING=utf-8`
- Use UTF-8 compatible editor

### Import Errors
- Reinstall: `pip install -r requirements.txt`
---

## 📝 Notes for Developers

### Contributing
- Add export formats in `phonetic_dict.py`
- Adding more features related to Telugu apart from the phonemes collected from Wikitionary
- Testing the code thoroughly and improving the aspect of TTS and extend cleaner rules in `data_cleaner.py`
- As a language is quite diverse such as Telugu, incorporating the rural aspects such as different dialects (coastal Andhra Telugu, Godavari telugu, Rayalseema telugu) and slang words into the dictionary with the respective phonemes

---

## 📚 External Resources

- [Wiktionary Telugu](https://te.wiktionary.org/)
- [IPA Reference](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet)
- [Unicode References]https://www.unicode.org/charts/PDF/U0C00.pdf, https://kolichala.com/unicode2font/
- [Motivation for the project]https://medha.ciil.org/en/DesktopApplication/darpana

---

## 📞Any questions/collaboration requests?
DM at https://www.linkedin.com/in/neethi-amrutha-a2939a376/
Dhanyavadaalu!
---

**Happy building! 🎉**

*Telugu Phonetic Dictionary - Empowering speech and language technology*
