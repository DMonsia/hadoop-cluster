# hadoop-cluster

Ce projet consiste à construire un cluster Hadoop avec des conteneurs Docker.
Une fois le cluster créé, nous installons un ensemble d'outils de l'écosystème hadoop à savoir Spark, Sqoop, Hbase, Storm, … Puis les mettrons en œuvre via des mini projets de data science.

Pour déployer le framework Hadoop, nous allons utiliser des contenaires Docker. 

## Preparation de l’environments
### Installation de Docker

Docker est un système de conteneurisation, c'est-à-dire d’isolation d’application et toutes ses dépendances dans un mini système d'exploitation (OS) appelé conteneur. 

L'installation de docker dépend du système d’exploitation de votre machine (système hôte).
Les détails de l’installation sont dans le fichier `docker-instalation.md`.

### Création du claster
make permet d'exécuter les commandes contenues dans le `Makefile` pour créer de manière soft le cluster hadoop de trois machines: un master et deux slaves. 

Chaque machine est dans un conteneur docker. L’ensemble de ces conteneurs sont mis dans un réseau afin de constituer notre cluster. 

1. Ouvrez un terminal (Ubuntu) ou powershell (Windows) dans le dossier du projet et entrez successivement les deux commandes ci-dessous.

```
make build
make create-network 
make create-master
make create-slave hostname=slave1 port=8040
make create-slave hostname=slave2 port=8041
```
2. Vérifier la création du claster
```
docker ps
```
Cette commande va vous afficher la liste de conteneur créer qui sont actifs. 

## Prise en main hadoop

### CLI

1. Entrer dans le conteneur master en mode bash pour commencer à l'utiliser.
```
docker exec -it master bash
```
Le résultat de cette exécution sera le suivant:

```
root@master:~#
```
Vous êtes à l'intérieur du conteneur. Vous pouvez l’explorer:
- `ls` : lister les fichiers du répertoire courant (répertoire dans le que le terminal est ouvert)
- `pwd` : voir le chemin absolu ver le répertoire courant
- `cd` [path] : remplace path par le chemin vers le répertoire ou vous voulez vous rendre.
Bref, c’est une machine ubuntu, amusez-vous.


2. Démarrer hadoop et yarn
Un script est fourni pour cela, appelé `start-hadoop.sh`. Lancer ce script.

```
cd ~
ls
```
```
./start-hadoop.sh
```
Des autorisations de connexions peuvent être demandées, entre `yes` à chaque fois.

3. Créer un répertoire dans HDFS, appelé `input`.
```
hadoop fs -mkdir -p /user/root/input
```
4. Ajouter un fichier texte dans hadoop HDFS
 - Télécharger le fichier
 ```
 wget https://github.com/CodeMangler/udacity-hadoop-course/raw/master/Datasets/purchases.txt.gz
 ```
 - Décompresser le fichier
 ```
 gunzip purchases.txt.gz
 ```
 ```
 ls -lh
 ```
- Ajouter le fichier dans HDFS
 ```
 hdfs dfs -put purchases.txt input
 ```
- Vérifier que le fichier à été bien ajouter dans HDFS
 ```
 hdfs dfs -ls input
 ```
Cliquez [ici](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://images.linoxide.com/hadoop-hdfs-commands-cheatsheet.pdf) pour plus de commandes hadoop

### Interfaces web pour Hadoop¶
Hadoop offre plusieurs interfaces web pour pouvoir observer le comportement de ses différentes composantes.
Allez dans votre navigateur et entrer les URLs suivants:
- `http://localhost:50070` permet d'afficher les informations de votre namenode (le master).
* Dans le menu cliquez sur: `Utilities > Browse the file system` pour voir les fichiers créés
- `http://localhost:8088` qui permet d'afficher les informations du resource manager de Yarn et visualiser le comportement des différents jobs.

