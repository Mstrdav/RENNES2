library(FactoMineR)
alcool <- read.csv(file = "Analyse des Données/DM/Sujet 3/alcool.csv", header = T, sep = ",")
alcool_quant <- alcool[-1]
acp <- PCA(alcool_quant, scale.unit = T)

barplot(acp$eig[,2])
