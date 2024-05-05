from PIL import Image
import pytesseract
import re
import json
import os
import pyautogui
from datetime import datetime

def clean_text(text):
    # Eliminar letras solas y dos letras solas
    text = re.sub(r'\b[a-zA-Z]{1,2}\b', '', text)
    # Eliminar apóstrofes
    text = text.replace("‘", "")
    text = text.replace('\\', "")
    text = text.replace('\"', "")
    text = text.replace("/", "")
    text = text.replace(",", "")
    text = text.replace("-", "")
    text = text.replace("»", "")
    text = text.replace("@", "")
    text = text.replace("&", "")
    # Eliminar espacios al inicio de cada línea
    text = re.sub(r'(?m)^\s+', '', text)
    # Reemplazar múltiples espacios por uno solo, manteniendo los saltos de línea
    text = re.sub(r'[ ]{2,}', ' ', text)
    return text.strip()

def parse_items_to_json(text):
    import re
    lines = text.strip().split('\n')
    items = []
    current_item = {'name': '', 'price': ''}  # Inicia con un objeto vacío

    for line in lines:
        # Checar si la línea contiene un precio, asumiendo que el precio siempre tiene comas o solo números
        if re.search(r'\d{2,},\d{3}', line) or re.search(r'\d{5,}', line):
            if current_item['name']:  # Solo añadir el precio si ya hay un nombre
                current_item['price'] = line.strip()
                items.append(current_item)
                current_item = {'name': '', 'price': ''}  # Reiniciar para el próximo objeto
        else:
            # Si no es un precio, debe ser un nombre de objeto
            if current_item['name']:  # Si ya hay un nombre sin precio, añadir al listado
                items.append(current_item)
            current_item = {'name': line.strip(), 'price': ''}  # Comenzar nuevo objeto con nombre actual
    
    # Añadir el último item si no se añadió previamente
    if current_item['name']:
        items.append(current_item)

    return items

def save_json(data, filename):
    # Obtener la fecha y hora actual
    current_datetime = datetime.now()
    # Crear la carpeta si no existe
    os.makedirs('json', exist_ok=True)
    # Formatear la fecha y hora actual como parte del nombre del archivo JSON
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    # Escribir los datos en un archivo JSON
    with open(f'json/{filename}_{formatted_datetime}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Definir la ubicación de Tesseract-OCR en tu sistema
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Solo necesario en Windows

# Tamaño deseado para la captura de pantalla
width, height = 800, 600

# Ubicación de la imagen que quieres cargar
image_path = 'img/Captura9.jpg'

# Ubicación donde deseas guardar la captura de pantalla
#screenshot_path = 'screenshots/screenshot.png'

# Captura la pantalla en las coordenadas especificadas y la guarda en la ubicación deseada
#screenshot = pyautogui.screenshot(region=(60, 175, 300, 800))
#screenshot.save(screenshot_path)

img = Image.open('img/Captura.jpg')

# Usar pytesseract para extraer texto
text = pytesseract.image_to_string(img)

# Limpieza y análisis del texto
cleaned_text = clean_text(text)
parsed_data = parse_items_to_json(cleaned_text)

# Guardar el resultado en un archivo JSON
save_json(parsed_data, 'items')
os.remove('img/Captura.jpg')


