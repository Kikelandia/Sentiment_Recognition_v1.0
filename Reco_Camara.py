#Librerias necesarias
'''
Python version > 3.XX
Conda installed with path variables activated (miniconda can be installed too)
For the correct execution of the script create a new environment
install openCV using:
    conda install -c conda-forge opencv
install scikit learn with the version 0.22.1 to prevent any waring or malfunction
scikit=0.22.1
numpy could be any version however the one -i used was
    numpy=1.18.1
'''
import cv2
import numpy as np
import pickle

#XML para reconocimiento de rostros
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#Archivo del modelo de reconocimiento de emociones
#filename = 'modelo_Reco_Facial_LogReg.sav'
filename = 'modelo_Reco_Facial_LogReg_Over.sav'

#Instancia del Modelo
loaded_model = pickle.load(open(filename, 'rb'))
#Contador de Fotogramas
count = 0
#Lista con la emoción respectiva a cada rostro en la imagen (Hasta 10)
emotions = [''] * 10
#Se activa la cámara con OpenCV
cap = cv2.VideoCapture(0)

#fourcc = cv2.VideoWriter_fourcc(*'MJPG')

#out = cv2.VideoWriter('output.avi', fourcc, 15.0, (640,480))

while True:
    #Función read() retorna boolean e imagen como np.array()
    ret, img = cap.read()
    #La imagen es convertida a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #Se detectan las caras en la imagen
    faces = face_cascade.detectMultiScale(gray,1.3,5)

    #Recorrido y enumeración de cada uno de los rostros en la imagen
    #tambien son retornadas las coordenadas de cada cara
    for idx, (x,y,w,h) in enumerate(faces):
        #Se imprime en la imagen un rectangulo delimitando el rostro que fue encontrado
        cv2.rectangle(img, (x,y), (x+w,y+h),(255,0,0),2)
        #Se aisla el rostro en la imagen en escala de grises para trabajar con él
        roi_gray = gray[y:y+h,x:x+w]
        #Dimensiones que escalar el rostro a evaluar
        dim = (48,48)
        #Redimensión y "aplanamiento" de la np.array()  (matriz(48,48)->vector(2304))
        res = cv2.resize(roi_gray,dim).flatten()
        #Tipo de fuente para mostrar la emoción en pantalla
        font = cv2.FONT_HERSHEY_SIMPLEX
        #Para aligerar la carga en el procesador se evalua la emoción cada 10 fotogramas
        if count%10==0:
            #Con el vector de 2304 dimensiones se realiza la predicción con la instancia del modelo
            emotions[idx] = loaded_model.predict([res])[0]
        #Se imprime en la imagen original la emoción correspondiente para cada rostro
        cv2.putText(img,emotions[idx],(x, y+h),font, 1,(0, 255, 255),2,cv2.LINE_4)
    #Imagen resultante, incluyendo el rectangulo que delimita al rostro y la emoción predicha
    cv2.imshow('Prediccion Tiempo Real',img)
    #Contador de fotogramas incrementa en 1
    count +=1
    #out.write(img)
    #se registra la tecla ESC para finalizar el programa
    k = cv2.waitKey(30 & 0xff)
    if k == 27:
        break
#Liberación de la camara y recursos usados
cap.release()
#out.release()
cv2.destroyAllWindows()
