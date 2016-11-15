# Crash crawler for Mozilla crashes

OPL - Thème 2: Crash Analysis

What is a crash? How to detect it? How to collect it? How to analyze crashes? What to put in crash report? What are the issues related to privacy and law? What is a bucket? What is a stack trace? What are the technical limitations and tradeoffs or crash analysis? Which crash to fix first?

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
Le but initial de ce projet est de développer un outil permettant de récupérer des rapports de crash de Mozilla Firefox afin de récolter au moins 20 000 rapports sur les deux dernières versions de Firefox.
Au cours de l’avancement du projet, nous avons défini des objectifs supplémentaires. Etant donné que nous avions des données précieuses, nous avons pu en sortir des métriques. Nous nous sommes malgré tout limités à l'analyse des buckets entre les différentes versions de Firefox.


### Contexte

L'objectif de ce projet était assez général : analyser des crashs. Seulement, il n'est pas évident de trouver des rapports de crash de manière publique et dans une quantité assez grande que pour pouvoir les analyser ou travailler dessus. La fondation Mozilla Firefox a lancé "Super Search" qui est une interface aux données de rapport de crash. C'est un outil accessible à tout le monde via une interface graphique ou via une API. "Super Search" est donc une mine d'or d'information et répond parfaitement à ce que l'on a besoin pour ce cours.


## Travail technique
### But
Le travail technique n'est pas un but en lui-même, c'est plutôt les résultats et l'analyse de ceux-ci qui nous intéressent ici. Le but est de collecter un maximum de données afin de pouvoir analyser celles-ci. Vu la quantité et qualité de données extraites, les possibilités d'analyse sont grandes et peuvent être faites de manière différente et dans des buts différents. Nous nous sommes concentrés sur l'analyse des ajouts et suppressions de buckets entre les différentes versions de firefox (et donc par extension des introductions et correction de bugs).

### Technologies et langages utilisés

Pour ce projet, nous avons utilisé le langage Python (https://www.python.org/), d'une part pour le script qui permet d'extraire les données et d'autre part pour le script qui permet d'analyser les données.

Concernant la répartition des fichiers :

- extract_data.py : script qui permet d'extraire les rapports de bug.
- diff_bucket_by_version.py : script qui permet d'analyser les données, comparaison et statistiques de présence de certains buckets entre deux versions

### Algorithme

Un algorithme important dans notre projet est celui qui permet de déterminer les changements de buckets entre deux versions.
Le principe consiste à parcourir toutes les signatures des crash pour deux versions, et de déterminer si les signatures de l'une sont présentes dans l'autre.

```python
def determineChanges(signatures1, signatures2):
    result = defaultdict(list)
    for signature in signatures1:
        if signature not in signatures2 and signature not in result['corrected']:
            result['corrected'].append(signature)
    for signature in signatures2:
        if signature not in signatures1 and signature not in result['introduced'] and signature not in result['corrected']:
            result['introduced'].append(signature)
        elif signature not in result['remaining'] and signature not in result['introduced'] and signature not in result['corrected']:
            result['remaining'].append(signature)
        else :
            result['doubles'].append(signature)
    return result
```
### Utilisation
Script d'extraction :
* python extract_data.py

    Le script peut être arrêté et repris plus tard, des informations à l'écran sur la progression sont affichées.

* Script d'analyse :
    * python diff_bucket_by_version.py

    * Le script génère deux sorties:
        * une page html avec un tableau indiquant le nombre de buckets corrigés|introduits|restants entre deux versions
        * un rapport de comparaison pour chaque version deux par deux.

### Screenshots

Voici un exemple de résultat au lancement du script d'analyse.
![Résultat analyse](http://nsa37.casimages.com/img/2016/11/14/161114112419160221.jpg)

## Evaluation
Dans un premier temps nous devions récupérer un grand nombre de crashs-report, ce que nous avons accompli avec succès.
Mais une fois ces données récupérées nous devions en tirer des métriques intéressantes. Nous avons principalement eu deux idées:

- comparer le nombre buckets disparus/apparus entre plusieurs versions pour essayer d'en tirer des généralités.
- comparer plusieurs algorithmes de bucketing pour déterminer lequel est le plus efficace.

Nous sommes partis sur la première idée car la seconde nous semblait difficilement réalisable dans le temps imparti (il n'en est pas moins interressant pour autant!).

#### Comment avont nous récupéré les buckets

Le mot clef bucket n'est jamais mentionné dans la documentation de Mozilla. Néanmoins il existe une valeur similaire appelé "signature".

####Pourquoi cette signature est un bucket

Elle est utilisée par la fondation mozilla pour caractériser un crash report et trouver d'autres crashs similaires.

![Crash report mozilla](http://nsa37.casimages.com/img/2016/11/14/16111411384447573.jpg)

####Comment a-t-on récupéré l'ensemble des signatures des crashs
Via l'api SuperSearch ; plus précisément via cette requète :
    https://crash-stats.mozilla.com/api/SuperSearch/?product=Firefox&_facets=signature
## Limitations

- vitesse (requêtes) du script d'extraction
- quantité de données à extraire + analyser
- Nos requètes se basent uniquement sur les crash-reports des sept derniers jours
- Du fait de la limite précédente , il y a tès peu de crash reports sur les versions les plus anciennes -> potentiellement des buckets qui existaient mais qui ne sont pas apparus les sept derniers jours
- Bien qu'ayant des résultats cohérents pour l'algo d'analyse dans le rapports .Les stats version par version sont étranges -> problème dans la requête?ou alors mozilla change régulièrement ses buckets


## Conclusion


dire que les objectifs de base est atteint et les objectifs secondaires qu'on a ciblés sont aussi atteint. Que ça répond à l'attente.

## Glossaire
- Bucket :
- Crawler :
