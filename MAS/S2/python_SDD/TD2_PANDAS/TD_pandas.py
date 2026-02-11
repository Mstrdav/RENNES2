import pandas as pd

# Lecture des données
#####################
# Question 1

df = pd.read_csv("SpeedDating.csv", sep=",")
print(df.shape)
print(df.columns)
print("="*100)

# Suppression des incohérences
##############################
# Question 2
df = df.drop(['from', 'zipcode'], axis=1)
# ou
# df = df.drop(columns=['from', 'zipcode'])

# autre possibilité avec le paramètre inplace=True (modification de la DataFrame "sur place")
# df.drop(['from', 'zipcode'], axis=1, inplace=True)

# Question 3
print("Question 3")
df = df[~df['wave'].between(6,9)]   # sélection de lignes par une Series de booléens (renvoyée par between())
                                    # l'opérateur ~ permet d'inverser la Series de booléens

# autre solution avec un OU logique : opérateur |
# df = df[(df['wave'] < 6) | (df['wave'] > 9)]

# autre solution avec méthode de requête query()
# df = df.query("(wave < 6) | (wave > 9) ")

print(df.shape)
print("="*100)

# Suppression des redondances
#############################
# Question 4 : ajout de la différence d'âge (après la colonne 'age')
print("Question 4")
df.insert(loc=df.columns.get_loc('age')+1, column='diff_age', value=(df['age'] - df['age_o']).abs())

# remarque : abs(df['age'] - df['age_o']) semble fonctionner aussi...
print(df.shape)
print("="*100)

# Question 5
print("Question 5")
df = df.drop([c for c in df.columns if c.endswith("_o") or "_o_" in c], axis=1)
print(df.shape)
print("="*100)

# Question 6
print("Question 6")
df = df.drop(['id', 'idg', 'partner', 'field', 'career'], axis=1)
print(df.shape)
print("="*100)

# Sélection des données utiles
##############################
# Question 7
print("Question 7")
df = df.drop(['condtn', 'wave', 'round', 'position', 'positin1', 'order'], axis=1)
print(df.shape)
print("="*100)

# Question 8
print("Question 8")
df = pd.concat([df.loc[:,:'amb5_1'], df['dec']], axis=1)
print(df.shape)
print("="*100)

# Traitement des données manquantes
###################################
# Question 9
print("Question 9")
print(df.isna().sum())
print("="*100)

# Question 10
print("Question 10")
df = df.loc[:,df.isna().sum() < 0.1*df.shape[0]]  # sélection des colonnes par une Series de booléens
print(df.shape)
print("="*100)

# Question 11
print("Question 11")
df = df.dropna()
print(df.shape)
print(df.columns)
print("="*100)

# Analyse des données
######################
# Question 12
print("Question 12")

print(df.groupby('gender')[['sports', 'tvsports', 'exercise','hiking', 'yoga']].mean())
# --> plus de sport et sport à la télé pour les hommes, plus de yoga pour les femmes
print("="*100)

print(df.groupby('gender')[['dining', 'gaming', 'clubbing', 'reading', 'tv', 'shopping']].mean())
# --> plus de jeux vidéo pour les hommes, plus de shopping pour les femmes
print("="*100)

print(df.groupby('gender')[['museums', 'art', 'theater', 'movies', 'concerts', 'music']].mean())
# --> globalement plus de culture pour les femmes, surtout musées, arts et théâtre 
print("="*100)

# Question 13
print("Question 13")
print(df.groupby('gender')[['attr1_1', 'sinc1_1', 'intel1_1', 'fun1_1', 'amb1_1', 'shar1_1']].mean())
# --> les hommes cherchent plutôt une partenaire attirante, les femmes plutôt un partenaire intelligent
# --> différence marquée sur l'ambition du/de la partenaire, plus recherchée par les femmes que par les hommes
print("="*100)

# Question 14
print("Question 14")
print(df.groupby('gender')['iid'].count())
print("="*100)
# --> environ le même nombre de femmes et d'hommes

# groupement double par genre et par décision
print(df.groupby(['gender', 'dec'])['iid'].count())
print("="*100)
# --> un peu moins de décisions positives chez les femmes

# autre possibilité avec une table pivot dans Pandas
print(pd.pivot_table(df, values="iid", index='gender', columns='dec', aggfunc="count"))
print("="*100)

# Question 15
print("Question 15 : proportion de matchs")
nb_match = (df['match'] == 1).sum()
print(nb_match/df.shape[0])
print("="*100)
# environ 16,5% de matchs entre les partenaires des rencontres

# remarque : print(df['match'].mean())  marche aussi ici, mais c'est un cas particulier (seulement valable pour des valeurs 0 et 1)

# Question 16
print("Question 16")
print(df.groupby('match')[['int_corr', 'samerace', 'age', 'diff_age']].mean())
# --> la différence d'âge et l'origine ethnique semblent avoir le plus d'influence sur les matchs 
print("="*100)

# Triatement des données catégorielles
#######################################
# Question 17
print("Question 17")
# données catégorielles = données (textuelles ou codes numériques) qui représentent des catégories (ou modalités) dont l'ordre ne devrait pas avoir d'importance
# on ne transforme pas les données ayant seulement 2 catégories (données binaires) car c'est inutile : une des colonnes de dummies
# donnerait la même information que la colonne d'origine et une deuxième colonne de dummies, inverse de la première, serait ajoutée
# Les codes numériques ayant un ordre évident (exemple : échelle de 1 à 10) doivent être gardés tels quels

categoricals = ['field_cd', 'race', 'goal', 'date', 'go_out', 'career_c']
df = pd.get_dummies(df, columns=categoricals, dtype='int')   # dtype='int' permet d'avoir des dummies de type entiers : 0 ou 1 (par défaut on a des booléens)
                                                             # --> cela permet d'appliquer la normalisation des données à la fin

# df = df.astype('float')   # autre possibilité pour transformer les dummies booléens en nombres 0.0 ou 1.0

print(df)
print("="*100)

# Jointure
###########
# Question 18
print("Question 18 : df_0")
df_0 = df[df.gender == 0].drop('gender', axis=1)
print(df_0)
print("="*100)

print("Question 18 : df_1")
df_1 = df[df.gender == 1].drop('gender', axis=1)
df_1 = df_1.drop(['match', 'int_corr', 'samerace','diff_age'], axis=1)
print(df_1)
print("="*100)

# Question 19
print("Question 19 : df_all")

# il faut faire une jointure interne pour ne garder que les personnes qui ont une correspondance avec un partenaire de genre opposé 
# et obtenir une ligne par rencontre, avec les données complètes de la rencontre
# (avec une jointure externe on pourrait obtenir des lignes de rencontre incomplète)
# --> les lignes correspondant à des personnes dont le partenaire de rencontre n'est plus présent dans le jeu de données seront éliminées
df_all = df_0.merge(df_1, how="inner", left_on=["iid","pid"], right_on=["pid", "iid"], suffixes=("_0", "_1"))
print(df_all)
print("="*100)

# Question 20
print("Question 20")
df_all = df_all.loc[:, (df_all.nunique()>1)]
print(df_all.shape)
print("="*100)

# Séparation des variables explicatives et expliquées
#####################################################
# Question 21
print("Question 21")
df_all = df_all.drop(['pid_0', 'pid_1', 'dec_0', 'dec_1'], axis=1)
print(df_all.shape)
print("="*100)

# Question 22
print("Question 22")
df_all = df_all.set_index(['iid_0', 'iid_1'])
print(df_all)
print("="*100)

# Question 23
print("Question 23 : df_Y")
df_Y = df_all['match']
print(df_Y)
print("="*100)
print("Question 23 : df_X")
df_X = df_all.drop('match', axis=1)
print(df_X)
print("="*100)

# Normalisation des données explicatives
########################################
# Question 24
# remarque 1 : 
#   - df.min() calcule par défaut le minimum par colonne (i.e. le long de l'axe 0)
#   - on obtient une Series dont la taille correspond au nombre de colonnes de df
#
# remarque 2 : 
#   - le signe "-" (soustraction) entre une DataFrame et une série, opère par colonne
#   - à chaque valeur d'une colonne de la DataFrame est soustrait la valeur  correspondante de la Series  

df_X = (df_X - df_X.min())/(df_X.min()  - df_X.max())

# autre écriture possible avec la méthode sub() : 
#df_X = df_X.sub(df_X.min(), axis='columns')/df_X.min().sub(df_X.max())

print(df_X)