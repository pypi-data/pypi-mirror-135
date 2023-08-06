# MODELOS DE ATRIBUCION
Acá va un texto explicando qué es.

## INSTALACIÓN
```
pip install atribucion
```
## CÓMO SE USA
Primero creas el modelo y le pasas la data.
```
modelo = atribucion.Modelo(data)
```
Después pedís que te calcule el modelo que quieras.
````
resultado_markov = modelo.markov()
resultado_shapley = modelo.shapley()
````
