# index-solr-cores-pipeline

## Descripción

Este repositorio contiene los scripts necesarios para indexar las imagenes de las entregas de las fototrampas en los cores de solr necesarios para el cliente de anotación. 

## Preparación

Se espera que el archivo del modelo esté en un directorio `model` dentro de este repositorio.

## Pasos

1. `megad.py`: Corre el modelo megadetector sobre el directorio de las imagenes a indexar. Se ejecuta dentro del contenedor con el comando `python megad.py`.
2. `sipecam_anotaciones_cor.py`: Indexa en la instancia de Solr las inferencias obtenidas de megadetector en el core de anotaciones y las imagenes en la aplicación de sipecam.

## Variables de ambiente

El script `sipecam_anotaciones_cor.py` lee de un archivo que se llama `.env` las siguientes variables de ambiente

  - POSTGRES_DB
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - POSTGRES_HOST
  - POSTGRES_PORT
  - MGDT_OUTPUT
  - THRESHOLD_SCORE=10
  - SOLR_URL

## Dockerfile

Para correr estos scripts en el contenedor de docker, se deben seguir los siguientes pasos:

Countruir la imagen con lo necesario para correr los scripts usando el siguiente comando

```shell
    docker build -t megadetector-solr:1.0 .
```

Verificar que se construyó correctamente la imagen con el comando

``` shell
  docker images
```

Ejecutar el contenedor especificando el path a las imagenes, el path al archivo de salidas y el path del modelo con el siguiente comando

``` shell
  docker run -it -v /path/to/images/:/images/ -v /path/to/output.json/:/output.json -v /path/to/model.pt:/model/model.pt megadetector-solr:1.0 bash
```

Seguir los pasos.