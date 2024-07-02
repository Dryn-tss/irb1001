import cv2
import time
import serial
from percepcion import ver
from simple_pid import PID

cv2.namedWindow('frame')
msgOn = "A100;" # velocidad
msgOff = "A0;" 
msg_Or_right = "A100;" 
msg_Or_left = "A0;" 
msgOnEncode = str.encode(msgOn) 
msgOffEncode = str.encode(msgOff)
msgOr_rightEncode = str.encode(msg_Or_right)
msg_Or_leftEncode = str.encode(msg_Or_left)

#hay que redefinir las variables para el robot 
pid = PID(2.6,0,0, setpoint = 0)

def enviar(ser, vel:str, modo):
	if modo == "orientacion":
		msg = "O" + vel
	if modo == "avance":
		msg = "A" + vel
	else: 
		msg = "F" + '0'
	msg_e = str.encode(msg)
	ser.write(msg_e)

ser = serial.Serial("/dev/tty.IRB-G01",baudrate = 38400,timeout = 1)
time.sleep(5)

# Open the video file 
vid = cv2.VideoCapture("vid.mp4")

while(True):
	ret, img = vid.read()

	dis, theta = ver(ret, img)
	print(f"distancia: {dis:3f}, angulo: {theta:3f}")
	pid(dis)

	if theta > 5:
		vel = pid(theta)
		enviar(ser, str(vel), "orientacion")

	if theta < 5 and dis > 30:
		vel = pid(dis)
		enviar(ser, str(vel), "avance")
	
	elif theta < 5 and dis < 30:
		vel = 0
		enviar(ser, str(vel), "parar")
	
	# Press 'q' to exit the loop
	if cv2.waitKey(25) & 0xFF == ord('q'):
		vid.release()
		cv2.destroyAllWindows()
		ser.close()
		exit()