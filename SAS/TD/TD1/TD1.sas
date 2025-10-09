/*
  TD1.sas
  Exemples de lectures de fichiers CSV
*/

/* Lynx : i;date;nbe */
data lynx;
	informat date anydtdte10. nbe $5.;
	format date ddmmyy10.;
	infile "/home/u64337831/sasuser.v94/lynx.csv" dlm=";" firstobs=2;
	input i $ date nbe;
	drop i;
run;

/* Bank : i;age;job;marital;education;default;housing;loan;duration;y */
data bank;
	infile "/home/u64337831/sasuser.v94/bank.csv" dlm=";" firstobs=2;
	informat job marital education $30. 
		default housing loan y $3.;
	input i age job marital education default housing loan duration y;
	drop i;
run;

/* Import : i;date;nbDef */
data import;
	informat date anydtdte10. nbDef;
	format date ddmmyy10.;
	infile "/home/u64337831/sasuser.v94/import.csv" dlm=";" firstobs=2;
	input i $ date nbDef;
	drop i;
run;


/* ISF2018 : Region;Departement;Ville;Nb-redevables;Patrimoine-moyen;Impot-moyen */
data isf2018;
	informat codePostal $6. region departement ville $30.;
	format patrimoineMoyen NUMX10.2;
	infile "/home/u64337831/sasuser.v94/isf-2018.csv" dlm=";" firstobs=2;
	input codePostal region departement ville nbRedevables patrimoineMoyen impotMoyen;
run;

/* Version proc import */
proc import datafile="/home/u64337831/sasuser.v94/lynx.csv"
	out=lynx_pi
	dbms=csv
	replace;
	delimiter=';';
	datarow=2;
	getnames=no;
run;

proc import datafile="/home/u64337831/sasuser.v94/bank.csv"
	out=bank_pi
	dbms=csv
	replace;
	delimiter=';';
	datarow=2;
	getnames=yes;
run;

proc import datafile="/home/u64337831/sasuser.v94/import.csv"
	out=import_pi
	dbms=csv
	replace;
	delimiter=';';
	datarow=2;
	getnames=no;
run;

proc import datafile="/home/u64337831/sasuser.v94/isf-2018.csv"
	out=isf2018_pi
	dbms=csv
	replace;
	delimiter=';';
	datarow=2;
	guessingrows=MAX;
	getnames=no;
run;

/* 
  Import des fichiers test
*/

proc import datafile="/home/u64337831/sasuser.v94/test1.csv"
	out=test1
	dbms=csv
	replace;
	delimiter=';';
	datarow=2;
	getnames=yes;
run;

* the second one has comma as decimal separator, so we use data step;
data test2;
	infile "/home/u64337831/sasuser.v94/test2.csv" dlm=";" firstobs=2;
	informat HT19 C19 HT29 COMMA10.2;
	input CLONE $ B $ IN $ HT19 C19 HT29;
run;

* the third one is a prn file with tab separators;
proc import datafile="/home/u64337831/sasuser.v94/test3.prn"
	out=test3
	dbms=dlm
	replace;
	delimiter=tab;
	datarow=2;
	getnames=yes;
	guessingrows=MAX;
run;

/* 
Importer puis fusionner (en un seul tableau au final) etat1.csv, etat2.csv et etat3.csv grâce aux
clefs communes (attention aux longueurs des champs de caractères)
etat1 : "region";"etat"
etat2 : "etat","Population","Income","Illiteracy","Life.Exp","Murder","HS.Grad","Frost","Area"
etat3 : "num" "region" "vote"
*/
data etat1; 
	infile "/home/u64337831/sasuser.v94/etat1.csv" dlm=";" firstobs=2;
	informat region $20. etat $20.;
	input region etat;
run;
proc sort data=etat1; by etat; run;

data etat2; 
	infile "/home/u64337831/sasuser.v94/etat2.csv" dlm="," firstobs=2;
	informat etat $20. Population Income Illiteracy LifeExp Murder HSGrad Frost Area;
	input etat $ Population Income Illiteracy LifeExp Murder HSGrad Frost Area;
run;