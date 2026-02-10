ozone <- read.table("Regression Lineraire/TP/ozone.dat", sep=" ", header = TRUE, na.strings = ".")

ozone.app <- ozone[substring(ozone[["date"]], 1, 4) != 2001,-1]
ozone.val <- ozone[substring(ozone[["date"]], 1, 4) == 2001,-1]

reg <- lm(maxO3 ~ T6 + T12 + T15 + Vx + Ne6 + Ne12 + Ne15 + maxO3v, ozone.app)
summary(reg)

residus <- rstudent(reg)
plot(residus)
# plot(fitted(reg),residus, cex=.5, ylab = "Résidus studentisés", xlab="Valeurs ajustées")
abline(h = c(2, -2), col = "red", lty = 2)
lines(loess.smooth(1:length(residus), residus), col = "blue")

# Le modèle explique bien les variable, avec un R2 de 0.6693 et un test de validité du modèle avec une p-value de 2^10-16.
# Toutes les variables ne sont pas significatives, en particulier, T15 et Ne6 ne semblent pas individuellement expliquer maxO3.

# L'hypothèse d'homoscédasticité sur les résidus semblent conforme, la courbe de lissage des résidus est proche de y=0.
# l'hypothèse de linéarité est aussi raisonnablement satisfaisante.
# Certains points sont aberrants (outliers) mais ils sont peu nombreux et pas très dangereux.

# justification des hypothèses du modèle
residus_std <- rstandard(reg)
qqnorm(residus_std)
qqline(residus_std, col = "red")
# la normalité est vérifiée (moins dans les valeurs extrêmes, mais le modèle est résistant car le nombre d'observations est grand)

shapiro.test(residus_std)
# avec un p-value > 0.05, on ne rejette pas l'hypothèse nulle H0 : les résidus suivent une distribution normale.
# on a déjà testé l'homoscédasticité avec le graphe des résidus. Il ne reste que l'indépendance

acf(residus_std, main = "Corrélogramme des Résidus Standardisés")
# Le lag0 est a 1 (logique), tous les autres sont faibles, surtout à partir de 13.

# recherche des points leviers et points influents
n <- length(residus)
seuil_cook <- 4 / n # on prend tout, et pas juste ceux supérieurs à 1
influents <- which(cooks.distance(reg) > seuil_cook)

cat("Indices des observations influentes (Cook's >", seuil_cook, "):", influents, "\n")
# Affichage du graphique de la distance de Cook
plot(cooks.distance(reg), cex=.8, main="Distance de Cook")
abline(h = seuil_cook, col = "red", lty = 2)

# et les leviers
p <- length(coef(reg))
seuil_levier <- 2 * p / n # Seuil 2p/n
leviers <- which(hatvalues(reg) > seuil_levier)

cat("Indices des observations leviers (Hat-values >", seuil_levier, "):", leviers, "\n")
plot(hatvalues(reg), cex=.8, main="Hat Values")
abline(h = seuil_levier, col="red", lty=2)

# selection de variables : on a vu que les variables Ne6 et T15 ne semblaient pas significatives. On va construire un modèle réduit sans celles-ci
reg_low <- lm(maxO3 ~ T6 + T12 + Vx + Ne12 + Ne15 + maxO3v, ozone.app)
anova(reg_low, reg) # La p-value est > 0.05, donc on ne rejette pas H0 : le modèle réduit est suffisant.

#residus_part <- resid(reg_low, type = "partial")

par(mfrow = c(2, 3)) # Configure l'affichage pour 8 graphiques (ou adaptez si votre modèle est réduit)
termplot(reg_low, 
         partial.resid = TRUE, # Trace les résidus partiels
         se = TRUE,            # Trace les barres d'erreur standard (optionnel)
         smooth = panel.smooth) # Ajoute la courbe de lissage (équivalent à loess)
par(mfrow = c(1, 1)) # Réinitialise le paramètre d'affichage
