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
pid = PID(2.6,0,0, setpoint = 0)



def enviar(vel:str):
	msg = vel
	msg_e = str.encode(msg)
	ser.write(msg_e)

ser = serial.Serial("COM3",baudrate = 38400,timeout = 1)
time.sleep(5)

# Open the video file 
vid = cv2.VideoCapture("vid.mp4")

while(True):
	ret, img = vid.read()

	dis, theta = ver(ret, img)
	print(f"distancia: {dis:3f}, angulo: {theta:3f}")
	pid(theta)
	pid(dis)

	if dis > 30:
		vel = 0
		pass
	
	enviar(str(0))
	
	# Press 'q' to exit the loop
	if cv2.waitKey(25) & 0xFF == ord('q'):
		vid.release()
		cv2.destroyAllWindows()
		ser.close()
		exit()

	