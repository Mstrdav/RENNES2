/*

Sujet 8

L’objectif est d’obtenir les mêmes sorties graphiques que celle proposées dans le fichier acp.htm. La procédure
pour faire les calculs d’ACP et certains graphiques est proc princomp.
— Importer le fichier decathlon.csv et centrer-réduire 2 les variables de v100m à v1500m (proc stdize).
— Réaliser l’ACP et sélectionner les graphiques afin d’obtenir uniquement les 2 graphiques sur les valeurs
propres, les caractéristiques de la composantes et les scores de la composante.
— Réaliser le dernier graphique par proc gplot en suivant les étapes suivantes
1. Exporter les résultats de l’ACP ; Le fichier contiendra les variables prin1 et prin2 qui sont les
coordonnées des individus sur les axes 1 et 2 ;
2. Calculer pour la variable prin1 la moyenne (des coordonnées) des individus ayant pour modalité
OlympicG et la moyenne (des coordonnées) des individus ayant pour modalité Decastar ; Ces deux
moyennes donnent les coordonnées sur l’axe 1 des points moyens OlympicG et Decastar ;
3. Faire de même pour prin2
4. Tracer les individus de coordonnées données par les axes 1 et 2 avec comme identifiant leur nom et
les 2 points moyens OlympicG et Decastar en rouge (graphique final).
puis prin2

*/
proc import datafile="/home/u64337831/sasuser.v94/DM/decathlon.csv"
	out=decathlon
	dbms=csv
	replace;
	delimiter=";";
	getnames=yes;
run;

proc stdize data=decathlon out=decathlon_cr method=std;
   var v100m longueur poids hauteur v400m v110mH disque perche javelot v1500m;
run;

proc means data=decathlon_cr mean std min max;
   var v100m longueur poids hauteur v400m v110mH disque perche javelot v1500m;
   title "Decathlon avec variables centrées réduites";
run;

/* ACP */
proc princomp data=decathlon_cr out=decathlon_acp plots=(scree score(ncomp=2 ellipse));
   var v100m longueur poids hauteur v400m v110mH disque perche javelot v1500m;
   title "Analyse en Composantes Principales sur Decathlon";
run;

/* Calcul des moyennes des coordonnées sur les deux premiers axes */
proc sort data=decathlon_acp;
   by compet;
run;

proc means data=decathlon_acp noprint;
   by compet;
   var prin1 prin2;
   output out=moyennes mean=Prin1 Prin2;
run;

/* Ajout de la variable compet aux moyennes: valeur=decastar_moy et olympicg_moy */
data moyennes;
   set moyennes;
   if compet = "Decastar" then competbis = "Decastar_moy";
   else if compet = "OlympicG" then competbis = "OlympicG_moy";
   drop _TYPE_ _FREQ_ compet;
run;

data filter_acp;
	set decathlon_acp;
   if compet = "Decastar" then competbis = "Decastar";
   else if compet = "OlympicG" then competbis = "OlympicG";
   if compet = "Decastar" then Nom = "Decastar";
   else if compet = "OlympicG" then Nom = "OlympicG";
   drop compet;
run;

/* un graphique avec les deux points moyens moyennes(mean_prin1, mean_prin2) et les individus decathlon_acp(prin1 prin2) avec leur nom decathlon_acp(Nom), les premiers en rouge les autres en noir */
data final;
	set moyennes filter_acp;
	drop v100m longueur poids hauteur v400m v110mH disque perche javelot v1500m classement points Prin3-Prin10;
run;

data labels;
    set final;
    retain function 'label'color 'black' size 1.2
              xsys '2' ysys '2';
              
    x = prin1;
    y = prin2;

    if compet in ("Decastar_moy", "OlympicG_moy") then do;
        color = 'red';
    end;
    else do;
        color = 'black';
        position = '3';
    end;
    
    text = Nom;
run;

proc gplot data=final;
   plot prin2*prin1=competbis / annotate=labels;
   symbol1 c=black v=dot h=1;
   symbol2 c=red v=dot h=2;
   symbol3 c=black v=plus h=1;
   symbol4 c=red v=plus h=2;
   title "Graphique des individus et des points moyens";
run;
quit;
