# hadoop-cluster

Ce projet consiste à construire un cluster Hadoop avec des conteneurs Docker.
Une fois le cluster créé, nous installons un ensemble d'outils de l'écosystème hadoop à savoir Spark, Sqoop, Hbase, Storm, … Puis les mettrons en œuvre via des mini projets de data science.



## Preparation de l’environments
Pour déployer le framework Hadoop, nous allons utiliser des contenaires Docker. 

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

Créer une liste de dossier qui seront utile pour le dérouler du projet.
```
mkdir mahout mapreduce
```


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


## Hadoop MapReduce

Un Job Map-Reduce se compose principalement de deux types de programmes:

- **Mappers** : permettent d’extraire les données nécessaires sous forme de clef/valeur, pour pouvoir ensuite les trier selon la clef

- **Reducers** : prennent un ensemble de données triées selon leur clef, et effectuent le traitement nécessaire sur ces données (somme, moyenne, total...)


### Wordcount
Nous allons tester un programme MapReduce grâce à un exemple très simple, le WordCount, l'équivalent du HelloWorld pour les applications de traitement de données. Le Wordcount permet de calculer le nombre de mots dans un fichier donné, en décomposant le calcul en deux étapes:

- L'étape de Mapping, qui permet de découper le texte en mots et de délivrer en sortie un flux textuel, où chaque ligne contient le mot trouvé, suivi de la valeur 1 (pour dire que le mot a été trouvé une fois).<br>
L'implémentation python du mapping se trouve dans le dossier `mapreduce/mapper.py`
- L'étape de Reducing, qui permet de faire la somme des 1 pour chaque mot, pour trouver le nombre total d'occurrences de ce mot dans le texte.


- Copie du mapper et du reducer dans le master

Ouvrez un terminal à la racine du projet et entrer la commande suivante. 
```
docker cp mapreduce/* master:/root/mapreduce
```

Ensuite entrer dans le master.
```
docker exec -it master bash
cd mapreduce
```

- Execution du map

```
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
-file /root/mapreduce/mapper.py -mapper mapper.py \
-file /root/mapreduce/reducer.py -reducer reducer.py \
-input /user/root/input/purchases.txt \
-output /user/root/output \
-verbose
```

- Execution du reduce 

```
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
-mapper /root/mapreduce/mapper.py \
-reducer /root/mapreduce/reducer.py \
-input /user/root/input/purchases.txt \
-output /user/root/output
```

Le résultat du map et du reduce se trouve dans le `dossier` output dans hdsf.


## Hadoop & Mahout

### installation

Pour l'installation vous exécuterez les commandes ci-dessous dans le master.

- Téléchargement et installation
```
wget http://archive.apache.org/dist/mahout/0.13.0/apache-mahout-distribution-0.13.0.tar.gz &&\
    tar -zxvf apache-mahout-distribution-0.13.0.tar.gz &&\
    mv apache-mahout-distribution-0.13.0 /usr/local/mahout &&\
    rm apache-mahout-distribution-0.13.0.tar.gz
```

- Configurations utiles 
```
export MAHOUT_HOME=/usr/local/mahout
CLASSPATH=$CLASSPATH:/usr/local/mahout
PATH=$PATH:/usr/local/mahout/bin
```

### Régression logistique avec mahout

- Téléchargement des données `iris.csv` dans le master.

Copie des données dans le master.
Pour cela allez dans le dossier `mahout/` situé à la racine du projet.
Puis exécuter la commande suivante.

```
docker cp iris.csv master:/root/
```

Ensuite entrer dans le master.


- Entrainement

```
 mahout trainlogistic \
 --input iris.csv \
 --output logit_model \
 --target target \
 --categories 2 \
 --predictors sepal.length sepal.width petal.length petal.width \
 --types numeric numeric numeric numeric \
 --features 4 --passes 100 --rate 0.1 --lambda 0.0001

```

- Évaluation

```
mahout runlogistic \
--input iris.csv \
--model logit_model \
--scores --auc --confusion > iris_eval_result.txt
```

### Classification de texte avec mahout (mode cluster)

Entrer dans le master.

```
mkdir 20news
cd 20news
wget http://people.csail.mit.edu/jrennie/20Newsgroups/20news-bydate.tar.gz
tar xzvf 20news-bydate.tar.gz
rm 20news-bydate.tar.gz
```

- Préparation des données 

Chargement des données dans hdfs dans le dossier `20news`.

```
hdfs dfs -put 20news-bydate-test 20news
```

Transformation des données textuelles en données numériques basée sur la matricielle TF-IDF. 

```
mahout seqdirectory -i 20news -o 20newsdataseq

mahout seq2sparse \
    -i 20newsdataseq/part-m-00000 \
    -o 20newsdataVec \
    -lnorm -nv -wt tfidf
```

- Création des données d'entraînement et de test

```
mahout split \
  -i 20newsdataVec/tfidf-vectors \
  --trainingOutput 20newsdataVecTrain \
  --testOutput 20newsdataVecTest \
  --randomSelectionPct 20 \
  --overwrite \
  --sequenceFiles -xm sequential
```

- Entrainement

```
mahout trainnb \
  -i 20newsdataVecTrain \
  -o nb_model \
  -li labelindex -ow -c 
```

- Évaluation

```
mahout testnb \
  -i 20newsdataVecTest\
  -m nb_model \
  -l labelindex -ow -o mahout_nb_results
```

Le résultat de l’évaluation se trouve dans le système de fichier hdfs. Nous allons le télécharger dans le système de fichier de Ubuntu pour pouvoir le consulter. 

```
hdfs dfs -get mahout_nb_results
```

Pour copier le fichier sur notre machine local, tapez la commande ci-dessous dans votre terminal local.  

```
docker cp master:/root/20news/mahout_nb_results mahout_nb_results
```
