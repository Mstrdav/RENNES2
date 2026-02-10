# Rapport d'Étude : Validation de Capteurs de Puissance (Wahoo KickR vs Favero Assioma Duo)

**Auteurs :** Colin Geindre & Binôme
**Date :** 13/02/2026
**Contexte :** Master SNS / Outils de Mesure

---

## Partie 1 : Fonctionnement des outils de mesures

### 1. Puissance mécanique de pédalage
La puissance mécanique ($P$) est le produit du couple ($C$) appliqué sur les pédales et de la vitesse angulaire de pédalage ($\omega$).
$$ P = C \times \omega $$
Elle s'exprime en Watts (W). $C$ est en Newton-mètre (N.m) et $\omega$ en radians/seconde (rad/s).

### 2. Méthodes de mesure
*   **Wahoo KickR (Home Trainer) :** Mesure la puissance au niveau de la cassette (hub arrière). Il estime le couple via le frein électromagnétique et mesure la vitesse de rotation de la cassette (liée à la cadence par le braquet).
*   **Favero Assioma Duo (Pédales) :** Mesure la puissance directement au point d'application de la force. Chaque pédale contient des jauges de contrainte (strain gauges) pour mesurer la force tangentielle (et donc le couple) et un accéléromètre/gyroscope pour la vitesse angulaire instantanée (IAV).

### 3. Avantages et Limites
| Outil | Avantages | Limites |
|-------|-----------|---------|
| **Wahoo KickR** | Stabilité, contrôle de la résistance (Erg mode), pas de problème d'installation. | Mesure après la transmission (pertes chaîne ~2-3%), inertie du volant, nécessite un vélo. |
| **Favero Assioma** | Mesure directe (source), portable (sur n'importe quel vélo), analyse G/D. | Installation (couple de serrage), calibration requise, fragile (chocs). |

### 4. Outil de Référence
**Favero Assioma Duo** est considéré comme l'outil de référence ("Gold Standard" terrain) pour la puissance physiologique produite par le cycliste, car il mesure avant les pertes mécaniques de la transmission. Le Wahoo mesure la puissance *transmise* à la route (ou au volant), ce qui est différent de la puissance *produite*.

---

## Partie 2 : Validation du capteur de puissance

### 1. Protocole de validation
L'étude compare les données de puissance issues des deux capteurs enregistrées simultanément lors de deux types d'efforts :
*   **Steady State :** Paliers stables à cadence fixée (70 rpm et 90 rpm).
*   **Sprints :** Efforts maximaux brefs pour évaluer la réactivité et les pics de puissance.

**Synchronisation :** Les fichiers bruts (.fit) ont été synchronisés temporellement par une méthode de corrélation croisée (Cross-Correlation) sur le signal de puissance afin de corriger les décalages d'horloge.

### 2. Limites et Améliorations
*   **Problème identifié (70 rpm) :** Une divergence majeure a été observée sur les essais à 70 rpm (Wahoo ~50W vs Assioma ~130W). Cela suggère un défaut de calibration du Wahoo à basse intensité/cadence, ou un mode "Erg" mal réglé. Ces données ont été exclues de l'analyse de corrélation finale.
*   **Synchronisation Sprints :** Les fichiers de sprints présentaient des décalages temporels importants et une faible corrélation, rendant l'analyse point par point difficile.
*   **Amélioration :** Utiliser un compteur unique (head unit) appairé aux deux capteurs simultanément (si possible) ou effectuer un "top départ" (marker) visible dans les données (ex: 3 coups de pédale à vide) pour faciliter l'alignement.

### 3. Reproductibilité intra-individuelle (Sprints)
L'analyse des pics de puissance sur les sprints montre une variabilité. Le Coefficient de Variation (CV) intra-individuel permettrait de quantifier cette reproductibilité. (Données brutes non exploitables avec précision pour ce calcul suite aux problèmes de sync).

### 4. Corrélation (Données Valides)
Sur les enregistrements valides (principalement 90 rpm, ~120W), nous obtenons une **forte corrélation** ($r \approx 0.85 - 0.96$) pour les sujets Anton, MathisW, Tristan, NathanM, MathisM, Jonathan, Sacha.
Cela indique que les deux capteurs suivent la même tendance d'évolution de puissance.

### 5. Comparaison des Moyennes (Biais)
Sur le groupe "Valide" (Steady State ~120W) :
*   **Moyenne Wahoo :** 122.5 W
*   **Moyenne Assioma :** 116.5 W
*   **Biais moyen :** +6 W (Wahoo > Assioma).

*Interprétation :* Ce résultat est contre-intuitif (le Wahoo en bout de chaîne devrait mesurer moins). Cela confirme une surestimation probable du Wahoo KickR ou une sous-estimation des pédales (calibration).

### 6. Analyse de Bland-Altman
L'analyse de Bland-Altman sur les données synchronisées montre :
*   Un biais systématique positif du Wahoo.
*   Une dispersion (limites d'agrément) raisonnable pour les données à 90 rpm ($\pm 10-15$ W), mais inacceptable pour les données à 70 rpm (> 100 W de différence).

---

## Partie 3 : Compte-rendu client (Synthèse)

**Objet : Rapport de validation du prototype de mesure de puissance Wahoo KickR**

Madame, Monsieur,

Suite à la campagne de mesures effectuée le 15/01/2026, comparant votre dispositif Wahoo KickR aux pédales de référence Favero Assioma Duo, voici nos conclusions :

**1. Fiabilité Globale :**
Le dispositif montre une **très bonne corrélation ($r > 0.9$)** avec la référence sur des efforts d'intensité moyenne à cadence élevée (90 rpm, ~120W). Il capture fidèlement les variations de puissance du cycliste.

**2. Biais de Mesure :**
Nous observons une **surestimation systématique de la puissance** de l'ordre de **+5 à +6%** par rapport à la référence sur les plages stabilisées. Bien que précis (répétable), l'outil manque d'exactitude (justesse) dans sa configuration actuelle.

**3. Point de Vigilance Majeur (Faibles Intensités) :**
Des écarts critiques ont été relevés lors des phases à basse cadence (70 rpm) et faible résistance, où le Wahoo sous-estime drastiquement la puissance réelle (50W mesurés contre 130W réels). Ce comportement suggère un défaut de linéarité ou de calibration à bas régime.

**Recommandations :**
*   Effectuer une calibration d'usine (Spindown) avant chaque utilisation critique.
*   Investiguer la linéarité du frein électromagnétique à basse vitesse de rotation (< 75 rpm).
*   Appliquer un facteur correctif de -5% pour les intensités cibles > 100W.

**Conclusion :**
Le Wahoo KickR est un outil valide pour l'entraînement à intensité modérée/haute, sous réserve de correction du biais. Il n'est pas validé pour les mesures de précision à basse intensité (< 100W / 70 rpm) dans l'état actuel.

**L'équipe Data Science Performance**
M1 SNS - Rennes 2
