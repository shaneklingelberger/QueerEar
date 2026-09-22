library(dplyr)

## Load Data

# Google Form responses
formdf <- read.csv("C:/Users/shane/OneDrive/Desktop/Queer Ear/queer_ear_form_responses.csv")
# Frequency of Artists in all Playlists
countsdf <- read.csv("C:/Users/shane/OneDrive/Desktop/Queer Ear/artist_counts.csv")
# Popularity of Artists
popdf <- read.csv("C:/Users/shane/OneDrive/Desktop/Queer Ear/artist_popularity_cleaned.csv")

# Remove Date as first column
formdf <- formdf[, -1]

# Rename columns
colnames(formdf) <- c("Artist 1", "Artist 2", "Artist 3", "Artist 4", "Artist 5", "status")

# removes the white space for artists "Taylor Swift " -> "Taylor Swift"
formdf[] <- lapply(formdf, function(x) if(is.character(x)) trimws(x) else x)
countsdf$Artist <- trimws(countsdf$Artist)
popdf$Artist <- trimws(popdf$Artist)

# Creates a new dataframe with the LGBTQ+ status of each person in the test data, and an empty column for their scores
calcdf <- data.frame(
  status = factor(formdf$status),
  score = NA
)

# Adjusted the formula mechanically through a "plug and chug" technique, may change in later editions
pop_power = 8
count_power = 1

# For each row (person in test data), it computes a score
for (i in 1:nrow(formdf)) {
  # Creates a list to enter in the scores for each artist for one person
  artistscores <- c()
  
  # Only looks at the first three artists
  for (j in 1:3) {
    # Grabs one artist at a time
    currentartist <- formdf[i, j]
    
    # If an artist is NA, then it assigns it a score of zero, and adds it to the list
    if (is.na(currentartist) || currentartist == "") {
      artistscores <- c(artistscores, 0)
      next
    }
    
    # Gets the row index from the countsdf that matches the current artist from the test data (case insensitive)
    row_index <- which(tolower(countsdf$Artist) == tolower(currentartist))
    
    # If there is a valid row, then...
    if (length(row_index) > 0) {
      # FORMULA: Score for each artist = Count of artist / (Popularity of artist)^pop_power
      artistscores <- c(artistscores, (countsdf$Count[row_index[1]])^count_power / (popdf$Popularity[row_index[1]])^pop_power)
    } else {
      # else, assigns a score zero if there is no match
      artistscores <- c(artistscores, 0)
    }
  }
  
  # FORMULA: User's score = Mean(Each of their artist's scores)
  calcdf[i, "score"] <- mean(artistscores) #mean
  
}

# Boxplot
plot(calcdf$score~calcdf$status)

# Plotting the logistic regression model, using code from StatQuest with Josh Starmer
# Credits: "https://youtu.be/C4N3_XJJ-jU?is=bOS-Adv-ET-JzPzH"
library(ggplot2)
library(cowplot)

calcdf$status <- factor(calcdf$status, levels = c("Not LGBTQ+", "LGBTQ+"))

logistic <- glm(status ~ score, data = calcdf, family = "binomial")

predicted.data <- data.frame(
  score = calcdf$score,
  probability.of.status = logistic$fitted.values,
  status = calcdf$status
)

ggplot(data = predicted.data, aes(x = score, y = probability.of.status)) + 
  geom_point(aes(color = status), alpha = 1, shape = 4, stroke = 2, size = 3) + 
  stat_smooth(method = "glm", method.args = list(family = "binomial"), se = FALSE, color = "black") +
  xlab("Mean Artist Score") +
  ylab("Predicted Probability of LGBTQ+ Status") +
  theme_cowplot()


## Prediction Function for NEW data (plugs in new artists into same formula)
predict_lgbtq_prob <- function(artist_list, countsdf, popdf, model, count_power, pop_power) {
  clean_input  <- trimws(tolower(artist_list))
  clean_counts <- trimws(tolower(countsdf$Artist))
  
  artist_scores <- numeric(length(clean_input))
  
  #Scores each artist in user's artist list
  for (i in seq_along(clean_input)) {
    if (clean_input[i] != "") {
      match_idx <- which(clean_counts == clean_input[i])
      
      if (length(match_idx) > 0) {
        idx <- match_idx[1]
        cnt <- countsdf$Count[idx]
        pop <- popdf$Popularity[idx]
        
        # Power dynamically applied here: (pop ^ pop_power)
        artist_scores[i] <- if (pop > 0) cnt^count_power / (pop^pop_power) else 0
      } else {
        artist_scores[i] <- 0
      }
    }
  }
  
  new_data <- data.frame(score = mean(artist_scores, na.rm = TRUE))
  prob <- predict(model, newdata = new_data, type = "response")
  
  return(unname(prob))
}

# Shows summary and significance
summary(logistic)

# The User can input their own data
user_artists <- c("Lady Gaga", "Slayyyter", "Kylie Minogue")
predict_lgbtq_prob(user_artists, countsdf, popdf, logistic, count_power, pop_power)
