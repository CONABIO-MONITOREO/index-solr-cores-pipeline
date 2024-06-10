# index-solr-cores-pipeline

# Descripción

Este repositorio contiene los scripts necesarios para indexar las imagenes de las entregas de las fototrampas en los cores de solr necesarios para el cliente de anotación. 

## Pasos

1. `megad.py`: Corre el modelo megadetector sobre el directorio de las imagenes a indexar. Recibe como parametros
 - Path del directorio de las imagenes.
 - Path del archivo de salidas.
 - Path del archivo del modelo de megadetector.