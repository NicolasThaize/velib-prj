# DOCS

## Which window is used in spark structured streaming data processing ?
We used a 1 hour window which updates every 5 minutes to provide a sufficent overview of Velib's usage in Paris area.

## How did we defined station clusters ?
Firstly, we have taken station geographical positions on the following source: https://opendata.paris.fr/explore/dataset/velib-emplacement-des-stations/export/

Secondly, In order to make metrics with grouped stations, we clusterized with machine learning the stations according to their longitude and latitude coordinates.
<br>To do so we used the K-Means algorithm with Scikit-Learn to automatically define 74 clusters of velib stations. Why 74 ? Velib's are implemented in the 20 Paris districts and in 55 diffrent cities.
A notebook which relates this simple research is available in the ./notebooks/ folder.