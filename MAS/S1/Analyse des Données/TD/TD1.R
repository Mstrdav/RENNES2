#
# Fonction de centrage réduction
#
table = data.frame(1:5, 6:10)

varemp = function(X) return(mean((X-mean(X))^2))
substract_mean = function(x) return(x - mean(x))
div_std = function(x) return(x/sqrt(varemp(x))) # sqrt var is standard deviation

cr = function(df) {
  df = apply(df, 2, substract_mean)
  return(apply(df, 2, div_std))
}

cr_scale = function(df) {
  return(scale(df, center=TRUE, scale=TRUE))
}

# EXERCICE 3

# 1. a) importer le jeu de données inertie1.csv
inertie1 = read.table("Analyse des Données/TD/inertie1.csv", sep = ";", header = TRUE)
summary(inertie1)
dim(inertie1)

# center and turn into data frame
inertie1 = as.data.frame(scale(inertie1, center=TRUE, scale=FALSE)) # pourquoi si je scale les vecteurs propres sont 1,1 et -1,1 ???

# b) tracer le jeu de données pty=s et plot avec xlim et ylim
plot(inertie1$x1, inertie1$x2, pty="s", xlim=c(-1,1), ylim=c(-1,1), xlab = "x1", ylab="x2")

# c) est-on centrés ?
print(colMeans(inertie1)) # oui

# d) calcul de l'inertie par O par sa définition
# l'inertie totale est la somme des distances entre les points et le centre O

# Calculer le carré de la distance de chaque point à l'origine (pour les données centrées)
distances_squared = inertie1$x1^2 + inertie1$x2^2
inertie_totale = sum(distances_squared) / nrow(inertie1)
print(inertie_totale)

# e) calculer via G -> la meme
# f) calcul via variables
inertie_var = sum(apply(inertie1, 2, varemp))
print(inertie_var)

# bonus : calcul via trace de matrice de covariance
# but cov in R is divided by n-1, so we need to multiply by (n-1)/n
n = nrow(inertie1)
cov_matrix = cov(inertie1) * (n-1)/n
inertie_trace = sum(diag(cov_matrix))
print(inertie_trace) 

# g) inertie projetée sur l'axe i
inertie_proj_x1 = varemp(inertie1$x1) 
inertie_proj_x2 = varemp(inertie1$x2) 
cat("inertie_proj_x1:", inertie_proj_x1, "\n")
cat("inertie_proj_x2:", inertie_proj_x2, "\n")

# h) inertie projeté sur l'axe engendré par (1,1)'
u = c(1, 1) / sqrt(2) # vecteur unitaire
projections = as.matrix(inertie1) %*% u

# affichage des projections
abline(0, 1, col="gray") # droite y=x
points(projections * u[1], projections * u[2], col="green", pch=4) # pch=4 pour croix
inertie_proj_u = varemp(projections)
print(inertie_proj_u)

# i) inertie projetée sur l'axe engendré par (1,-1)'
v = c(1, -1) / sqrt(2) # vecteur unitaire
projections_v = as.matrix(inertie1) %*% v

inertie_proj_v = varemp(projections_v)
print(inertie_proj_v)

# j) somme des inerties projetées = inertie totale
cat("Somme des inerties projetées:", inertie_proj_u + inertie_proj_v, "\n")
cat("Inertie totale:", inertie_totale, "\n")

# recherche des axes principaux
cov_inertie1 = cov(inertie1) * (n-1)/n
eigen_decomp = eigen(cov_inertie1)
print(eigen_decomp)

vecteurs_propres = eigen_decomp$vectors
valeurs_propres = eigen_decomp$values

# verification que les vecteurs propres sont orthogonaux
cat("Produit scalaire des vecteurs propres:", sum(vecteurs_propres[,1] * vecteurs_propres[,2]), "\n")
# doit être proche de 0

# ajout des axes principaux au plot
abline(0, vecteurs_propres[2,1]/vecteurs_propres[1,1], col="red") # premier axe principal
abline(0, vecteurs_propres[2,2]/vecteurs_propres[1,2], col="blue") # deuxième axe principal

### FactoMineR
library(FactoMineR)
res.pca = PCA(inertie1)

# affichage du pourcentage d'inertie des axes
print(valeurs_propres[]/sum(valeurs_propres))
