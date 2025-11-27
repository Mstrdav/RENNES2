library(tidyverse)
library(dplyr)
library(ggplot2)
library(gridExtra)
library(corrplot)

# data sources
# https://worldhappiness.report/
# https://data360.worldbank.org/en/indicator/WB_ESG_SM_POP_NETM
# https://data360.worldbank.org/en/indicator/WB_ESG_EN_POP_DNST
# https://data360.worldbank.org/en/indicator/WB_ESG_SH_STA_OWAD_ZS
# https://data360.worldbank.org/en/indicator/WB_ESG_SH_MED_BEDS_ZS

happiness_raw = read.csv2(file = "happiness.csv")
happiness_numeric = happiness_raw[sapply(happiness_raw, is.numeric)]
# filter obs with NA
happiness = na.omit(happiness_numeric)

# separate by year, so that happines_by_year$year becomes a data frame with all the lines of the same year
happiness_by_year = split(happiness, happiness$Year)

# remove Year column from each data frame in the list
happiness_by_year = lapply(happiness_by_year, function(df) df %>% select(-Year))

# duplicate to remove upper and lower confidence intervals
happiness_by_year = lapply(happiness_by_year, function(df) df %>% select(-c(Lower.whisker, Upper.whisker)))

# correlation matrices for each year, from 2018 to 2024, arranged in a grid
correlation_matrices = lapply(happiness_by_year, function(df) cor(df))

# shorten variables names for better display in correlation plots
shorten_names = function(corr_matrix) {
  colnames(corr_matrix) = c("Rank", "LifeEval", "LogGDP", "SocialSup", "HealthExp", "Freedom", "Generosity", "Corruption", "Dystopia")
  rownames(corr_matrix) = c("Rank", "LifeEval", "LogGDP", "SocialSup", "HealthExp", "Freedom", "Generosity", "Corruption", "Dystopia")
  return(corr_matrix)
}
correlation_matrices = lapply(correlation_matrices, shorten_names)

# setup the grid for 3x2 plots
par(mfrow = c(2, 3))

plots = function(corr_matrix, year) {
  # title below, with year, name of variables very shortened
  corrplot(corr_matrix, method = "shade", type = "lower", tl.col = "black", tl.srt = 45, title = paste("Correlation Matrix -", year), mar = c(0,0,1,0))
          
}
correlation_plots = mapply(plots, correlation_matrices, names(correlation_matrices), SIMPLIFY = FALSE)
