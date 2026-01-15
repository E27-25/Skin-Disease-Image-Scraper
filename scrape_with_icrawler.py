"""
Google Images Scraper using icrawler library
More reliable and feature-rich alternative for scraping images.

Install required packages:
    pip install icrawler Pillow

Usage:
    python scrape_with_icrawler.py
"""

import os
import re
from pathlib import Path
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler


# Configuration
IMAGES_PER_SEARCH = 50  # Number of images to download per search term
OUTPUT_DIR = "scraped_images"
USE_BING = True  # Using Bing - more reliable for automated scraping


def parse_skin_words(file_path: str) -> list[str]:
    """
    Parse disease names from the skin_word.txt file.
    Extracts only the disease names (ignoring the count and header lines).
    """
    diseases = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip header lines and separators
            if not line or line.startswith('=') or line.startswith('-'):
                continue
            if 'DISEASE COUNT' in line or 'Total rows' in line or 'Unique diseases' in line:
                continue
            
            # Extract disease name (everything before the count)
            match = re.match(r'^(.+?)\s+\d+$', line)
            if match:
                disease_name = match.group(1).strip()
                if disease_name:
                    diseases.append(disease_name)
    
    return diseases


def sanitize_folder_name(name: str) -> str:
    """Create a safe folder name from disease name."""
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', name)
    safe_name = re.sub(r'[\s_]+', '_', safe_name)
    return safe_name.strip('_').lower()


def scrape_images(disease: str, output_base: Path, num_images: int, use_bing: bool = False) -> int:
    """
    Scrape images for a disease using icrawler.
    Returns the number of images downloaded.
    """
    folder_name = sanitize_folder_name(disease)
    disease_folder = output_base / folder_name
    disease_folder.mkdir(parents=True, exist_ok=True)
    
    # Add keywords to find actual patient skin photos (not diagrams/charts)
    search_query = f"{disease} skin lesion patient photo close up real"
    
    print(f"\n📍 Scraping: {disease}")
    print(f"   Query: {search_query}")
    print(f"   Folder: {folder_name}/")
    
    # Count existing images to track downloads
    existing_count = len(list(disease_folder.glob('*')))
    
    try:
        if use_bing:
            crawler = BingImageCrawler(
                storage={'root_dir': str(disease_folder)},
                downloader_threads=4,
            )
        else:
            crawler = GoogleImageCrawler(
                storage={'root_dir': str(disease_folder)},
                downloader_threads=4,
            )
        
        crawler.crawl(
            keyword=search_query,
            max_num=num_images,
            min_size=(100, 100),  # Minimum image size
        )
        
        # Count new images
        new_count = len(list(disease_folder.glob('*')))
        downloaded = new_count - existing_count
        print(f"   ✅ Downloaded {downloaded} images")
        return downloaded
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 0


def main():
    """Main function to run the scraper."""
    script_dir = Path(__file__).parent
    skin_words_file = script_dir / "skin_word.txt"
    output_dir = script_dir / OUTPUT_DIR
    
    print("=" * 60)
    print("🔬 Image Scraper for Skin Diseases (icrawler)")
    print("=" * 60)
    
    if not skin_words_file.exists():
        print(f"❌ Error: {skin_words_file} not found!")
        return
    
    diseases = parse_skin_words(skin_words_file)
    source = "Bing" if USE_BING else "Google"
    
    print(f"\n📋 Found {len(diseases)} diseases to scrape")
    print(f"📁 Output directory: {output_dir}")
    print(f"🖼️  Images per disease: {IMAGES_PER_SEARCH}")
    print(f"🔍 Search engine: {source}")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Option to limit diseases for testing
    print(f"\nDiseases to scrape (first 5 shown):")
    for d in diseases[:5]:
        print(f"   - {d}")
    if len(diseases) > 5:
        print(f"   ... and {len(diseases) - 5} more")
    
    # Ask for confirmation
    print(f"\n⚠️  This will attempt to download ~{len(diseases) * IMAGES_PER_SEARCH} images.")
    response = input("Start scraping? (y/n/test for first 3 only): ").strip().lower()
    
    if response == 'test':
        diseases = diseases[:3]
        print(f"Running test mode with first 3 diseases...")
    elif response != 'y':
        print("Cancelled.")
        return
    
    # Scrape images
    results = []
    total_downloaded = 0
    
    for i, disease in enumerate(diseases, 1):
        print(f"\n[{i}/{len(diseases)}]", end="")
        count = scrape_images(disease, output_dir, IMAGES_PER_SEARCH, USE_BING)
        results.append((disease, count))
        total_downloaded += count
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 SCRAPING SUMMARY")
    print("=" * 60)
    print(f"Total diseases processed: {len(diseases)}")
    print(f"Total images downloaded: {total_downloaded}")
    print(f"Output directory: {output_dir}")
    
    # Show diseases with no images
    failed = [(d, c) for d, c in results if c == 0]
    if failed:
        print(f"\n⚠️  Diseases with no images downloaded ({len(failed)}):")
        for disease, _ in failed:
            print(f"   - {disease}")


if __name__ == "__main__":
    main()
