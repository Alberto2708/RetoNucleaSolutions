from ultralytics import SAM
import cv2
import os

# Cargar modelo (y descargar en caso que no esté presente)
model = SAM("../vision_model/sam_b.pt")

#app = Flask(__name__)

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
        image_path = os.path.join('C:', os.sep, 'Users', 'jessi', 'Desktop', 'E1. Actividad Integradora 1 - Monks', 'Source',UPLOAD_FOLDER_droneViews, image_name)

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

process_image()