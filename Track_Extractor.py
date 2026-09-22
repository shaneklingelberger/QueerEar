from playwright.sync_api import sync_playwright
import pandas as pd
import csv

playlist_df = pd.read_csv(
    r"C:/Users/shane/OneDrive/Desktop/Queer Ear/queer_playlists.csv"
)

# Only process first 3 playlists
playlist_urls = playlist_df["url"].tolist()
len_playlist_urls = len(playlist_urls)

output_file = "queer_tracks.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    # CSV header
    writer.writerow([
        "Playlist Name",
        "Playlist ID",
        "Artist",
        "Track"
    ])

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        context = browser.new_page()
        
        # Guardrail: Set a 30-second default timeout so the script never hangs forever on a broken page
        context.set_default_timeout(30000)

        for i, playlist_url in enumerate(playlist_urls):

            print(f"\nProcessing {i+1}/{len_playlist_urls}")
            print(playlist_url)

            # Extract playlist ID
            try:
                playlist_id = (
                    playlist_url
                    .split("/playlist/")[1]
                    .split("?")[0]
                )
            except Exception:
                playlist_id = ""

            context.goto(
                playlist_url,
                wait_until="domcontentloaded"
            )

            # REASONABLE TIMEOUT: Wait 1 second for elements to fully render after initial load
            context.wait_for_timeout(1000)

            # Get playlist name
            try:
                playlist_name = context.locator(
                    'meta[property="og:title"]'
                ).get_attribute("content")

            except Exception:
                playlist_name = f"Playlist_{i+1}"

            if not playlist_name:
                playlist_name = f"Playlist_{i+1}"

            print("Playlist:", playlist_name)

            seen = set()
            tracks_added = 0

            previous_count = 0
            no_change = 0

            # Scroll and collect tracks
            while no_change < 5:

                rows = context.locator(
                    '[data-testid="tracklist-row"]'
                )

                for j in range(rows.count()):

                    row = rows.nth(j)

                    try:
                        title = row.locator(
                            '[data-testid="internal-track-link"]'
                        ).inner_text()

                        artists = row.locator(
                            'a[href*="/artist/"]'
                        ).all_inner_texts()

                        # Separate multiple artists with ### instead of a comma
                        artist = "###".join(artists)

                        key = (artist, title)

                        if key not in seen:

                            seen.add(key)

                            writer.writerow([
                                playlist_name,
                                playlist_id,
                                artist,
                                title
                            ])

                            f.flush()

                            tracks_added += 1

                    except Exception:
                        continue

                # Scroll playlist
                context.mouse.wheel(0, 10000)
                
                # REASONABLE TIMEOUT: Give Spotify's lazy loader 800ms to fetch new items after scrolling
                context.wait_for_timeout(800)

                if len(seen) == previous_count:
                    no_change += 1
                else:
                    no_change = 0

                previous_count = len(seen)

            print(f"Added {tracks_added} tracks")

        browser.close()

print("\nFinished. Saved to:", output_file)