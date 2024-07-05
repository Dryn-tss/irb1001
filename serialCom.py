import cv2
import time
import serial

cv2.namedWindow('frame')

msgOn = "A100;" # Mensaje que queremos enviar para prender el LED del Arduino
msgOff = "A0;" # Mensaje que queremos enviar para apagar el LED del Arduino
# El Ambos mensajes que estan en formato Sring deben ser transformados en un arreglo de bytes mediante la funcion .encode
msgOnEncode = str.encode(msgOn) 
msgOffEncode = str.encode(msgOff)

# seria.Serial nos permite abrir el puerto COM deseado	
ser = serial.Serial("/dev/tty.IRB-G01",baudrate = 38400,timeout = 1)
# Cuando se abre el puerto serial con el Arduino, este siempre se reinicia por lo que hay que esperar a que inicie para enviar los mensajes
time.sleep(5)

while(True):
	# .write nos permite enviar el arreglo de bytes correspondientes a los mensajes
	ser.write(msgOnEncode)
	time.sleep(5)
	ser.write(msgOffEncode)
	time.sleep(5)
	
	# Terminamos el codigo con la tecla ESC
	if cv2.waitKey(10) & 0xFF == 27:
		break
	
# Cerramos el puerto serial abierto una vez terminado el codigo
ser.close()
