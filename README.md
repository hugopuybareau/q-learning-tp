# M2IA UE Intelligent Agents - TP1

Dans ce projet, vous allez implémenter les algorithmes Value Iteration, Q-learning tabulaire et approximé. 
Ces algorithmes seront testés sur différents environnements simulés (labyrinthes, un petit robot crawler, jeu de Pacman).

## Installation
Le code est écrit en python 3.6. Pour créer un environnement virtuel pour votre TP, les explications sont [ici](README_conda.md). 

## Rendu du TP
Vous devez pousser vos modifications dans votre projet git avant la date limite (date du commit faisant foi).


## Introduction

Dans ce TP, vous devrez modifier les fichiers suivants:
- `valueIterationAgents.py`: définition de la classe `ValueIterationAgent` pour un agent planifiant avec l'algorithme Value Iteration
- `qlearningAgent.py`: définition des différentes classes d'agent utilisant le Q-learning.
- `featureExtractors.py`: définition des fonctions caractéristiques pour le Q-learning approximé.

et compléter le fichier [RAPPORT.md](RAPPORT.md) en utilisant le [formalisme MarkDown](https://guides.github.com/features/mastering-markdown/)

Les fichiers suivants peuvent être intéressants à regarder mais ne sont pas à compléter:
- `mdp.py`: classe abstraite `MarkovDecisionProcess` et méthodes permettant de définir un MDP complet, nécessaire en planification
- `environment.py`: classe abstraite `Environment` et méthodes permettant de définir un environnement pour l'apprentissage par renforcement
- `learningAgents.py`: définition des classes mères des agents à compléter
- `util.py`: fonctions utilitaires
- `gridworld.py`: modélisation des labyrinthes sous forme de MDP 
- `crawler.py`: modélisation de l'environnement robot crawler pour l'apprentissage par renforcement
- `featureExtractors.py`: utilisé par le QLearning approximé (classe `ApproximateQAgent`) pour extraire des features sur les (états,actions)

Les autres fichiers peuvent être ignorés.

## Partie 1: Value Iteration

### Modélisation sous forme de MDP des labyrinthes
Contrôler manuellement un agent dans le labyrinthe par défaut:

`` python gridworld.py -m``

Visualiser dans la console les récompenses obtenues dans chaque état pour bien comprendre la modélisation du labyrinthe sous forme de MDP utilisée ici, qui est différente de celle utilisée dans le CM.

Changer les options (liste: `` python gridworld.py -h``) pour avoir un environnement déterministe, des récompenses à chaque transition, modifier le labyrinthe, ...

L'agent par défaut se déplace aléatoirement: 

`` python gridworld.py -g MazeGrid``

### Algorithme Value Iteration 

Compléter `valueIterationAgents.py` pour obtenir un agent qui planifie en utilisant l'algorithme Value Iteration.
- vous utiliserez la version *batch* de l'algorithme où la fonction de valeur à l'itération *k* est calculée à partir de la fonction de valeur à l'itération *k-1*.


Pour tester votre agent, regarder les valeurs et la politique obtenues sur les 3 premières itérations dans l'environnement BookGrid avec les paramètres par défaut: 

`` python gridworld.py -a value -i 3 -k 0 -v``

Vérifier les valeurs obtenues avec les valeurs théoriques. 

**Question 1: Préciser dans le rapport le détail du calcul de la politique gloutonne sur les 3 premières itérations.**

Observer la politique optimale et le comportement de l'agent après convergence :

``python gridworld.py -a value -k 2``

### Influence des paramètres

On s'intéresse maintenant à l'influence des différents paramètres sur la politique optimale calculée. 

On considère tout d'abord le labyrinthe *BridgeGrid* dont la politique optimale avec les valeurs par défaut ne permet pas à l'agent de traverser le pont (i.e. d'atteindre la récompense de 10):

``python gridworld.py -g BridgeGrid -a value -k 1``

**Question 2: Modifier un seul des 2 paramètres (noise ou discount) pour obtenir une politique optimale qui permet à l'agent de traverser le pont (s'il n'était pas soumis au bruit). Préciser le paramètre modifié et sa valeur dans votre rapport et justifier votre choix.**


Dans le labyrinthe *DiscountGrid* on distingue 2 types de chemins :
- des chemins courts mais risqués qui passent près de la ligne du bas ; ces chemins sont représentés par la flèche rouge ;
- des chemins plus longs mais sûrs qui passent par le haut du labyrinthe ; ces chemins sont représentés par la flèche verte.

![chemins](discountgrid.png)

Les valeurs par défaut permettent d'obtenir une politique optimale qui suit un chemin sûr pour atteindre l’état absorbant de récompense 10.

``python gridworld.py -g DiscountGrid -a value -k 1``

Vous devez essayer d'obtenir les politiques optimales ci-dessous en ne modifiant à chaque fois qu'**un seul des 3 paramètres (noise, discount, livingReward)** (un paramètre non modifié prend sa valeur par défaut):
1. qui suit un chemin risqué pour atteindre l’état absorbant de récompense +1 ;
2. qui suit un chemin risqué pour atteindre l’état absorbant de récompense +10 ;
3. qui suit un chemin sûr pour atteindre l’état absorbant de récompense +1 ;
4. qui évite les états absorbants


**Question 3: Modifier un seul des 3 paramètres (noise, discount, livingReward) pour obtenir les politiques optimales précédentes. Préciser pour chaque politique, le paramètre modifié et sa valeur dans votre rapport et justifier votre choix.**


## Partie 2: QLearning tabulaire

L'agent codé dans la partie 1, qui utilise l'algorithme value iteration, possède un modèle de son environnement (ici un labyrinthe) sous forme de MDP. Ce modèle MDP lui permet de calculer une politique optimale avant même d'interagir avec son environnement (phase hors-ligne).
Lorsqu'il interagit avec l'environnement (phase en-ligne), il suit simplement la politique précalculée. Cette distinction peut être subtile dans un environnement simulé comme une grille, mais elle est très importante dans le monde réel, où le vrai MDP de l'environnement d'un robot est rarement disponible.


L'objectif de cette partie est d'implémenter un agent qui apprend à partir de ses interactions avec l'environnement, sans connaitre le MDP modélisant son environnement.

### Agent manuel

Compléter dans la classe `QLearningAgent` (dans `QLearningAgent.py`) toutes les méthodes sauf `getAction`.
- Pour l'implémentation du *argmax*, vous devez résoudre les égalités de manière aléatoire pour un meilleur comportement.
- Assurez-vous de toujours accéder et modifier les Q valeurs en utilisant `getQValue` et `setQValue` (car ces fonctions sont redéfinies dans les classes filles)

Tester votre agent en le déplacant manuellement:

`python gridworld.py -a q -k 5 -m`

Vérifier les valeurs obtenues avec les valeurs théoriques sur les 4 épisodes suivants: les 2 premiers épisodes, l'agent va tout au nord puis tout à l'est (récompense de +1), les 3eme et 4eme épisodes il va tout à l'est puis au nord (récompense de -1). 

**Question 4: Préciser dans le rapport le détail du calcul des valeurs théoriques.**

### Epsilon greedy

Compléter dans la classe `QLearningAgent` (dans `QLearningAgent.py`) la méthode `getAction` pour appliquer une stratégie epsilon-greedy.

Observer le comportement de l'agent:

`python gridworld.py -a q -k 100`

et la politique optimale obtenue après 100 épisodes:

`python gridworld.py -a q -k 100 -q`

Comparer les résultats avec différentes valeurs pour *epsilon*.

`python gridworld.py -a q -k 100 --noise 0.0 -e 0.1 -q`

`python gridworld.py -a q -k 100 --noise 0.0 -e 0.9 -q`

**Question 5: Expliquer dans le rapport les différences entre le résultat obtenu avec epsilon à 0.1 et à 0.9.**

### Robot *crawler*

Tester votre agent avec le robot *crawler*:

`python crawler.py`

**Question 6: Expliquer dans le rapport la modélisation de cet environnement sous forme de MDP, en précisant S et A ainsi que la fonction de récompense R (regarder le fichier `crawler.py`). Quelle est la dimension de l'espace d'états ? Quel est le comportement attendu de l'agent s'il suit sa politique optimale ?**

Vérifier que votre agent apprend bien le comportement optimal (vous pouvez modifier les paramètres via l'interface graphique).

### Pacman avec QLearning tabulaire

L'algorithme QLearning tabulaire va maintenant être utilisé pour apprendre à un agent Pacman à jouer.

Tester tout d'abord votre niveau à Pacman:

`python pacman.py`

Le score est modifié à chaque étape d'une partie avec:
- +500 si le pacman a mangé tous les dots (gagne la partie)
- +200 si le pacman mange un fantome effrayé (les fantomes passent en mode effrayé pendant un certain temps lorsque le pacman mange une capsule (*big dot*))
- +10 si le pacman mange une nourriture
- -1 à chaque étape
- -500 si le pacman perd la partie (se fait manger par un fantome)

La modélisation des différents éléments du MDP pour le jeu de Pacman est la suivante:
- les actions possibles pour le Pacman à chaque étape sont l'ensemble des actions qui ne l'emmènent pas dans un mur
- la récompense à chaque étape d'une partie est la différence entre le score actuel et le score à l'étape précédente.
- l'état du MDP contient les coordonnées de l'ensemble des entités (Pacman et fantômes), les positions des nourritures, capsules, murs, et le score.

L'apprentissage se fait en 2 phases:
- une phase d'*entrainement*: l'agent va apprendre des Qvaleurs en jouant un certain nombre de parties (ou épisodes). Les valeurs par défaut sont précisées dans la classe `PacmanQAgent` de `QLearningAgent.py`. Elles sont modifiables avec l'option `-a epsilon=0.1,alpha=0.3,gamma=0.7`
- une phase de *test*: l'apprentissage et l'exploration sont stoppés (*epsilon* et *alpha* mis à 0) pour évaluer la politique obtenue sur plusieurs parties.

Tester votre agent codé précédemment en lançant la commande ci-dessous  (des statistiques sont affichées dans la console):

- `python pacman.py -p PacmanQAgent -x 2000 -n 2010 -l smallGrid`
- `python pacman.py -p PacmanQAgent -x 2000 -n 2010 -l mediumGrid`

**Question 7: Expliquer les résultats obtenus et préciser dans le rapport les solutions que l'on peut mettre en place pour améliorer ces résultats.**



## Partie 3: QLearning approximé

Pour améliorer l'apprentissage de l'agent dans des grilles plus complexes, vous devez maintenant implémenter le QLearning approximé.

Le Qlearning approximé utilise des fonctions caractéristiques (*feature*) qui doivent hériter de la classe `FeatureExtractor` (dans `featureExtractors.py`).

2 classes filles de `FeatureExtractor` sont proposées:
- `IdentityExtractor` réalise un encodage *one-hot*; ainsi, le QLearning approximé est équivalent au QLearning tabulaire (utile pour debugger le QLearning approximé)
- `SimpleExtractor` utilise plusieurs fonctions caractéristiques spécifiques au Pacman (allez regarder dans cette classe les fonctions caractéristiques utilisées !).

Compléter la classe `ApproximateQAgent` (dans `QLearningAgent.py`).

Tester votre agent avec `IdentityExtractor` pour vérifier que le résultat est similaire au QLearning tabulaire:

`python pacman.py -p ApproximateQAgent -x 2000 -n 2010 -l smallGrid` ça ok

Tester votre agent avec `SimpleExtractor` dans différents labyrinthes:

`python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumGrid` ok 

`python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic` hmm des fois il perd quand même donc jsp

Votre agent devrait gagner presque toutes les parties, même dans des labyrinthes plus complexes, et avec moins d'épisodes d'entrainement.

Les features proposées dans `SimpleExtractor` ignorent les capsules. Compléter la classe `ExpertExtractor` (dans `featureExtractors.py`) pour considérer les capsules et permettre à l'agent pacman de chasser les fantômes. Tester dans des labyrinthes avec capsule (d'autres labyrinthes sont présents dans le dossier `layout`, par ex. smallClassic et capsuleClassic).

**Question 8: Expliquer dans le rapport les features que vous avez implémentées et leurs rôles. Présenter et analyser les résultats obtenus.**


