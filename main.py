import cv2
import numpy as np
from simple_pid import PID
import time

from perception import ver, masks
from message import open_connection, close_connection, send_msg

PATH_VID = 'vid.mp4'
BT_PORT = "/dev/tty.IRB-G01"
VID = False


def setup():
    pid = PID(2.6, 0, 0, setpoint = 0)
    channel = open_connection(BT_PORT)
    
    if VID:
        # Open the video file 
        vid = cv2.VideoCapture(PATH_VID)  
    else:
        vid = cv2.VideoCapture(0)
            
        if not vid.isOpened():
            vid = cv2.VideoCapture(1)

    if not vid.isOpened():
        print("Error: Could not open video or camera.")
        exit()

    return (pid, channel, vid)

def close():
    vid.release()
    cv2.destroyAllWindows()
    close_connection()
    exit()

def orient_to_ball(pid, channel, theta):
    while abs(info['theta']) > 5:
        vel = pid(info['theta'])
        send_msg(channel, str(vel), "orientation")


        ret, img = vid.read()
        if not ret:
            break
        info = ver(ret, img)
    
    return info

def move_to_img_center():
    pass



def main():
    img, img_masked, red_center, blue_center, yellow_center = masks(ret, img)
    info = ver(img, img_masked, red_center, blue_center, yellow_center)


    if abs(info['theta']) > 5:
        vel = pid(info['theta'])
        send_msg(channel, str(vel), "orientation")






    if cv2.waitKey(25) & 0xFF == ord('o'):  # Press 'o' to orient towards the ball 
        info = orient_to_ball(pid, channel, info['theta'])

    if cv2.waitKey(25) & 0xFF == ord('c'):  # Press 'c' to move to img_center 
        info = move_to_img_center()
            
    if cv2.waitKey(25) & 0xFF == ord('q'):  # Press 'q' to exit 
        close()

if __name__ == "__main__":

    pid, channel, vid = setup()

    while(True):
        vid.set(cv2.CAP_PROP_POS_FRAMES, 0)   # Reset the video capture to the start
        
        while vid.isOpened():
            ret, img = vid.read()
            if not ret:
                break
            
            main()



            
