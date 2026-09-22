import pandas as pd

# 1. Read file interpreting raw bytes
df = pd.read_csv("C:/Users/shane/OneDrive/Desktop/Queer Ear/artist_popularity.csv", encoding="latin1")

# 2. Re-encode misplaced characters back to proper UTF-8
def fix_encoding(text):
    if isinstance(text, str):
        try:
            return text.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            return text
    return text

df['Artist'] = df['Artist'].apply(fix_encoding)

# 3. Save clean CSV with UTF-8 BOM so Excel/R display accent marks correctly
df.to_csv("C:/Users/shane/OneDrive/Desktop/Queer Ear/artist_popularity_cleaned.csv", index=False, encoding="utf-8-sig")

print("Fixed! Sample entries:")
print(df[df['Artist'].str.contains('Beyoncé|Reneé', na=False)])