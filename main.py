import cv2
import numpy as np
from simple_pid import PID

from perception import ver
from message import open_connection, close_connection, send_msg

PATH_VID = 'vid.mp4'
VID = False


def setup():
    pid = PID(2.6, 0, 0, setpoint = 0)
    channel = open_connection()
    
    if VID:
        # Open the video file 
        vid = cv2.VideoCapture(PATH_VID)  
    else:
        vid = cv2.VideoCapture(1)
            
        if not vid.isOpened():
            vid = cv2.VideoCapture(0)

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
    while np.abs(theta) > 5:
        vel = pid(theta)
        send_msg(channel, str(vel), "orientation")


        ret, img = vid.read()
        if not ret:
            break
        dis, theta, robot_center, img_center = ver(ret, img)
    
    return (dis, theta, robot_center, img_center)

def move_to_img_center():
    pass


    

if __name__ == "__main__":

    pid, channel, vid = setup()

    while(True):
        vid.set(cv2.CAP_PROP_POS_FRAMES, 0)   # Reset the video capture to the start
        
        while vid.isOpened():
            ret, img = vid.read()
            if not ret:
                break
            dis, theta, robot_center, img_center = ver(ret, img)
            # print(f"distancia: {dis:3f}, angulo: {theta:3f}")

            if cv2.waitKey(25) & 0xFF == ord('o'):  # Press 'o' to orient towards the ball 
                dis, theta, robot_center, img_center = orient_to_ball(theta)

            if cv2.waitKey(25) & 0xFF == ord('c'):  # Press 'c' to move to img_center 
                dis, theta, robot_center, img_center = move_to_img_center()
            

            if cv2.waitKey(25) & 0xFF == ord('q'):  # Press 'q' to exit 
                close()





            if np.Abs(theta) < 5 and dis > 30:
                vel = pid(dis)
                send_msg(channel, str(vel), "advance")
            
            elif np.Abs(theta) < 5 and dis < 30:
                vel = 0
                send_msg(channel, str(vel), "stop")


            
