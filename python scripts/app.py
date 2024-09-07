from flask import Flask, request, jsonify
import os
from constants import positions
from logicaAgentes import start
import shutil
from ultralytics import SAM
import cv2
import os

# Cargar modelo (y descargar en caso que no esté presente)
model = SAM("../vision_model/sam_b.pt")

app = Flask(__name__)

# Folder to save uploaded images
UPLOAD_FOLDER_startingViews = 'uploads'
if not os.path.exists(UPLOAD_FOLDER_startingViews):
    os.makedirs(UPLOAD_FOLDER_startingViews)

# Folder to save uploaded drone images
UPLOAD_FOLDER_droneViews = 'droneUploads'
if not os.path.exists(UPLOAD_FOLDER_droneViews):
    os.makedirs(UPLOAD_FOLDER_droneViews)
    
# Folder to save processed images
UPLOAD_FOLDER_processedImage= 'processedImages'
if not os.path.exists(UPLOAD_FOLDER_processedImage):
    os.makedirs(UPLOAD_FOLDER_processedImage)

#@app.route('/process_image', methods=['POST'])
def process_image():

    print("Procesando imagen...")
    for counter in range(0,10):
        print(f"Procesando imagen {counter}...")
        image_name = "DroneView_" + str(counter)+".png"
    #image_path = os.path.join('droneUploads\DroneView_' + str(counter) + '.png')
    #image_path = os.path.join('droneUploads\DroneView_0.png')
    #image_path = os.path.join('C:', os.sep, 'Users', 'esqui', 'Documents', 'Pyton', 'tec-2024B', 'assets', 'image1.png')
    #"C:\Users\esqui\Documents\GitHub\Evidencia-Agentes\Logicadeagentes\droneUploads"

    #MODIFICAR PATH DE ABAJO# 
        image_path = os.path.join('C:', os.sep, 'Users', 'jessi', 'Desktop', 'Source', 'E1. Actividad Integradora 1 - Monks',UPLOAD_FOLDER_droneViews, image_name)

        # Cargar la imagen
        #"C:\Users\esqui\Documents\GitHub\Evidencia-Agentes\Logicadeagentes\droneUploads\DroneView_0.png"
        
        if not os.path.exists(image_path):
            print(f"Error: La imagen {image_name} no existe en la ruta {image_path}.")
            break

        image = cv2.imread(image_path)

        # Verificar si la imagen se cargó correctamente
        if image is None:
            print("Error al cargar la imagen.")
        else:
            # Aplicar el modelo a la imagen con bounding boxes predefinidos
            results = model(image, bboxes=[100, 100, 1200, 800])

            # Obtenemos el frame con los objetos detectados y ya graficados con su bounding box y etiqueta
            annotated_image = results[0].plot()

            # Ruta de destino para guardar la imagen 
            #CAMBIAR RUTA PARA CARPETA DONDE SE QUIERE GUARDAR LAS IMAGENES. 
            #output_path = 'C:/Users/esqui/Documents/Pyton/tec-2024B/assets/results'

            processed_name = "ProcessedImage_" + str(counter)+".png"

            # Automaticamente descargar el resultado annotated_image
            cv2.imwrite(os.path.join(UPLOAD_FOLDER_processedImage, processed_name), annotated_image)
            print(f"Resultado guardado como annotated_image.png en {UPLOAD_FOLDER_processedImage}")

@app.route('/simulation_complete', methods=['POST'])
def simulation_complete():
    try:
        # Call your image processing function here
        print("Simulation completed. Starting image processing...")
        process_image()

        return jsonify({'status': 'success', 'message': 'Image processing started after simulation completion'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Route to receive the image from Unity (starting views)
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No image file found'}), 400
    
    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400
    
    save_path = os.path.join(UPLOAD_FOLDER_startingViews, image_file.filename)
    image_file.save(save_path)
    
    return jsonify({'status': 'success', 'message': f'Image saved at {save_path}'})

# Route to receive the drone image from Unity (drone views)
@app.route('/upload_drone_image', methods=['POST'])
def upload_drone_image():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No image file found'}), 400
    
    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400
    
    # Save the image with the filename provided by Unity
    save_path = os.path.join(UPLOAD_FOLDER_droneViews, image_file.filename)
    image_file.save(save_path)
    
    print(f"Drone image saved at: {save_path}")  # Log the save action
    
    return jsonify({'status': 'success', 'message': f'Drone image saved at {save_path}'})

# Route to clear the folders for starting views and drone images
@app.route('/clear_folders', methods=['POST'])
def clear_folders():
    try:
        # Clear the 'uploads' folder
        for filename in os.listdir(UPLOAD_FOLDER_startingViews):
            file_path = os.path.join(UPLOAD_FOLDER_startingViews, filename)
            os.remove(file_path)

        # Clear the 'droneUploads' folder
        for filename in os.listdir(UPLOAD_FOLDER_droneViews):
            file_path = os.path.join(UPLOAD_FOLDER_droneViews, filename)
            os.remove(file_path)

        return jsonify({'status': 'success', 'message': 'Folders cleared successfully'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

# Route to start the simulation and move objects
@app.route('/move', methods=['POST'])
def move_object():
    global positions
    start()
    return jsonify({'status': 'success'})

# Route to get the current position
@app.route('/move', methods=['GET'])
def get_position():
    if positions:
        return jsonify(positions.pop(0))
    else:
        return jsonify({'status': 'error', 'message': 'No positions available'}), 404

# Route to clear the positions
@app.route('/move', methods=['PUT'])
def delete_positions():
    global positions
    positions.clear()

    return jsonify({'status': 'success', 'message': 'Positions cleared'})

# Route to handle capture trigger (POST)
@app.route('/trigger_capture', methods=['GET', 'POST'])
def trigger_capture():
    if request.method == 'POST':
        data = request.get_json()
        if data and data.get('action') == 'capture':
            print("Capture trigger received via POST")
            return jsonify({'status': 'success'}), 200
    elif request.method == 'GET':
        print("Capture trigger received via GET")
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'failure', 'message': 'Invalid request'}), 400


if __name__ == '_main_':
    app.run(host='127.0.0.1', port=5000)