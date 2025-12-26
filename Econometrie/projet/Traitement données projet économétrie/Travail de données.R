'''
SOURCES


#############################################################################################

#Trop de données aberrantes
https://ourworldindata.org/grapher/meat-consumption-vs-gdp-per-capita?overlay=download-data #MeatConsumption

################################################################################################################

https://data360.worldbank.org/en/indicator/WB_ESG_SI_POV_GINI #Index distribution income
https://data360.worldbank.org/en/indicator/WB_ESG_SE_PRM_ENRR #School enrollment
https://data360.worldbank.org/en/indicator/WB_ESG_SP_DYN_LE00_IN #Lifeexpectancy
https://data360.worldbank.org/en/indicator/WB_WDI_NY_GDP_PCAP_CD #GDPpc
https://data360.worldbank.org/en/indicator/VDEM_CORE_V2X_CORR #corruption
https://ourworldindata.org/grapher/population-growth-rates?tab=map&overlay=download-data #PopulationGrowthRates
https://ourworldindata.org/grapher/military-spending-as-a-share-of-gdp-sipri?overlay=download-data #MilitayspendingPerGDP
https://ourworldindata.org/grapher/per-capita-energy-use?overlay=download-data #KwhPC
https://ourworldindata.org/grapher/annual-working-hours-vs-gdp-per-capita-pwt #annualworkhours
#Popdensity https://data360.worldbank.org/en/indicator/WB_WDI_EN_POP_DNST
#Netmigration https://data360.worldbank.org/en/indicator/WB_WDI_SM_POP_NETM
#Overweight https://data360.worldbank.org/en/indicator/WB_HNP_SH_STA_OWAD_ZS
'''



#################################### Importation de données #######################################


popgrowth = read.csv("popgrowth.csv", dec= ".", header = TRUE, sep = ",")
popgrowth = popgrowth[which(popgrowth$Year >= 2013, arr.ind = TRUE),]
popgrowth = popgrowth[which(popgrowth$Year <= 2023, arr.ind = TRUE),]
summary(popgrowth)
View(popgrowth)
popgrowth_moyenne = tapply(popgrowth$Growth, popgrowth$Code, mean, na.rm=TRUE)
popgrowth_moyenne = as.data.frame.table(popgrowth_moyenne)
names(popgrowth_moyenne) = c('Code', "Pop_Growth")
anyNA(popgrowth_moyenne) #pas de NA
dim(popgrowth_moyenne) #239
View(popgrowth_moyenne)


popgrowth = popgrowth[which(popgrowth$Year == 2023, arr.ind = TRUE),]
dim(popgrowth)

militarydepense = read.csv("militaryspendingpgdp.csv", dec= ".", header = TRUE, sep = ",")
summary(militarydepense)
View(militarydepense)
militarydepense = militarydepense[which(militarydepense$Year >= 2013 & militarydepense$Year <=2023, arr.ind = TRUE),]
militarydepense_moyenne = tapply(militarydepense$Military.expenditure, militarydepense$Code, mean, na.rm=TRUE)
militarydepense_moyenne = as.data.frame.table(militarydepense_moyenne)
summary(militarydepense_moyenne) # 252   NA's   :97 -> 155 left
names(militarydepense_moyenne) = c('Code', "Military_expenditure")
View(militarydepense_moyenne)
militarydepense_moyenne = na.omit(militarydepense_moyenne)
dim(militarydepense_moyenne)
anyNA(militarydepense_moyenne)

energyconsumption = read.csv("per-capita-energy-use.csv", dec= ".", header = TRUE, sep = ",")
summary(energyconsumption)
View(energyconsumption)
energyconsumption = energyconsumption[which(energyconsumption$Year >= 2013 & energyconsumption$Year <=2023, arr.ind = TRUE),]
energyconsumption_moyenne = tapply(energyconsumption$KWHpppc, energyconsumption$Code, mean, na.rm=TRUE)
energyconsumption_moyenne = as.data.frame.table(energyconsumption_moyenne)
names(energyconsumption_moyenne) = c('Code', "KWH_pp_pc")
energyconsumption_moyenne = replace(energyconsumption_moyenne, which(energyconsumption_moyenne == 0, arr.ind=TRUE), NA)
summary(energyconsumption_moyenne) # 213     NA's   :6  -> 207 left
View(energyconsumption_moyenne)
energyconsumption_moyenne = na.omit(energyconsumption_moyenne)
dim(energyconsumption_moyenne)




############################################################ Données moins reloues

popdensity = read.csv("density.csv", sep = ",", dec = ".", header = TRUE)
popdensity = popdensity[,-c(1,2,5:68)]
summary(popdensity)
View(popdensity)
anyNA(popdensity) #Pas de moyennage, on a 2021 pour 239 pays
dim(popdensity)
popdensity$moyennes = rowMeans(popdensity[,3:11], na.rm=TRUE) # 2013 à 2021
popdensity_moyenne = popdensity[,-c(2:11)]
View(popdensity_moyenne)
names(popdensity_moyenne) = c("Code", "Population_density")

overweight = read.csv("overweight.csv", sep = ",", dec = ".", header = TRUE)
overweight = overweight[,-c(1,2,5:46)]
summary(overweight)
View(overweight)
anyNA(overweight) #Pas de moyennage, on a 2016 pour 234 pays
dim(overweight)
overweight$overweight_moyenne = rowMeans(overweight[,11:14], na.rm=TRUE) #2013 à 2016
overweight_moyenne = overweight[,c(1,15)]
names(overweight_moyenne) = c("Code", "Overweight")
View(overweight_moyenne)


migration = read.csv("netmigration.csv", sep = ",", dec = ".", header = TRUE, na.strings = 0)
migration = migration[,-c(1,2,5:67)]
migration = replace(migration, which(migration == 0, arr.ind=TRUE), NA)
summary(migration)
View(migration)
migration$moyennes = rowMeans(migration[,5:12], na.rm=TRUE) #2013 à 2020
sum(is.na(migration$moyennes)) #On a des moyennes pour 238 pays mais certaines lignes sont louches comme Barbados ou Grenada
migration_moyenne = migration[,c(1,13)]
names(migration_moyenne) = c("Code", "Netmigration")
migration_moyenne=na.omit(migration_moyenne)
View(migration_moyenne)
dim(migration_moyenne)
anyNA(migration_moyenne)

primaryschool = read.csv("Primary school enrollment.csv", sep = ",", dec = ".", header = TRUE)
primaryschool = primaryschool[,-c(1,2,5:61)]
summary(primaryschool)
View(primaryschool)
primaryschool$moyennes = rowMeans(primaryschool[,3:12], na.rm=TRUE) #2013 à 2022
sum(is.na(primaryschool$moyennes)) #9 lignes vides => 230 pays utilisables avec moyennes
primaryschool_moyenne = primaryschool[,c(1,13)]
names(primaryschool_moyenne) = c("Code", "PrimarySchool_enrollment")
primaryschool_moyenne = na.omit(primaryschool_moyenne)
dim(primaryschool_moyenne)
View(primaryschool_moyenne)

lifespan = read.csv("Life expectancy.csv", sep = ",", dec = ".", header = TRUE)
lifespan = lifespan[,-c(1,2,5:69)]
summary(lifespan)
View(lifespan) #juste 2020 utilisable, pas de moyenne
lifespan$moyennes = rowMeans(lifespan[,3:10], na.rm=TRUE) #2013 à 2020
lifespan_moyenne = lifespan[,c(1,11)]
names(lifespan_moyenne) = c("Code", "Lifespan_At_Birth")
anyNA(lifespan_moyenne) 
lifespan_moyenne = na.omit(lifespan_moyenne)
dim(lifespan_moyenne) #235
View(lifespan_moyenne)

GDP = read.csv("GDP per capita.csv", sep = ",", dec = ".", header = TRUE)
GDP = GDP[,-c(1,2,5:75)]
summary(GDP)
View(GDP) #manque que le venezuela 
GDP$moyennes = rowMeans(GDP[,3:13], na.rm=TRUE) #2013 à 2023
sum(is.na(GDP$moyennes)) #2 lignes vides => 260 pays utilisables avec moyennes
GDP_moyenne = GDP[,c(1,15)]
GDP_moyenne = na.omit(GDP_moyenne)
names(GDP_moyenne) = c("Code", "GDP_per_capita")
dim(GDP_moyenne)
View(GDP_moyenne)


corruptionindex = read.csv("Political corruption index.csv", sep = ",", dec = ".", header = TRUE)
corruptionindex = corruptionindex[,-c(1,2,5:240)]
summary(corruptionindex)
View(corruptionindex)
anyNA(corruptionindex) 
dim(corruptionindex)
corruptionindex$moyennes = rowMeans(corruptionindex[,3:13], na.rm=TRUE) #2013 à 2023
corruptionindex_moyenne = corruptionindex[,c(1,15)]
corruptionindex_moyenne = na.omit(corruptionindex_moyenne)
names(corruptionindex_moyenne) = c("Code", "PoliticalCorruption_Index")
dim(corruptionindex_moyenne)
View(corruptionindex_moyenne)


# incomedistributionindex  corruptionindex  GDP  lifespan  netmigration   overweight  popdensity   annualworkhours   energyconsumption   militarydepense   popgrowth
variables = list(corruptionindex_moyenne,GDP_moyenne,lifespan_moyenne,migration_moyenne,overweight_moyenne,popdensity_moyenne,energyconsumption_moyenne,militarydepense_moyenne,popgrowth_moyenne, primaryschool_moyenne)

library(purrr)
CombinedTrue = purrr::reduce(.x = variables, merge, by = c('Code'), all = T)
CombinedFalse = purrr::reduce(.x = variables, merge, by = c('Code'), all = F)
dim(CombinedTrue)
dim(CombinedFalse) #105 mais 123 sans le Gini income distribution index et 127 sans le annualworkhours



dim(purrr::reduce(.x = list(corruptionindex_moyenne,GDP_moyenne,lifespan_moyenne,migration_moyenne,overweight_moyenne,popdensity_moyenne,energyconsumption_moyenne,militarydepense_moyenne,popgrowth_moyenne), merge, by = c('Code'), all = F))

CombinedFalse = purrr::reduce(.x = list(corruptionindex_moyenne,GDP_moyenne,lifespan_moyenne,migration_moyenne,overweight_moyenne,popdensity_moyenne,energyconsumption_moyenne,militarydepense_moyenne,popgrowth_moyenne), merge, by = c('Code'), all = F)
View(CombinedFalse)

###########################################################################

popdensity = read.csv("density.csv", sep = ",", dec = ".", header = TRUE)
countrynames = popdensity[,c(3,4)]
names(countrynames) = c("Code", "Country.name")
View(countrynames)
##########################################################################

happiness = read.csv("WorldHappinessIndex.csv", sep  =";", dec  =",", header = TRUE)
summary(happiness)
View(happiness)
happiness = happiness[which(happiness$Year >= 2013 & happiness$Year <=2023, arr.ind = TRUE),]

happiness_moyenne = tapply(happiness$Life.evaluation..3.year.average., happiness$Country.name, mean, na.rm=TRUE)
happiness_moyenne = as.data.frame(happiness_moyenne)z
library(tibble)
happiness_moyenne <- tibble::rownames_to_column(happiness_moyenne, "Country.name")
anyNA(happiness_moyenne)
summary(happiness_moyenne)
View(happiness_moyenne)
dim(happiness_moyenne)

don = merge(countrynames,CombinedFalse, by = c("Code"))
  purrr::reduce(.x = list(countrynames, CombinedFalse), merge, by = c('Code'), all = T)
View(don)
donnees = purrr::reduce(.x = list(don, happiness_moyenne), merge, by = c('Country.name'), all = T)
donnees = as.data.frame(donnees)
summary(donnees)
donnees = na.omit(donnees)
View(donnees)

################################################################################


donnees$happiness_moyenne2 =donnees$happiness_moyenne
donnees = donnees[,-13]
donnees$happiness_moyenne =donnees$happiness_moyenne2
donnees = donnees[,-14]


#write.csv(donnees, "donnees.csv")
donnees = read.csv("donnees.csv", sep =",", dec=".", header = TRUE)

dim(donnees)
######################################################################

OCDE_countries = c("Australia","Austria","Belgium","Canada","Chile","Colombia","Costa Rica","Czechia","Denmark","Estonia","Finland","France","Germany","Greece","Hungary","Iceland","Israel","Italy","Japan","Korea","Latvia","Lithuania","Luxembourg","Mexico","Netherlands","New Zealand","Norway","Poland","Portugal","Slovak Republic","Slovenia","Spain","Sweden","Switzerland","Türkiye","United Kingdom","United States")
donnees$OCDE = 0
for (i in 1:nrow(donnees)){ if (donnees$Country.name[i] %in% OCDE_countries) {
  donnees$OCDE[i] = 1
}}


########################################################################
#RENAME
View(donnees)
donnees = donnees[,-1]
names(donnees) = c("Name", "Code", "Political_Corruption","GDP_per_Capita","Lifespan","Net_Migration","Overweight_Adults","Population_Density","KWH_pp_pc","Military_Expenses","Population_Growth","Primary_School_Enrollment","OCDE","Happiness")


########################################################################


Startcountries = read.csv("WorldHappinessIndex.csv", sep  =";", dec  =",", header = TRUE)
Startcountries = Startcountries[which(Startcountries$Year == 2023, arr.ind = TRUE),][,-c(1,4:28)]
View(Startcountries)
names(Startcountries) = c("Rank", "Country")
endcountries  = as.data.frame(rownames(data))
names(endcountries) = c("Country")
dim(Startcountries)
dim(endcountries)
endcountrieslist = c(endcountries$Country)
Startcountrieslist = c(Startcountries$Country)
missing = c()

for (i in Startcountrieslist){
  if (!(i %in% endcountrieslist)){
    missing = c(missing,i)
  }
}
missing = as.data.frame(missing)


OCDE_countries = c("Australia","Austria","Belgium","Canada","Chile","Colombia","Costa Rica","Czechia","Denmark","Estonia","Finland","France","Germany","Greece","Hungary","Iceland","Israel","Italy","Japan","Korea","Latvia","Lithuania","Luxembourg","Mexico","Netherlands","New Zealand","Norway","Poland","Portugal","Slovak Republic","Slovenia","Spain","Sweden","Switzerland","Türkiye","United Kingdom","United States")
missing$OCDE = 0
for (i in 1:nrow(missing)){ if (missing$Pays_perdus[i] %in% OCDE_countries) {
  missing$OCDE[i] = 1
}}

names(missing) = c("Pays_perdus")
write.csv(missing, "Pays_perdus.csv")
dim(missing)

