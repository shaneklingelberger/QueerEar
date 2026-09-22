
# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

INPUT_CSV = "C:/Users/shane/OneDrive/Desktop/Queer Ear/artist_counts.csv"      # Input CSV file name
OUTPUT_CSV = "C:/Users/shane/OneDrive/Desktop/Queer Ear/artist_popularity.csv" # Output CSV file name
ARTIST_COLUMN_NAME = "Artist"         # Column header name in your input CSV
import csv
import re
import time
from playwright.sync_api import sync_playwright


GROOVER_URL = "https://groover.co/en/lp/free-tools/spotify-popularity-score/"

def parse_popularity(text):
    match = re.search(r'(\d{1,3})\s*%', text)
    if match:
        return int(match.group(1))
    return "N/A"

def get_target_column(fieldnames):
    if not fieldnames:
        return None
    for field in fieldnames:
        clean = field.strip().lower()
        if any(keyword in clean for keyword in ["artist", "name", "band", "performer"]):
            return field
    return fieldnames[0]

def main():
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"Reading input file: {INPUT_CSV}...")
        with open(INPUT_CSV, mode="r", encoding="utf-8-sig") as infile:
            reader = csv.DictReader(infile)
            artist_col = get_target_column(reader.fieldnames)
            
            if not artist_col:
                print("[!] Error: Could not detect artist column in input CSV.")
                return
            
            print(f"Detected artist column: '{artist_col}'\n")
            
            # Load Groover tool once
            page.goto(GROOVER_URL, wait_until="domcontentloaded", timeout=25000)
            
            for idx, row in enumerate(reader, start=1):
                artist_name = row.get(artist_col, "").strip()
                if not artist_name:
                    continue
                
                print(f"[{idx}] Searching Groover for: '{artist_name}'...")
                score = "N/A"
                
                try:
                    # 1. Locate the text input field
                    input_box = page.locator("input[type='text'], input[type='search']").first
                    input_box.click()
                    input_box.fill("")
                    input_box.fill(artist_name)
                    
                    # 2. Click the orange "Check score" button shown in your screenshot
                    check_button = page.locator("button:has-text('Check score'), input[value='Check score']").first
                    if check_button.is_visible():
                        check_button.click()
                    else:
                        page.keyboard.press("Enter")
                    
                    # 3. Wait for result text containing percentage (e.g., 90%)
                    page.wait_for_timeout(3000)
                    
                    # 4. Extract body text and search for XX%
                    body_text = page.locator("body").inner_text()
                    score = parse_popularity(body_text)
                    
                except Exception as e:
                    print(f"   [!] Error retrieving score: {e}")
                
                print(f"   -> Result Score: {score}")
                results.append({
                    "Artist": artist_name,
                    "Popularity": score
                })
                
                time.sleep(0.5)
                
        browser.close()

    # Save output CSV
    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["Artist", "Popularity"])
        writer.writeheader()
        writer.writerows(results)
        
    print(f"\nDone! Saved results to: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()