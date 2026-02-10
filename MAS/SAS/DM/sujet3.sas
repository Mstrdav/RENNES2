/* 
Comparaison de deux moyennes
Nous allons comparer les poids de poulpes mâles et femelles au stade adulte grâce à proc ttest. Nous disposons
pour cela des données de 15 poulpes mâles et de 13 poulpes femelles pêchés au large des côtes mauritaniennes.
1. Importer les données (fichier poulpe.csv) ;
2. Comparer graphiquement les deux sous-populations (Construire des boîtes à moustaches pour chaque
sous-population) ;
3. Estimer les statistiques de base (moyenne, écart-type, quartiles) par sous-population ;
4. Tester l’égalité des moyennes via un test avec hypothèse d’égalité de variance (pooled) ou sans égalité
des variances (Satterthwaite).
*/

/* dlm is ; not , */
proc import datafile="M:\Données\Analyse des Données\DM\Sujet 3\poulpe.csv"
    out=poulpe
    dbms=csv
    replace;
    delimiter=';';
    getnames=yes;
run;

/* Boîtes à moustaches */
proc sgplot data=poulpe;
    vbox poids / category=sexe;
    title "Boîtes à moustaches des poids de poulpes par sexe";
run;

/* Statistiques descriptives */
proc means data=poulpe mean std q1 q3;
    class sexe;
    var poids;
    title "Statistiques descriptives des poids de poulpes par sexe";
run;

/* Test d'égalité des moyennes */
proc ttest data=poulpe;
    class sexe;
    var poids;
    title "Test d'égalité des moyennes des poids de poulpes par sexe";
run;
