# R Functions Cheat Sheet

## Getting Help
| Function | What it does |
|---|---|
| `?function_name` | Opens the help page for a function |
| `help(function_name)` | Same as `?`, opens help page |
| `example(function_name)` | Runs the example code from the help page |

## Assignment & Basics
| Function | What it does |
|---|---|
| `<-` | Assigns a value to a name (e.g., `x <- 5`) |
| `print(x)` | Prints `x` to the console |
| `class(x)` | Tells you the type/class of `x` (numeric, character, data.frame, etc.) |
| `str(x)` | Shows the structure of an object (great for data frames/lists) |
| `summary(x)` | Quick summary stats (or structure summary for non-numeric objects) |
| `rm(x)` | Removes `x` from the environment |
| `ls()` | Lists all objects currently in your environment |

## Vectors
| Function | What it does |
|---|---|
| `c(...)` | Combines values into a vector, e.g. `c(1, 2, 3)` |
| `length(x)` | Number of elements in a vector |
| `seq(from, to, by)` | Creates a sequence, e.g. `seq(1, 10, by = 2)` |
| `rep(x, times)` | Repeats `x`, e.g. `rep(1, 5)` |
| `sort(x)` | Sorts a vector |
| `unique(x)` | Returns the distinct values in `x` |
| `sum(x)` / `mean(x)` / `median(x)` | Sum / mean / median of `x` |
| `min(x)` / `max(x)` | Minimum / maximum of `x` |
| `sd(x)` / `var(x)` | Standard deviation / variance of `x` |
| `is.na(x)` | TRUE/FALSE for each missing value |
| `na.omit(x)` | Removes missing values |

## Data Frames
| Function | What it does |
|---|---|
| `data.frame(...)` | Builds a data frame from named vectors |
| `names(df)` | Gets or sets column names |
| `nrow(df)` / `ncol(df)` | Number of rows / columns |
| `dim(df)` | Both dimensions at once |
| `head(df)` / `tail(df)` | First / last 6 rows |
| `df[rows, cols]` | Subsets rows and/or columns |
| `df$col` | Accesses a single column by name |
| `rbind(df1, df2)` | Stacks rows (data frames must share column names) |
| `cbind(df1, df2)` | Binds columns side by side (same number of rows) |
| `merge(df1, df2, by = )` | Joins two data frames by matching column(s) |

## Reading & Writing Data
| Function | What it does |
|---|---|
| `read.csv("file.csv")` | Reads a CSV file into a data frame |
| `write.csv(df, "file.csv")` | Writes a data frame to a CSV file |
| `getwd()` | Shows current working directory |
| `setwd("path")` | Sets the working directory |

## Apply Family (loop-like operations)
| Function | What it does |
|---|---|
| `sapply(x, function)` | Applies a function to each element, simplifies result to a vector |
| `lapply(x, function)` | Same as `sapply`, but always returns a list |
| `apply(matrix, 1 or 2, function)` | Applies a function across rows (1) or columns (2) of a matrix/data frame |
| `tapply(x, group, function)` | Applies a function to `x`, split by `group` |

## Control Flow
| Function | What it does |
|---|---|
| `if (condition) { ... } else { ... }` | Conditional execution |
| `for (i in 1:n) { ... }` | Loops over a sequence |
| `while (condition) { ... }` | Loops while a condition is TRUE |
| `function(args) { ... }` | Defines a custom function |
| `return(x)` | Returns a value from a function |

## Plotting (base R)
| Function | What it does |
|---|---|
| `plot(x, y)` | Basic scatter plot |
| `hist(x)` | Histogram |
| `boxplot(x)` | Boxplot |
| `barplot(x)` | Bar chart |
| `abline(h = , v = )` | Adds a horizontal/vertical line to a plot |
| `legend(...)` | Adds a legend to a plot |

## Plotting (ggplot2)
| Function | What it does |
|---|---|
| `ggplot(data, aes(...))` | Starts a plot, mapping data to aesthetics |
| `geom_boxplot()` | Adds a boxplot layer |
| `geom_dotplot()` | Adds a dotplot layer |
| `geom_bar()` | Adds a bar chart layer (counts by default) |
| `geom_density()` | Adds a density curve layer |
| `geom_histogram()` | Adds a histogram layer |
| `theme_bw()` / `theme_gray()` | Preset non-data styling (background, gridlines) |
| `labs(title=, x=, y=)` | Sets titles and axis labels |
| `scale_x_continuous(breaks=)` | Controls axis breaks/labels for continuous scales |
| `scale_fill_manual()` / `scale_colour_manual()` | Manually sets fill/colour values |
| `scale_fill_viridis_d()` / `scale_color_viridis_d()` | Colorblind-friendly discrete color scales |

## Strings
| Function | What it does |
|---|---|
| `paste(...)` | Joins strings together (with a space by default) |
| `paste0(...)` | Joins strings together (no space by default) |
| `nchar(x)` | Number of characters in a string |
| `toupper(x)` / `tolower(x)` | Converts case |
| `substr(x, start, stop)` | Extracts part of a string |
| `gsub(pattern, replacement, x)` | Replaces all matches of a pattern |
| `grepl(pattern, x)` | TRUE/FALSE for whether a pattern is found |

## Packages
| Function | What it does |
|---|---|
| `install.packages("name")` | Downloads and installs a package |
| `library(name)` | Loads an installed package for use |
| `installed.packages()` | Lists all packages currently installed |

---
*This covers base R and ggplot2 functions commonly used in intro stats courses. For anything not listed, try `?function_name` in the console — it's usually the fastest way to get an answer.*
