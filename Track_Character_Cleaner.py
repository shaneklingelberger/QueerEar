import pandas as pd


def repair_single_artist(name):
    if pd.isna(name):
        return name
    try:
        return name.encode("latin1").decode("utf-8")
    except Exception:
        return name


def repair_cell(text):
    if pd.isna(text):
        return text

    # Split multiple artists, repair each individually, then rejoin
    artists = str(text).split("###")
    repaired_artists = [repair_single_artist(a) for a in artists]
    return "###".join(repaired_artists)


df = pd.read_csv(
    "C:\Users\shane\OneDrive\Desktop\Queer Ear\queer_tracks.csv",
    dtype=str,
)

df["Artist"] = df["Artist"].apply(repair_cell)

df.to_csv(
    "C:/Users/Shane/Downloads/queer_tracks_ch_fixed",
    index=False,
    encoding="utf-8-sig",
)