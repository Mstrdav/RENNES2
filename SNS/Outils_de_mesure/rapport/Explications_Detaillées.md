# Guide Explicatif Détaillé (Pour les non-spécialistes)

Ce document accompagne le rapport technique pour expliquer la démarche, les choix méthodologiques et l'interprétation des résultats, question par question.

---

## Contexte : De quoi parle-t-on ?

Nous avons comparé deux appareils qui mesurent la puissance (l'effort) d'un cycliste :

1. **Wahoo KickR (Home Trainer) :** Le vélo est posé dessus (on enlève la roue arrière). Il mesure la puissance au niveau de la chaîne/cassette.
2. **Favero Assioma (Pédales) :** Ce sont les pédales qui mesurent la force directement sous le pied. C'est considéré comme la référence ("la vérité").

**Le but :** Savoir si le Wahoo KickR dit la vérité (est-il valide ?) ou s'il se trompe.

---

## Partie 1 : Comprendre les outils

### Q1. La Puissance Mécanique

* **C'est quoi ?** C'est l'énergie produite par seconde. En vélo, c'est simple : c'est la force avec laquelle tu appuies sur la pédale (**Couple**) multipliée par la vitesse à laquelle tu tournes les jambes (**Cadence**).
* **Pourquoi c'est important ?** C'est le seul indicateur objectif de l'effort. La vitesse dépend du vent, le cœur dépend du stress... les Watts ne mentent pas.

### Q2. Comment ils mesurent ?

* **Wahoo (Le Hometrainer) :** Il freine la roue avec des aimants. Il sait combien de force il met pour te freiner, et à quelle vitesse tu tournes. C'est une estimation indirecte (en bout de chaîne).
* **Assioma (Les Pédales) :** Elles contiennent des minuscules capteurs qui se déforment quand tu appuies dessus (jauges de contrainte). Elles mesurent la force réelle appliquée par le pied. C'est une mesure directe.

### Q3 & Q4. Lequel croire ?

On croit les **Pédales (Assioma)**.

* *Pourquoi ?* Parce qu'elles mesurent l'énergie *à la source* (le pied).
* Le Home Trainer mesure *après* que la chaîne a frotté, que les roulements ont tourné... Il y a de la perte d'énergie (frottements). Donc logiquement, le Home Trainer devrait afficher *moins* de Watts que les pédales. Si ce n'est pas le cas, c'est suspect !

---

## Partie 2 : La Validation (Le cœur du TP)

### Q1. Le Protocole (Ce qu'on a fait)

On a demandé aux étudiants de rouler à vitesse stable (70 tours/minute puis 90 tours/minute) et de faire des sprints à fond. On a enregistré les deux capteurs en même temps.

### Q2. Le Problème Technique (Synchronisation)

* **Le Souci :** Les deux appareils n'étaient pas réglés à la même heure ! L'un disait "il est 10h00:05" et l'autre "il est 10h00:12". Impossible de comparer point par point si on a 7 secondes de décalage (quand tu arrêtes de pédaler, l'un affiche 0W et l'autre encore 200W).
* **La Solution (Cross-Correlation) :** J'ai utilisé un algorithme mathématique qui fait "glisser" les deux courbes l'une sur l'autre jusqu'à ce qu'elles se superposent parfaitement. C'est comme caler le son et l'image d'un film.

### Q3. Reproductibilité (Sprints)

C'est la capacité de l'appareil à donner le même résultat pour le même effort. Sur les sprints, c'est dur à voir car les horloges étaient trop décalées. Mais visuellement, les pics de puissance semblent cohérents.

### Q4. La Corrélation (Est-ce que ça suit la même courbe ?)

* **Principe :** Si le Wahoo monte de 10 Watts, les Pédales doivent monter de 10 Watts.
* **Résultat :** Pour les efforts intenses (90 tours/min), OUI ($r > 0.9$). Les courbes se ressemblent comme deux gouttes d'eau. C'est une bonne nouvelle.

### Q5 & Q6. Le Biais (Est-ce que c'est la bonne valeur ?)

* **Le Hic :** Même si les courbes se ressemblent, elles ne sont pas au même niveau.
* **Résultat :** Le Wahoo affiche en moyenne **+6 Watts** de plus que les pédales.
* **Pourquoi c'est bizarre ?** Comme expliqué plus haut, il devrait en afficher *moins* (à cause des pertes mécaniques). S'il en affiche plus, c'est qu'il "sur-estime" l'effort. Il est "généreux".
* **Le cas des 70 rpm :** Pour certains étudiants qui roulaient doucement (70 tours/min), le Wahoo affichait 50W alors que les pédales disaient 130W ! C'est un énorme bug de mesure à basse vitesse.

---

## Partie 3 : Conclusion pour le Client

Si vous achetez ce Wahoo KickR :

1. **Pour s'entraîner dur (Sprints, Intensité) :** C'est super, il réagit bien.
2. **Pour la précision absolue :** Attention, il vous "donne" environ 5% de puissance en trop. Ne vous comparez pas à un pro qui utilise des pédales, vos chiffres sont gonflés.
3. **Pour la promenade (Basse vitesse) :** À éviter, il n'est pas fiable du tout en dessous de 100 Watts.
