import pandas as pd

# File paths
input_file = r"C:/Users/shane/OneDrive/Desktop/Queer Ear/queer_tracks_ch_nmg_fixed.csv"
output_file = r"C:/Users/shane/OneDrive/Desktop/Queer Ear/artist_counts.csv"

# Load the fixed CSV
df = pd.read_csv(input_file, dtype=str)

# Split by '###', explode into individual rows, clean spaces, and count
artist_counts = (
    df["Artist"]
    .dropna()
    .str.split("###")
    .explode()
    .str.strip()
    .value_counts()
    .reset_index()
)

# Rename columns clearly
artist_counts.columns = ["Artist", "Count"]

# Export to CSV
artist_counts.to_csv(output_file, index=False, encoding="utf-8-sig")