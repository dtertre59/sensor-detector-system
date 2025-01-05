# READ VIDEO

import cv2

# Ruta del archivo .avi
archivo_mp4 = 'data/videos/samples/video_brass_3.mp4'

cap = cv2.VideoCapture(archivo_mp4)

# Verificar si se abrió correctamente
if not cap.isOpened():
    print("Error al abrir el archivo de video.")
    exit()

while True:
    # Leer un cuadro del video
    ret, frame = cap.read()
    
    # Si no se puede leer un cuadro, terminamos
    if not ret:
        print("Fin del video.")
        break

    # Mostrar el cuadro
    cv2.imshow('Video', frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    input('a')

# Liberar el objeto de captura y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()