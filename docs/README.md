# Q/A about the application functioning

## Where does the processed streaming data land?
The data processed by Spark Structured Streaming is sinked into a MongoDB database with a collection for each data processing (grouped stations and single stations).

## Which window is used in spark structured streaming data processing?
We used a 1 hour window which updates every 5 minutes to provide a sufficent overview of Velib's usage in Paris area.

## How did we defined station clusters?
Firstly, we have taken station geographical positions on the following source: https://opendata.paris.fr/explore/dataset/velib-emplacement-des-stations/

Secondly, In order to make metrics with grouped stations, we clusterized with machine learning the stations according to their longitude and latitude coordinates.
<br>To do so we used the K-Means algorithm with Scikit-Learn to automatically define 74 clusters of velib stations. Why 74 ? Velib's are implemented in the 20 Paris districts and in 55 diffrent cities.
A notebook which relates this simple research is available in the ./notebooks/ folder.

## Why using Big Data tools for such a project?

Obviously Big Data tools are not required for this volume of data, however the main goal of this application is to show how data can be manipulated in a Big Data context the simplest way.