import pandas as pd

input_file = r"C:/Users/shane/OneDrive/Desktop/Queer Ear/queer_tracks_ch_fixed.csv"
output_file = r"C:/Users/shane/OneDrive/Desktop/Queer Ear/queer_tracks_ch_nmg_fixed.csv"

# Load the CSV
df = pd.read_csv(input_file, dtype=str)

# Filter out rows where "Playlist Name" contains "marvin gaye" (case-insensitive)
df_filtered = df[~df["Playlist Name"].str.contains("marvin gaye", case=False, na=False)]

# Save to the new file
df_filtered.to_csv(output_file, index=False, encoding="utf-8-sig")