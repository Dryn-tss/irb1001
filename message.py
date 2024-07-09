import serial
import time


def open_connection(port:str="COM5"):
	channel = serial.Serial(port, baudrate=38400, timeout=1)
	time.sleep(5)
	return channel

def close_connection(channel):
	channel.close()

def send_msg(channel, vel:str, mode:str, print_msg=True):
	vel = str(round(float(vel)))
	if mode == "orientation":
		msg = "O" + vel
	elif mode == "advance":
		msg = "A" + '-' + vel
	else:
		msg = "F" + "0"	

	if print_msg:
		print(f"Sending msg:	{msg}")

	msg_e = str.encode(msg)
	channel.write(msg_e)
	time.sleep(0.05)

