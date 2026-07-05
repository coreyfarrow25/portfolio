# STAT 1601 - Final Grade Calculator
# Weights: Collaborative 40%, Homework 40%, Final Project 20%
# (Attendance is 0%, so it's not included)

# --- Step 1: Enter your scores and points possible ---

# Collaborative assignments (assumed worth 100 points each)
collab_score_raw       <- c(95, 88, 92, 90)
collab_points_possible <- 100 * length(collab_score_raw)

# Homework scores (points possible can differ per assignment)
hw_score_raw       <- c(85, 90, 78, 100, 95, 88, 92, 90, 85, 80, 95, 98)
hw_points_possible <- c(100, 100, 150, 100, 100, 100, 100, 100, 100, 100, 100, 200)

# Safety check: make sure every HW score has a matching points-possible entry
stopifnot(length(hw_score_raw) == length(hw_points_possible))

# Final project
final_project_score_raw       <- 90
final_project_points_possible <- 100

# --- Step 2: Convert each category to a percentage ---

collab_score        <- sum(collab_score_raw) / collab_points_possible
hw_score            <- sum(hw_score_raw) / sum(hw_points_possible)
final_project_score <- final_project_score_raw / final_project_points_possible

# --- Step 3: Apply the weights ---

w_collab  <- 0.40
w_hw      <- 0.40
w_project <- 0.20

finalGrade <- (hw_score * w_hw) + (collab_score * w_collab) + (final_project_score * w_project)
finalGrade <- finalGrade * 100   # convert from decimal to 0-100 scale

# --- Step 4: Print a breakdown ---

cat("Collaborative Assignments:", round(collab_score * 100, 2), "%\n")
cat("Homework Assignments:     ", round(hw_score * 100, 2), "%\n")
cat("Final Project:            ", round(final_project_score * 100, 2), "%\n")
cat("---------------------------------------\n")
cat("Final Grade:              ", round(finalGrade, 2), "\n")
