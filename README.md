# Crash crawler for Mozilla crashes

OPL - Thème 2: Crash Analysis

14/11/2016

Denis Hamann - Nathan Baquet

## Table des matières
**[Introduction](#introduction)**  
**[Travail technique](#travail-technique)**  
**[Evaluation](#evaluation)**  
**[Limitation](#limitation)**  
**[Conclusion](#conclusion)**  
**[Glossaire](#glossaire)**

## Introduction
Le but premier de ce projet est de développer un outil qui permet de récupérer des rapports de crash de Mozilla Firefox afin de récolter au moins 20 000 rapports sur les deux dernières version de Firefox.
Au cours de l’avancement du projet, nous avons défini des objectifs supplémentaires. Etant donné que nous avions des données précieuses, nous avons pu en sortir des métriques. Nous nous sommes malgré tout limité à l'analyse de xxxxx Ecrire ici très brièvement ce qu'on a ciblé comme analyse.xxxxxxxxxxxxxxxxxxxxx


### Contexte

L'objectif de ce projet était assez général : analyser des crashs. Seulement, il n'est pas évident de trouver des rapports de crash de manière publique et dans une quantité assez grande que pour pouvoir les analyser ou travailler dessus. La fondation Mozilla Firefox a lancé "Super Search" qui est une interface aux données de rapport de crash. C'est un outil accessible à tout le monde via une interface graphique ou via une API. "Super Search" est donc une mine d'or d'information et répond parfaitement à ce que l'on a besoin pour ce cours.


## Travail technique
### But
Le travail technique n'est pas un but en lui-même, c'est plutot les résultats et l'analyse de ceux-ci qui nous intéressent ici. Le but est de collecter un maximum de données afin de pouvoir analyser celles-ci. Vu la quantité et qualité de données extraites, les possibilités d'analyse sont grandes et peuvent être faites de manières différentes et dans des buts différents. Nous nous sommes concentrés sur l'analyse de xxxxxxxxxx

### Technologies et langages utilisés

Pour ce projet, nous avons utilisé le langage Python (https://www.python.org/), d'une part pour le script qui permet d'extraire les données et d'autre part pour le script qui permet d'analyser les données.

Concerneant la répartition des fichiers :

- extract_data.py : script qui permet d'extraire les rapports de bug.
- diff_bucket_by_version.py : script qui permet d'analyser les données, comparaison et statistiques de présence de certains buckets entre deux versions

### Algorithme

Le seul algorithme important de notre système à décrire est celui qui pré-sélectionne les intégrateurs par rapport aux Pull Requests qui ne sont pas encore assignées.

Un algorithme important dans notre projet est celui qui permet de déterminer les changements de buckets entre deux version.
Le principe consiste à ... xxxxxxxxxx

```javascript
//Try to determine a type for each pull request
for pullRequest in pullRequestToAssign
    files = http.get(pullRequest.urlFiles)
    if (files.contains(keywordFront))
        pullRequest.type = "Front"
    else if (files.contains(keywordBack))
        pullRequest.type = "Back"
    (...)
end for

//Assign integrator
for pullRequest in pullRequestToAssign
    integra = integrators.compare(integra1, integra2)
        if(integra1.type == integra2.type)
            return min(integra1.number, integra2.number
        if(integra1.type == pullRequest.type)
            return integra1
        if(integra2.type == pullRequest.type)
            return integra2
        return min(integra1.number, integra2.number
    end compare

    pullRequest.assigned = integra
end for
```

### Utilisation
Script d'extraction :
- python extract_data.py

Le script peut être arrêté et repris plus tard, des informations à l'écran sur la progression sont affichées.

Script d'analyse :
- python diff_bucket_by_version.py

- Le script génère deux fichiers:
1. une page html avec un tableau graphique
2. un rapport de comparaison pour chaque version deux par deux.

### Screenshots

Voici un exemple de résultat au lancement du script d'analyse.
![Résultat analyse](https://raw.githubusercontent.com/Oupsla/Dashboard-Pr/master/public/images/Selection.png)

## Evaluation

parler beaucoup ici de pourquoi on a décidé d'analyser ces données-là, dans quel but, pour qui (les dév mozz) ?
commenter ici (du mieux qu'on peut) pourquoi c'est un bon algo de bucketing et pourquoi pas la comparer avec un autre (montrer qu'on a cherché d'autres algo de bucketing).
pourquoi est-ce qu'on a choisi ces métriques-là ?

dire ce qu'on aurait pu faire d'autre, ou en plus, d'autres idées que celle sur laquelle on s'est concentré : ex: quelle fonction fait le plus crasher ou bien chercher l'explosive https://wiki.mozilla.org/CrashKill/Plan/Explosive ?


## Limitation

- vitesse (requêtes) du script d'extraction
- quantité de données à extraire + analyser
- limitation de nos comparaisons (par exemple la date, le nombre de versions, etc.)
-


## Conclusion


dire que les objectifs de base est atteint et les objectifs secondaires qu'on a ciblés sont aussi atteint. Que ça répond à l'attente.

## Glossaire
- Bucket :
- Crawler :
