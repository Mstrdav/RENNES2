galton_x = 21:15
galton_y = c(17.5, 17.3, 16, 16.3, 15.6, 16, 15.3)

plot(galton_x, galton_y)
x_mean = mean(galton_x)
y_mean = mean(galton_y)
var_x = mean((galton_x - x_mean)^2)
cov_xy = mean((galton_x - x_mean)*(galton_y - y_mean))

a = cov_xy/var_x
b = y_mean - a*x_mean

abline(b, a, col="blue", lwd=2)

model = lm(galton_y~galton_x)
print(summary(model))
abline(model$coefficients[1], model$coefficients[2], col="red", lwd=1)

# moindres carrés
y_pred = a*galton_x + b
residus = galton_y - y_pred
sse = sum(residus^2)
n = length(galton_y)
cat("somme des carrés des erreurs = ", sse)