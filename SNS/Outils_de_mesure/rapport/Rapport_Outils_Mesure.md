# Rapport d'Étude : Validation de Capteurs de Puissance (Wahoo KickR vs Favero Assioma Duo)

**Auteurs :** Colin Geindre & Zoé Orlandi
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
Les fichiers bruts (.fit) présentaient des décalages d'horloge variables (jusqu'à 5 minutes). Une procédure de synchronisation automatique par **Cross-Correlation** a été développée (Python) pour aligner temporellement les signaux de puissance avant toute comparaison.

### 2.2 Analyse de la Corrélation (Fidélité)
Sur l'ensemble des protocoles (70 rpm, 90 rpm, Sprints), la corrélation entre les deux capteurs est excellente ($r > 0.95$ en moyenne). Le Wahoo KickR suit très fidèlement la dynamique de l'effort, même lors des variations rapides.

**Exemple (Sujet : Anton, 90 rpm) :**
![Comparaison Puissance Anton (90 rpm)](figures/Anton_90rpm_graph.png)
*Figure 1 : Superposition quasi-parfaite des dynamiques de puissance.*

### 2.3 Analyse du Biais (Justesse)
Contrairement aux attentes physiques (pertes de transmission), le Wahoo KickR affiche systématiquement une puissance supérieure à celle des pédales.

**Exemple (Sujet : Jules, 70 rpm) :**
![Comparaison Puissance Jules (70 rpm)](figures/Jules_70rpm_graph.png)
*Figure 2 : Même à basse cadence, la dynamique est bonne, mais le Wahoo (en bleu) est constamment au-dessus de l'Assioma (en orange).*

Ce biais positif est constant sur tous les sujets (moyenne +6W à +10W), suggérant un problème de calibration systématique plutôt qu'aléatoire.

---

## Partie 3 : Rapport Client (Synthèse Décisionnelle)

**À l'attention de la Direction R&D - Wahoo Fitness**
**Date :** 13 Février 2026
**Objet : Audit de validation du prototype KickR V6**

Madame, Monsieur,

Dans le cadre du processus de validation de votre nouveau Home Trainer **Wahoo KickR**, notre laboratoire d'analyse de la performance (Université Rennes 2) a mené une étude comparative rigoureuse face à l'étalon-or du marché (Favero Assioma Duo).

Ce rapport synthétise les résultats de nos tests menés sur un panel de cyclistes, couvrant des protocoles à cadence fixe (70 et 90 rpm) ainsi que des efforts maximaux (sprints), afin d'évaluer la fiabilité, la justesse et la robustesse de votre dispositif.

### 1. Synthèse des Résultats

L'analyse des données corrigées (synchronisation temporelle précise) révèle un comportement très cohérent de l'appareil, caractérisé par une excellente dynamique mais une justesse perfectible.

#### A. Fidélité Exemplaire (Point Fort)
Sur l'ensemble des plages d'utilisation testées (basses et hautes cadences, sprints), le Wahoo KickR démontre une **remarquable fidélité**.
*   **Corrélation :** Les coefficients de corrélation sont extrêmement élevés ($r > 0.95$) pour la quasi-totalité des sujets.
*   **Réactivité :** L'appareil capture avec précision les variations d'effort, sans lissage excessif ni retard perceptible une fois synchronisé.
*   **Conclusion :** La capacité du capteur à reproduire la *forme* de l'effort est validée. Il est parfaitement adapté pour structurer des séances d'entraînement basées sur la variation d'intensité.

#### B. Biais Systématique Positif (Non-Conformité)
Nous relevons un **biais systématique positif** de l'ordre de **+5% à +8%** par rapport à la référence (Assioma Duo) sur les efforts stabilisés.
*   **Physiquement incohérent :** Le KickR mesurant la puissance en "bout de chaîne" (après la transmission), il devrait logiquement afficher une puissance *inférieure* à celle des pédales (pertes mécaniques de 2-3%). Or, il affiche une puissance *supérieure* (+6 W en moyenne sur 100 W).
*   **Uniformité :** Ce biais est présent aussi bien à 70 rpm qu'à 90 rpm. Contrairement à nos premières observations (liées à un défaut de sync), le capteur ne "décroche" pas à basse cadence, mais il surestime constamment l'effort.
*   **Impact Utilisateur :** Ce biais "flatteur" fausse les données de performance absolue et rend difficile la comparaison avec des sorties sur route équipées de capteurs directs.

### 2. Analyse Technique & Hypothèses

La constance de ce biais positif écarte l'hypothèse d'une dérive aléatoire. Deux causes principales sont envisagées :
1.  **Calibration d'Usine (Slope/Offset) :** La pente de conversion (relation vitesse/résistance -> puissance) semble mal étalonnée, intégrant peut-être une compensation trop agressive des pertes de friction estimées.
2.  **Dérive Thermique :** Si le "Zero Offset" (calibration à vide) n'est pas effectué après une période de chauffe, la dilatation des composants et la fluidification des graisses peuvent réduire la friction réelle par rapport au modèle théorique, conduisant le système à surestimer la puissance résistive.

### 3. Recommandations Stratégiques

Pour garantir la validation du produit sur le segment "Expert/Scientifique", nous recommandons :

#### Actions Correctives (Software)
1.  **Ajustement du Factory Calibration :** Réviser les coefficients de la courbe de puissance pour réduire la valeur affichée de 5% à 8% globalement. Cela alignerait les mesures sur la réalité physique (P_Wahoo < P_Pédales).
2.  **Spindown Automatique :** Implémenter une procédure de calibration automatique en roue libre (Spindown) plus fréquente ou détectée lors des phases de récupération, pour compenser la dérive thermique en cours de séance.

#### Communication & Usage
1.  **Transparence :** Indiquer que la précision absolue est optimisée pour la répétabilité (suivi de progrès sur le même appareil) plutôt que pour la justesse absolue inter-appareils.
2.  **Protocole :** Recommander systématiquement une calibration après 10 minutes d'échauffement.

### 4. Conclusion

Le prototype **Wahoo KickR** est **VALIDE** pour l'entraînement sportif grâce à sa dynamique exceptionnelle et sa grande fidélité. Cependant, il présente un **DÉFAUT DE JUSTESSE** (surestimation systématique) qui doit être corrigé par une mise à jour logicielle pour prétendre au statut d'outil de mesure scientifique.

Restant à votre disposition pour détailler ces analyses techniques.

Cordialement,

**L'équipe Data Performance**
M1 SNS - Université Rennes 2
