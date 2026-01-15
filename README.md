# Skin Disease Image Scraper

A Python tool to scrape medical skin disease images from Bing Images based on disease names from a text file.

## Features

- 📋 Reads 178 skin disease names from `skin_word.txt`
- 🔍 Searches Bing Images for each disease with optimized keywords
- 📁 Organizes images into separate folders per disease
- 🖼️ Downloads up to 50 images per disease (~8,900 total)
- 🎯 Focused on real patient skin photos (not diagrams)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run Full Scrape
```bash
python scrape_with_icrawler.py
```
Then type `y` when prompted to start scraping all 178 diseases.

### Test Mode (First 3 Diseases Only)
```bash
python scrape_with_icrawler.py
```
Then type `test` when prompted to scrape only the first 3 diseases.

## Configuration

Edit `scrape_with_icrawler.py` to customize:

| Variable | Default | Description |
|----------|---------|-------------|
| `IMAGES_PER_SEARCH` | 50 | Number of images per disease |
| `OUTPUT_DIR` | `scraped_images` | Output folder name |
| `USE_BING` | True | Use Bing (True) or Google (False) |

## Output Structure

```
scraped_images/
├── squamous_cell_carcinoma/
│   ├── 000001.jpg
│   ├── 000002.jpg
│   └── ...
├── basal_cell_carcinoma/
│   ├── 000001.jpg
│   └── ...
├── psoriasis/
│   └── ...
└── ... (178 disease folders)
```

## Files

| File | Description |
|------|-------------|
| `scrape_with_icrawler.py` | Main scraper script |
| `skin_word.txt` | List of 178 skin diseases with counts |
| `requirements.txt` | Python dependencies |
| `README.md` | This documentation |

## Search Query

The scraper uses this optimized query to find real patient skin photos:
```
"{disease} skin lesion patient photo close up real"
```

## Notes

- ⚠️ **Rate Limiting**: The scraper includes delays to be respectful to search engines
- 🔒 **Bing Recommended**: Google tends to block automated requests; Bing is more reliable
- 📊 **Some diseases may have fewer images** if search results are limited

## License

For educational and research purposes only.
