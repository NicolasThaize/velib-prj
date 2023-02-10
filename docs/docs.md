# DOCS

## How did we defined station clusters ?
In order to make metrics with grouped stations, we clusterized with machine learning the stations according to their longitude and latitude coordinates.

To do so we used the K-Means algorithm with Scikit-Learn to automatically define 74 clusters of velib stations. Why 74 ? Velib's are implemented in the 20 Paris districts and in 55 diffrent cities.
A notebook which relates this simple research is available in the ./notebooks/ folder.