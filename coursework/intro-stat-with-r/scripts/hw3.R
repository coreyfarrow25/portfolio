# ============================================================
# Homework 3
# ============================================================

# ============================================================
# Problem 1: Read in all 8 data files
# ============================================================

data1 <- read.csv("homework_3_data_1.csv")  # International revenue 2010-2011
data2 <- read.csv("homework_3_data_2.csv")  # US revenue 2011
data3 <- read.csv("homework_3_data_3.csv")  # International revenue 2012-2017
data4 <- read.csv("homework_3_data_4.csv")  # US revenue 2012-2017
data5 <- read.csv("homework_3_data_5.csv")  # International membership 2010-2011
data6 <- read.csv("homework_3_data_6.csv")  # US membership 2011
data7 <- read.csv("homework_3_data_7.csv")  # International membership 2012-2017
data8 <- read.csv("homework_3_data_8.csv")  # US membership 2012-2017


# ============================================================
# Problem 2: Fix column name issues, then combine into
#            intermediate data frames
# ============================================================

# 2.1: data1 and data3 already share the name "Revenue" --
#      combine into int_rev (international revenue, 2010-2017)
int_rev <- rbind(data1, data3)

# 2.2: data2's column is lowercase "revenue" -- rename to match
#      data4's "Revenue", then combine into us_rev
names(data2)[names(data2) == "revenue"] <- "Revenue"
us_rev <- rbind(data2, data4)

# 2.3: data5 and data7 -- data7's column is lowercase "membership",
#      rename to "Membership" to match data5, then combine into int_mem
names(data7)[names(data7) == "membership"] <- "Membership"
int_mem <- rbind(data5, data7)

# 2.4: data6 and data8 -- data8's column is misspelled "Membershiip",
#      rename to "Membership" to match data6, then combine into us_mem
names(data8)[names(data8) == "Membershiip"] <- "Membership"
us_mem <- rbind(data6, data8)


# ============================================================
# Problem 3: Wide format
# ============================================================

# 3.1: Merge international and US revenue by Year/Quarter
rev_wide <- merge(int_rev, us_rev, by = c("Year", "Quarter"), all = TRUE)
names(rev_wide)[3:4] <- c("Int.revenue", "US.revenue")

# 3.2: Merge international and US membership by Year/Quarter
mem_wide <- merge(int_mem, us_mem, by = c("Year", "Quarter"), all = TRUE)
names(mem_wide)[3:4] <- c("Int.membership", "US.membership")

# 3.3: Combine revenue-wide and membership-wide into one table,
#      then put the columns in the requested order
stream_wide <- merge(rev_wide, mem_wide, by = c("Year", "Quarter"), all = TRUE)
stream_wide <- stream_wide[, c("Year", "Quarter", "US.membership", "US.revenue",
                                "Int.membership", "Int.revenue")]


# ============================================================
# Problem 4: Long format
# ============================================================

# 4.1 & 4.2: Tag each table with which service it belongs to
int_rev$Service <- "Int"
int_mem$Service <- "Int"
us_rev$Service  <- "US"
us_mem$Service  <- "US"

# 4.3: Stack international + US revenue rows, reorder columns
rev_long <- rbind(int_rev, us_rev)
rev_long <- rev_long[, c("Year", "Quarter", "Service", "Revenue")]

# 4.4: Stack international + US membership rows, reorder columns
mem_long <- rbind(int_mem, us_mem)
mem_long <- mem_long[, c("Year", "Quarter", "Service", "Membership")]

# 4.5: Merge revenue and membership by Year/Quarter/Service
stream_long <- merge(rev_long, mem_long, by = c("Year", "Quarter", "Service"), all = TRUE)
stream_long <- stream_long[, c("Year", "Quarter", "Service", "Membership", "Revenue")]


# ============================================================
# Problem 5: Comments
# ============================================================
# Everything after "#" is a comment -- R ignores it when running the
# script. Comments are used throughout this file to explain what each
# step does without affecting how the code executes.


# ============================================================
# Quick sanity checks
# ============================================================
head(stream_wide)
head(stream_long)
