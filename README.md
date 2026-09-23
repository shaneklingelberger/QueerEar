# QueerEar

Welcome to Queer Ear, a Logistic Regression Model to predict LGBTQ+ status based on personal music listening history.

In the queer community, there is a term, "gaydar", or the ability to predict whether someone is LGBTQ+ or not based on several different metrics: voice, clothing, culture, music taste, personality, etc. I have always been interested in perfecting my predictions, and I wondered if there was a surefire way to do it, based on music taste. Social media algorithms often use hashtags to determine the topic of a video, a post, or a comment, but different tracks don't always have these markers. 

Inspired by the hashtags, I used Spotify Web API to determine playlists with the keywords "gay", "homosexual", "pride", "lgbt", "queer" to find songs associated with those terms. This generated 4323 playlists. 

Because the Spotify Web API would not allow me to get each song’s playlist without a business account, I had to shift gears. As a result, I extracted all of the songs in each playlist with playwright.sync_api, which had its own API limitations (about 25 songs per playlist). Unfortunately, the key in order to weight him the same as other artists. This generated 27,192 tracks. 

Now, I retrieved the proportion of each artist in all of the tracks. This generated 9363 artists. Originally, I ran the model with this data, but I realized that the proportion biased more popular artists, so I had to factor popularity out. I used “https://groover.co/en/lp/free-tools/spotify-popularity-score/” and the aforementioned playwright.sync_api to get each artist’s popularity. Up until this point, I used Python with Google Gemini to help with API requests.

All I needed was test data, so I asked my friends to complete a Google Form for their LGBTQ+ status and their top artists from last year’s Spotify Wrapped, Apple Music Replay, or any equivalent. I received 60 responses. 

Finally, it was time for the model. I created the logistic regression model in R with the help of the youtube tutorial by StatQuest with Josh Starmer "https://youtu.be/C4N3_XJJ-jU?is=bOS-Adv-ET-JzPzH". The logistic regression model averages the top 3 artists' score for a user and uses that to predict the user’s LGBTQ+ status. Initially, the p-value was around 0.05, but I wanted it lower, so I adjusted the power of popularity in the formula for the score of each artist: score = (artist’s count in the playlists) / (artist’s popularity) ^ 8. Using mechanical substitution, I discovered that a power of 8 had the lowest p-value, 0.000915.

After consulting with my STAT 404 professor, Dr. Huiyan Sang, I realized that for newer editions of the model, I can collect data like gender and minutes listened to each artist for multivariate analysis. Additionally, I could have the model take in frequency/count and popularity at the same time, instead of computing a score first. As Spotify Wrapped 2026 draws nearer, I will update the model and conduct a new sample of test data.

Remark: Every time I scraped Spotify and other websites, the code often took hours at a time. So, I split up the tasks over multiple files to minimize the consequence of any minor mistakes:

1. Playlist_Finder.py -> queer_playlists.csv
2. Track_Extractor.py -> queer_playlists.csv
3. Track_Character_Cleaner.py -> queer_tracks_ch_fixed.csv
4. Track_No_Marvin_Gaye_Cleaner.py -> queer_tracks_ch_nmg_fixed.csv
5. Artist_Counter.py -> artists_counts.csv
6. Artist_Popularity_Finder.py -> artist_popularity.csv
7. Artist_Popularity_Cleaner.py -> artist_popularity_cleaned.csv
8. Google Form -> queer_ear_form_responses.csv
9. artists_counts.csv + artist_popularity_cleaned.csv + queer_ear_form_responses.csv -> Queer_Ear_Model1.R
