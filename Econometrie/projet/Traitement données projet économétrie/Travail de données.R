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
#Popdensity
#Netmigration
#Overweight
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


annualworkhours = read.csv("yearlyworkinghourspppc.csv", dec= ".", header = TRUE, sep = ",")
summary(annualworkhours)
View(annualworkhours)  #Manque surtout des pays pauvres
annualworkhours = annualworkhours[which(annualworkhours$Year >= 2013 & annualworkhours$Year <=2023, arr.ind = TRUE),]
annualworkhours_moyenne = tapply(annualworkhours$Average.working.hours.per.worker, annualworkhours$Code, mean, na.rm=TRUE)
annualworkhours_moyenne = as.data.frame.table(annualworkhours_moyenne)
names(annualworkhours_moyenne) = c('Code', "Annual_working_hours")
summary(annualworkhours_moyenne) # 254   NA's   :130 TROP DE PAYS MANQUANTS
View(annualworkhours_moyenne)
annualworkhours_moyenne = na.omit(annualworkhours_moyenne)
dim(annualworkhours_moyenne) 

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
View(migration_moyenne)


incomedistributionindex = read.csv("Gini income distribution index.csv", sep = ",", dec = ".", header = TRUE)
incomedistributionindex = incomedistributionindex[,-c(1,2,5:66)]
summary(incomedistributionindex)
View(incomedistributionindex)  #Bcp de donnees manquantes, a voir une fois les moyennes faites
incomedistributionindex$moyennes = rowMeans(incomedistributionindex[,3:12], na.rm=TRUE) #2013 à 2023
sum(is.na(incomedistributionindex$moyennes)) #23 lignes vides
dim(incomedistributionindex) #166 pays -23 non renseignées = 145 pays analysables
incomedistributionindex_moyenne = incomedistributionindex[,c(1,14)]
incomedistributionindex_moyenne = na.omit(incomedistributionindex_moyenne)
names(incomedistributionindex_moyenne) = c("Code", "Income_distribution_index")
View(incomedistributionindex_moyenne)

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
variables = list(incomedistributionindex_moyenne,corruptionindex_moyenne,GDP_moyenne,lifespan_moyenne,migration_moyenne,overweight_moyenne,popdensity_moyenne,annualworkhours_moyenne,energyconsumption_moyenne,militarydepense_moyenne,popgrowth_moyenne)

library(purrr)
CombinedTrue = purrr::reduce(.x = variables, merge, by = c('Code'), all = T)
CombinedFalse = purrr::reduce(.x = variables, merge, by = c('Code'), all = F)
dim(CombinedTrue)
dim(CombinedFalse) #105 mais 123 sans le Gini income distribution index et 127 sans le annualworkhours



dim(purrr::reduce(.x = list(corruptionindex_moyenne,GDP_moyenne,lifespan_moyenne,migration_moyenne,overweight_moyenne,popdensity_moyenne,energyconsumption_moyenne,militarydepense_moyenne,popgrowth_moyenne), merge, by = c('Code'), all = F))

CombinedFalse = purrr::reduce(.x = list(corruptionindex_moyenne,GDP_moyenne,lifespan_moyenne,migration_moyenne,overweight_moyenne,popdensity_moyenne,energyconsumption_moyenne,militarydepense_moyenne,popgrowth_moyenne), merge, by = c('Code'), all = F)
View(CombinedFalse)

###########################################################################

countrynames = popdensity[,c(3,4)]
names(countrynames) = c("Code", "Country.name")
View(countrynames)
##########################################################################

happiness = read.csv("WorldHappinessIndex.csv", sep  =";", dec  =",", header = TRUE)
summary(happiness)
View(happiness)
happiness = happiness[which(happiness$Year >= 2013 & happiness$Year <=2023, arr.ind = TRUE),]

happiness_moyenne = tapply(happiness$Life.evaluation..3.year.average., happiness$Country.name, mean, na.rm=TRUE)
happiness_moyenne = as.data.frame(happiness_moyenne)
library(tibble)
happiness_moyenne <- tibble::rownames_to_column(happiness_moyenne, "Country.name")
anyNA(happiness_moyenne)
summary(happiness_moyenne)
View(happiness_moyenne)
dim(happiness_moyenne)


don = purrr::reduce(.x = list(countrynames, CombinedFalse), merge, by = c('Code'), all = T)
donnees = purrr::reduce(.x = list(don, happiness_moyenne), merge, by = c('Country.name'), all = T)
donnees = as.data.frame(donnees)
summary(donnees)
donnees = na.omit(donnees)

################################################################################

dim(donnees)
summary(donnees)
View(donnees)

write.csv(donnees, "donnees.csv")



