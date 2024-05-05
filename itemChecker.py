import os
import json


# Ruta de la carpeta que contiene los archivos JSON
ruta_carpeta = "json"
objeto = 'Demol Earring +3'


# Lista para almacenar los precios de los objetos "Peision Necklace"
precios_peision_necklace = []
# Contador para almacenar el número de objetos "Peision Necklace"
contador_peision_necklace = 0

# Iterar sobre los archivos en la carpeta
for nombre_archivo in os.listdir(ruta_carpeta):
    # Comprobar si el archivo es un archivo JSON
    if nombre_archivo.endswith('.json'):
        # Construir la ruta completa al archivo
        ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
        # Leer y cargar los datos del archivo JSON
        with open(ruta_completa, 'r') as archivo:
            datos = json.load(archivo)
            # Buscar objetos "Peision Necklace" y agregar sus precios a la lista
            for item in datos:
                if item['name'] == objeto:
                    precios_peision_necklace.append(int(item['price']))
                    # Incrementar el contador
                    contador_peision_necklace += 1

# Calcular el promedio de los precios de los objetos "Peision Necklace"
if precios_peision_necklace:
    promedio_precios = sum(precios_peision_necklace) / len(precios_peision_necklace)
    print("El promedio del precio de los objetos "+ objeto + " es:", promedio_precios)
    print("Se encontraron", contador_peision_necklace)
else:
    print("No se encontraron objetos.")