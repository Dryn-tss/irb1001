import cv2
import numpy as np
from simple_pid import PID
import time

from perception import ver, masks
from message import open_connection, close_connection, send_msg

PATH_VID = 'vid.mp4'
VID = False
BT_PORT = "/dev/tty.IRB-G01"
SLEEP_TIME = 1

DEG_MARGIN = 5    # Probamos con 5
DIS_MARGIN_CENTER = 90
DIS_MARGIN_BALL = 140

KP_ANGLE = 2.6      # Probamos con solo kp = 2.6
KI_ANGLE = 0.01  
KD_ANGLE = 0.00001

KP_DIS = 1.6      
KI_DIS = 0.1  
KD_DIS = 0.01

def setup():
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

    return (channel, vid)

def close(channel):
    send_msg(channel, '00', 'off')
    vid.release()
    cv2.destroyAllWindows()
    close_connection()
    exit()

def act_info():
    ret, img = vid.read()
    img, img_masked, red_center, blue_center, yellow_center, goal = masks(ret, img)
    info = ver(img, img_masked, red_center, blue_center, yellow_center, goal)
    if not ret:
        info['break'] = True
    return info

def orient_to_ball(channel, info, pid):
    vel = pid(info['theta'])
    send_msg(channel, str(2*vel), "orientation")

def move_to_img_ball(channel, info, pid):
    if info['dis_center'] > DIS_MARGIN_CENTER:
        vel = pid(info['dis_center'])
        send_msg(channel, str(vel / 5), "advance")

def main(ret, img, channel):
    img, img_masked, red_center, blue_center, yellow_center, goal = masks(ret, img)
    info = ver(img, img_masked, red_center, blue_center, yellow_center, goal)

    pid_theta = PID(KP_ANGLE, KI_ANGLE, KD_ANGLE, setpoint = 0)
    pid_dis = PID(KP_DIS, KI_DIS, KD_DIS, setpoint = 0)

    if info['dis'] > DIS_MARGIN_BALL:
        if abs(info['theta']) > DEG_MARGIN:
            orient_to_ball(channel, info, pid_theta)
            print('orienting')
        else:
            move_to_img_ball(channel, info, pid_dis)

    key = cv2.waitKey(25) & 0xFF
    if key == ord('q'):  # Press 'q' to exit
        close(channel)

if __name__ == "__main__":

    channel, vid = setup()

    while(True):
        vid.set(cv2.CAP_PROP_POS_FRAMES, 0)   # Reset the video capture to the start
        
        while vid.isOpened():
            ret, img = vid.read()
            if not ret:
                break
            
            main(ret, img, channel)

