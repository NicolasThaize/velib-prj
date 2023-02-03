# Informations générales app Kafka

1. Url pour récupérer les données d’une station velib en particulier : 
https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&lang=fr&rows=9999&sort=duedate&facet=stationcode&refine.stationcode=25005 <= ex récupère les données des velibs pour la station no 25005

2.	Dans l'énoncé: "Faire une fonction get_velib_data(nrows) qui permet de récupérer nrows lignes de données."<br>
<span style="color:lightblue">=> étant donné qu'au retour de l'api il n’y a qu’une seule ligne pour chaque station, cela revient à dire que nrows = nstations ? </span>
<span style="color:red"></br>A priori oui, car dans un export plat de l’api (sans filtre) le nombre de lignes est égal au nombre de stations : attention, certaines stations n’ont pas remontées de données depuis un certain temps ou ne sont pas complètement à jour (quelques minutes / heures de retard). </br>
En filtrant par « OUI » sur la colonne « Station en fonctionnement », une bonne partie des stations ne remontant pas de données disparaissent.</span>
