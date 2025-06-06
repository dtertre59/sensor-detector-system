# READ VIDEO

import cv2

# Ruta del archivo .avi
archivo_mp4 = 'data/videos/samples/full_video_tspeed2_1.mp4'

cap = cv2.VideoCapture(archivo_mp4)

# Verificar si se abrió correctamente
if not cap.isOpened():
    print("Error al abrir el archivo de video.")
    exit()

# Settings
frame_c = 0
flag = False

counter = 0

while True:
    # Leer un cuadro del video
    ret, frame = cap.read()

    # Capture
    if flag:
        cv2.imwrite(str('data/images/background/background_0.png'), frame)
        flag = False
    
    # Si no se puede leer un cuadro, terminamos
    if not ret:
        print("Fin del video.")
        break

    # Mostrar el cuadro
    cv2.imshow('Video', frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    key = input(frame_c)

    if key == 's':
        print(f'Saving frame {counter}...')
        cv2.imwrite(str(f'data/images/samples/sequence/sequence_sample_1/sample_{counter}.png'), frame)
        counter += 1

    frame_c += 1
    if key == 'q':
        break

# Liberar el objeto de captura y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()