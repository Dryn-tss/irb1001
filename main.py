import cv2
import numpy as np
from simple_pid import PID
import time

from perception import ver, masks
from message import open_connection, close_connection, send_msg

from var import PATH_VID, VID, BT_PORT, SLEEP_TIME
from var import DEG_MARGIN, DIS_MARGIN_CENTER, DIS_MARGIN_BALL
from var import KP_ANGLE, KI_ANGLE, KD_ANGLE 
from var import KP_DIS, KI_DIS, KD_DIS 

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

def close():
    send_msg('00', 'Apagar')
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

def orient_to_ball(channel, info):
    pid = PID(KP_ANGLE, KI_ANGLE, KD_ANGLE, setpoint = 0)

    while abs(info['theta']) > DEG_MARGIN:
        vel = pid(info['theta'])
        send_msg(channel, str(vel), "orientation")

        info = act_info()
        if 'break' in info and info['break'] == True:
            break
    return info

def orient_to_img_center(channel, info):
    pid = PID(KP_ANGLE, KI_ANGLE, KD_ANGLE, setpoint = 0)

    while abs(info['theta_center']) > DEG_MARGIN:
        vel = pid(info['theta_center'])
        send_msg(channel, str(vel), "orientation")

        info = act_info()
        if 'break' in info and info['break'] == True:
            break
    
    return info

def orient_to_purple(channel, info):
    pid = PID(KP_ANGLE, KI_ANGLE, KD_ANGLE, setpoint = 0)

    while abs(info['theta_purple']) > DEG_MARGIN:
        vel = pid(info['theta_purple'])
        send_msg(channel, str(vel), "orientation")

        info = act_info()
        if 'break' in info and info['break'] == True:
            break
    return info

def orient_to_navy(channel, info):
    pid = PID(KP_ANGLE, KI_ANGLE, KD_ANGLE, setpoint = 0)

    while abs(info['theta_navy']) > DEG_MARGIN:
        vel = pid(info['theta_navy'])
        send_msg(channel, str(vel), "orientation")

        info = act_info()
        if 'break' in info and info['break'] == True:
            break
    return info

def move_to_img_center(channel, info):
    pid = PID(KP_DIS, KI_DIS, KD_DIS, setpoint = 0)

    while info['dis_center'] > DIS_MARGIN_CENTER:

        vel = pid(info['dis_center'])
        send_msg(channel, str(vel), "advance")

        info = act_info()
        if 'break' in info and info['break'] == True:
            break
    
    return info

def move_to_ball(channel, info):
    pid = PID(KP_DIS, KI_DIS, KD_DIS, setpoint = 0)

    while info['dis'] > DIS_MARGIN_BALL:
        info = orient_to_ball(channel, info)

        vel = pid(info['dis'])
        send_msg(channel, str(vel), "advance")

        info = act_info()
        if 'break' in info and info['break'] == True:
            break
    return info

def move_to_purple(channel, info):
    pid = PID(KP_DIS, KI_DIS, KD_DIS, setpoint = 0)

    while info['dis_purple'] > DIS_MARGIN_BALL:
        info = orient_to_purple(channel, info)

        vel = pid(info['dis_purple'])
        send_msg(channel, str(vel), "advance")

        info = act_info()
        if 'break' in info and info['break'] == True:
            break

    info = orient_to_img_center(channel, info)
    return info

def move_to_navy(channel, info):
    pid = PID(KP_DIS, KI_DIS, KD_DIS, setpoint = 0)

    while info['dis_navy'] > DIS_MARGIN_BALL:
        info = orient_to_navy(channel, info)

        vel = pid(info['dis_navy'])
        send_msg(channel, str(vel), "advance")

        info = act_info()
        if 'break' in info and info['break'] == True:
            break

    info = orient_to_img_center(channel, info)
    return info

def move_between_ball_goal(channel, info):
    while True:
        info = move_to_ball(channel, info)
        time.sleep(SLEEP_TIME)
        
        info = move_to_purple(channel, info)
        time.sleep(SLEEP_TIME)

        key = cv2.waitKey(25) & 0xFF
        if key == ord('x'):
            break

def main(ret, img, channel, move):
    img, img_masked, red_center, blue_center, yellow_center, goal = masks(ret, img)
    info = ver(img, img_masked, red_center, blue_center, yellow_center, goal)
    


    if move == '1':
        info = orient_to_ball(channel, info)
    elif move == '2':
        info = orient_to_img_center(channel, info)
    elif move == '3':
        info = move_to_img_center(channel, info)
    elif move == '0':
        print(info['dis_center'])





    # key = cv2.waitKey(25) & 0xFF

    # if key == ord('o'):  # Press 'o' to orient towards the ball
    #     info = orient_to_ball(channel, info)
    
    # elif key == ord('b'):
    #     info = move_to_ball(channel, info)

    # elif key == ord('c'):
    #     info = orient_to_img_center(channel, info)

    # elif key == ord('i'):  # Press 'c' to move to img_center
    #     info = move_to_img_center(channel, info)

    # elif key == ord('m'): 
    #     info = move_between_ball_goal(channel, info)

    # elif key == ord('q'):  # Press 'q' to exit
    #     close()

if __name__ == "__main__":

    channel, vid = setup()
    move = input('Ingrese movimiento:   ')


    while(True):
        vid.set(cv2.CAP_PROP_POS_FRAMES, 0)   # Reset the video capture to the start
        
        while vid.isOpened():
            ret, img = vid.read()
            if not ret:
                break
            

            
            main(ret, img, channel, move)


            
