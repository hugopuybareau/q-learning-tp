# RAPPORT

## Partie 1: Value Iteration

### Question 1 
*Préciser le détail du calcul de la politique gloutonne pour les 3 premières itérations de Value Iteration dans l'environnement BookGrid avec les paramètres par défaut*

### Question 2
*Modifier un seul des 2 paramètres (noise ou discount) pour obtenir une politique optimale qui permet à l'agent de traverser le pont (s'il n'était pas soumis au bruit). Préciser le paramètre modifié et sa valeur dans votre rapport et justifier votre choix.*

Paramètre modifié: `noise = 0.0` (au lieu de 0.2)

Justification:
Le problème avec les paramètres par défaut est que le bruit (noise=0.2) crée un risque de 20% de dévier perpendiculairement à la direction souhaitée. Sur le pont, cela signifie:

Probabilité de 0.2 de tomber dans les cases -100
Perte espérée par déplacement: 0.2 × (-100) = -20

Ce qui donne pour le calcul de l'espérance:
`E(traverser) = P(succés) × 10 + P(échec) × (-100)`
5 étapes et le bruit à 0.2:
 - `P(success) = 0.8^5 ≈ 0.33`
 - `P(failure) ≈ 0.67`
Soit `E(traverser) ≈ 0.33×10 + 0.67×(-100) = 3.3 - 67 = -63.7`
vs `E(rester) = 1`

Avec 5 déplacements nécessaires pour traverser: risque cumulé très élevé

En mettant noise = 0.0:

 - L'environnement devient déterministe
 - L'agent peut traverser sans risque de tomber
 - La récompense +10 devient atteignable sans danger avec `E(traverser) = 10`
 - La politique optimale dirigera l'agent vers la droite pour obtenir +10


### Question 3
*Modifier un seul des 3 paramètres (noise, discount, livingReward) pour obtenir les politiques optimales ci-dessous. Préciser pour chaque politique, le paramètre modifié et sa valeur dans votre rapport et justifier votre choix.*

1. qui suit un chemin risqué pour atteindre l’état absorbant de récompense +1 ;
2. qui suit un chemin risqué pour atteindre l’état absorbant de récompense +10 ;
3. qui suit un chemin sûr pour atteindre l’état absorbant de récompense +1 ;
4. qui évite les états absorbants

1. Chemin risqué vers +1

Paramètre modifié: `discount = 0.1`
Pourquoi: Avec un discount très faible, l'agent privilégie les récompenses immédiates. Le chemin le plus court vers +1 (3 actions) devient optimal malgré le risque de tomber dans -10. Les pénalités futures sont fortement dévaluées.

3. Chemin sûr vers +1

Paramètre modifié: `discount = 0.3`
Pourquoi: Avec un discount un peu haut, les récompenses futures conservent un peu plus leur valeur, l'agent va pouvoir se projeter en passant par le haut mais pas au point d'aller chercher le +10.

2. Chemin risqué vers +10
Paramètre modifié: `livingReward = -1`
Pourquoi: Avec une pénalité de 1 par étapes en vie, l'agent est encouragé à terminer rapidement. Un +1 n'étant pas suffisant pour combler ses pertes, il se dirige vers le +10 avec le chemin le plus court. 

4. Chemin évitant les états absorbant de récompense +1
Paramètre modifié: `livingReward = 1`
Pourquoi : Il gagne 1 par étape donc l'espérance de gain en allant sur une autre case sera toujours plus forte que celle d'aller sur un état absorbant +1.

## Partie 2: QLearning tabulaire

### Question 4
*Précisez le détail du calcul des qvaleurs pour les 3 premiers épisodes.*

### Question 5
*Expliquer les différences entre le résultat obtenu avec epsilon à 0.1 et à 0.9.*

### Question 6
*Préciser comment est modélisé l'environnement robot crawler sous forme de MDP (état, action, récompense) ainsi que la dimension de S. Quel est le comportement attendu de l'agent s'il suit sa politique optimale ?*


### Question 7
*Expliquer les résultats obtenus et préciser dans le rapport les solutions que l'on peut mettre en place pour améliorer ces résultats.*

### Question 8
*Expliquer dans le rapport les features que vous avez implémentées et leurs rôles. Présenter et analyser les résultats obtenus.*




