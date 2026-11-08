# Projet IA Go – Joueur Intelligent avec Ouvertures, Modèle Neuronal et Capture Stratégique

## 🧠 Objectif
Ce projet implémente un joueur de Go intelligent respectant l'interface `PlayerInterface` du tournoi. Il prend ses décisions en combinant :

- des coups d’ouverture issus de parties professionnelles (jouées depuis un arbre théorique),
- la détection de groupes ennemis capturables,
- un modèle de réseau de neurones entraîné pour évaluer les positions.

---

## 📁 Structure du projet

### `theorie.py`
Ce fichier implémente la logique de **l’arbre d’ouvertures** :

- **`Node`** : représente un coup joué.
- **`GameTree`** : structure permettant de stocker et d'explorer plusieurs parties.
- Utilise les parties contenues dans le fichier `plays.json` pour construire une base d’ouvertures.
- Permet de prédire des coups d'ouverture de manière guidée et optimisée.



---

### `model.py`
Contient le **modèle de réseau de neurones** utilisé pour évaluer une position donnée du plateau :

- Architecture CNN + couches fully connected.
- Retourne une **probabilité de victoire** pour le joueur donné, à partir de l’historique des coups.
- Prétraitement des données d’entrée avec `array_data()`.
- Le modèle est chargé depuis le fichier `mon_modele.pth`.

### `mon_modele.pth`
Fichier contenant les **poids entraînés** du modèle PyTorch. Il a été entraîné en amont sur des parties historiques pour apprendre à prédire le gagnant depuis une configuration du plateau.

---

### `myPlayer.py`
C'est le **joueur principal**, qui implémente la classe `PlayerInterface`. Il suit une logique de décision hybride :

1. **Coups d'ouverture** : 
   - Si l'ouverture est connue (dans l’arbre d’ouvertures), on suit la séquence théorique.
   
2. **Capture stratégique** :
   - Recherche les **chaînes adverses avec peu de libertés** (liberté ≤ 1 ou 2) en exploitant les structures internes du plateau (`_stringLiberties`).
   - Joue le coup qui permettrait une **capture immédiate**.

3. **Évaluation par le modèle** :
   - Si aucun coup théorique ni capture n’est possible, on explore les coups légaux et on choisit celui avec la meilleure probabilité de victoire selon le modèle (`model.py`).

---




## ✍️ Auteurs

Omar EL Alaoui El Ismaili et Ossama Aidoun

