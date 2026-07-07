### Homework 5 ###
# NOTE: This script assumes "homework_5_data_1.csv" is in R's working
# directory (columns: user, rating, date, movie.id -- dates as YYYY-MM-DD).

## ----------------------------------------------------------------
## Problem 1
## ----------------------------------------------------------------

# Read in the data, keeping character columns as character (not factor)
ratings <- read.csv("homework_5_data_1.csv", header = TRUE, stringsAsFactors = FALSE)

# The date column looks like "YYYY-MM-DD", so we can pull out each
# piece with substr() and convert to numeric.
ratings$year  <- as.numeric(substr(ratings$date, 1, 4))
ratings$month <- as.numeric(substr(ratings$date, 6, 7))
ratings$day   <- as.numeric(substr(ratings$date, 9, 10))


## ----------------------------------------------------------------
## Problem 2
## ----------------------------------------------------------------

# Create a blank 100 row x 14 column data frame with the required names
ratings.summary <- data.frame(matrix(NA, nrow = 100, ncol = 14))
colnames(ratings.summary) <- c("movie.id",
                                "rating.count.all",
                                "rating.count.1s", "rating.count.2s",
                                "rating.count.3s", "rating.count.4s",
                                "rating.count.5s",
                                "rating.prop.1s", "rating.prop.2s",
                                "rating.prop.3s", "rating.prop.4s",
                                "rating.prop.5s",
                                "earliest.rating", "latest.rating")

# Unique movie ids, smallest to greatest
unique.ids <- sort(unique(ratings$movie.id))
ratings.summary$movie.id <- unique.ids

# Outer loop: one iteration per unique movie
for (i in 1:length(unique.ids)) {

  this.id    <- unique.ids[i]
  this.movie <- ratings[ratings$movie.id == this.id, ]

  # total number of ratings for this movie
  ratings.summary$rating.count.all[i] <- nrow(this.movie)

  # Find earliest/latest date WITHOUT any date-handling function.
  # Because dates are all formatted "YYYY-MM-DD", plain character
  # comparison (< and >) sorts them correctly.
  earliest <- this.movie$date[1]
  latest   <- this.movie$date[1]

  # Inner loop: iterate over every rating this movie received
  for (j in 1:nrow(this.movie)) {
    if (this.movie$date[j] < earliest) {
      earliest <- this.movie$date[j]
    }
    if (this.movie$date[j] > latest) {
      latest <- this.movie$date[j]
    }
  }

  ratings.summary$earliest.rating[i] <- earliest
  ratings.summary$latest.rating[i]   <- latest

  # Inner loop: iterate over rating levels 1-5 to get counts/proportions
  for (level in 1:5) {
    count.this.level <- sum(this.movie$rating == level)

    ratings.summary[i, paste0("rating.count.", level, "s")] <- count.this.level
    ratings.summary[i, paste0("rating.prop.",  level, "s")] <-
      count.this.level / ratings.summary$rating.count.all[i]
  }

}

# quick sanity check
head(ratings.summary)
