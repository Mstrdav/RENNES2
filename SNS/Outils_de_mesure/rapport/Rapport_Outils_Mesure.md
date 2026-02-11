# Rapport d'Étude : Validation de Capteurs de Puissance (Wahoo KickR vs Favero Assioma Duo)

**Auteurs :** Colin Geindre & Binôme
**Date :** 13/02/2026
**Contexte :** Master SNS / Outils de Mesure

---

## Introduction
Ce rapport présente l'analyse comparative de deux dispositifs de mesure de puissance en cyclisme :
1.  **Wahoo KickR** (Home Trainer connecté) - *Outil évalué*
2.  **Favero Assioma Duo** (Pédales instrumentées) - *Outil de référence*

L'objectif est de valider la fiabilité (justesse et fidélité) du Wahoo KickR à travers différents protocoles d'effort.

---

## Partie 1 : Analyse Technique des Outils

### 1.1 La Puissance Mécanique
La puissance mécanique ($P$) est la mesure objective de l'intensité de l'effort externe fourni par le cycliste. Elle est définie par la relation :
$$ P (W) = C (N.m) \times \omega (rad.s^{-1}) $$
Où $C$ est le couple de force appliqué sur les manivelles et $\omega$ la vitesse angulaire de pédalage. Contrairement à la fréquence cardiaque (réponse physiologique retardée), la puissance est une mesure instantanée.

### 1.2 Principes de Mesure
*   **Favero Assioma Duo (Référence) :** Mesure directe. Huit jauges de contrainte par pédale mesurent la déformation de l'axe pour calculer la force tangentielle. La vitesse angulaire est mesurée par un gyroscope intégré (IAV Power), permettant une précision élevée même avec un pédalage irrégulier.
*   **Wahoo KickR (Test) :** Mesure indirecte/Estimation. La puissance est calculée au niveau du moyeu arrière via le freinage électromagnétique. Il déduit la puissance nécessaire pour maintenir une vitesse de volant d'inertie donnée contre une résistance magnétique connue.

### 1.3 Comparaison Théorique
| Critère | Wahoo KickR (Home Trainer) | Favero Assioma (Pédales) |
| :--- | :--- | :--- |
| **Localisation** | Après la transmission (Cassette) | Point d'application (Pied) |
| **Pertes** | Frottements chaîne/dérailleur (~2-3%) | Négligeables |
| **Précision annoncée** | +/- 1-2% | +/- 1% |
| **Avantage** | Stabilité, mode ERG (résistance pilotée) | Portabilité, mesure G/D réelle |

**Choix de la référence :** Les pédales **Assioma** sont choisies comme référence car elles mesurent la puissance produite *avant* les pertes mécaniques de la transmission. Théoriquement, la puissance KickR devrait donc être *inférieure* à la puissance Assioma.

---

## Partie 2 : Résultats de la Validation

### 2.1 Méthodologie de Traitement
Les fichiers bruts (.fit) présentaient des décalages d'horloge variables (de -5s à +22s). Une procédure de synchronisation automatique par **Cross-Correlation** a été développée (Python) pour aligner temporellement les signaux de puissance avant toute comparaison.

### 2.2 Analyse de la Corrélation (Fidélité)
Sur les efforts d'intensité moyenne à haute cadence (90 rpm), la corrélation entre les deux capteurs est excellente ($r > 0.9$).

**Exemple (Sujet : Anton, 90 rpm) :**
![Courbe Puissance Anton](figures/Anton_90rpm_power.png)
*On observe une superposition quasi-parfaite des dynamiques de puissance.*

### 2.3 Analyse du Biais (Justesse)
L'analyse de Bland-Altman révèle un biais systématique inattendu.

**Bland-Altman (Anton) :**
![Bland-Altman Anton](figures/Anton_90rpm_bland_altman.png)
* Le biais moyen (ligne rouge) est positif : Le Wahoo surestime la puissance par rapport aux pédales.
* Moyenne Wahoo : 123 W vs Assioma : 117 W.
* **Interprétation :** C'est physiquement "impossible" (création d'énergie). Cela indique un défaut de calibration du Wahoo qui "gonfle" les chiffres d'environ 5%.

### 2.4 Le Cas Critique des Basses Cadences
Une anomalie majeure a été détectée sur les protocoles à 70 rpm.

**Exemple (Sujet : Jules, 70 rpm) :**
![Courbe Puissance Jules](figures/Jules_70rpm_power.png)
* **Wahoo (Bleu) :** ~60 W
* **Assioma (Orange) :** ~130 W
* **Constat :** À basse vitesse de rotation, le Wahoo "décroche" et sous-estime massivement l'effort réel. Il n'est pas fiable dans cette zone.

---

## Partie 3 : Rapport Client (Synthèse Décisionnelle)

**À l'attention de la Direction R&D - Wahoo Fitness**

**Objet : Audit de validation du prototype KickR**

Madame, Monsieur,

L'évaluation de votre nouveau dispositif de mesure de puissance, menée par notre laboratoire sur un panel de cyclistes, a permis de dégager les conclusions suivantes :

### ✅ Points Forts (Validation)
*   **Réactivité :** Excellente dynamique sur les variations d'intensité.
*   **Corrélation :** Le capteur suit très fidèlement ($r=0.96$) la référence sur les plages d'utilisation standard (90 rpm, >100W). Pour un usage d'entraînement aux variations d'allure, l'outil est performant.

### ⚠️ Points Critiques (Non-Conformité)
1.  **Biais Positif (+5%) :** Contrairement aux lois de la physique (pertes de transmission), votre appareil affiche une puissance supérieure à celle produite aux pédales. Il "flatte" l'utilisateur mais manque de justesse absolue.
2.  **Défaillance à Basse Cadence :** En dessous de 75 rpm et 100W, le système de mesure s'effondre (écart > 50%). Cette plage d'utilisation "récupération" est actuellement non mesurable.

### 💡 Recommandations
Nous recommandons la mise en place d'une mise à jour firmware pour :
1.  Appliquer un facteur correctif de linéarisation sur la mesure du frein électromagnétique à basse vitesse.
2.  Recalibrer le "Zéro Offset" pour supprimer la surestimation systématique.

**Avis final :** Valide pour l'entraînement intensif, non valide pour la mesure scientifique ou les basses intensités en l'état.

**L'équipe Data Performance**
M1 SNS - Rennes 2
