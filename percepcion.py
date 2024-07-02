import cv2 
import numpy as np
# from PIL import Image

# VARIABLES
PATH = 'vid.mp4'
FONT = cv2.FONT_HERSHEY_SIMPLEX

# Colors
GREEN = (0, 200, 0)
RED = (0, 0, 200)
BLUE = (200, 0, 0)
YELLOW = (0, 200, 200)
PURPLE = (200, 0, 200)
NAVY = (180,50,100)

# Range of the colors in HSV
LOW_GREEN = np.array([40, 100, 100])
HIGH_GREEN = np.array([80, 255, 255])

LOW_RED = np.array([0, 100, 100])
HIGH_RED = np.array([10, 255, 255])

LOW_BLUE = np.array([100, 100, 100])
HIGH_BLUE = np.array([108, 255, 255])

LOW_YELLOW = np.array([20, 100, 100])
HIGH_YELLOW = np.array([30, 255, 255])

#Colores para los arcos, falta modificar los rangos, aunque no estoy segura que esta sea la mejor manera de hacer lo de los arcos

LOW_PURPLE = np.array([120, 100, 100])
HIGH_PURPLE = np.array([160, 255, 255])

LOW_NAVY = np.array([60, 100, 100])
HIGH_NAVY = np.array([70, 255, 255])

# Aux. functions
def draw_box(img, img_masked, contours, color, text):
    """
    Draw the bounding box of the biggest contour,
    on the original img and the masked img
    """
    if contours:
        # Find the largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)
        # Get the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)
        # Draw the bounding box
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.rectangle(img_masked, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, text, (x, y - 5), FONT, 0.5, color, 1, cv2.LINE_AA)
        cv2.putText(img_masked, text, (x, y - 5), FONT, 0.5, color, 1, cv2.LINE_AA)

        # Returns the center of the box
        center = (int(x + w / 2), int(y + h / 2))
        return center
    return False

def distance(center_one, center_two):
    """
    Returns the distance between the 2 centers in pixels.
    """
    x = abs(center_one[0] - center_two[0])
    y = abs(center_one[1] - center_two[1])
    dis = (x ** 2 + y ** 2) ** (1 / 2)
    # print(f"x:  {x},   y:  {y},   dis:  {dis}")
    return round(dis, 2)

def angle(center_one, center_two, center_three, deg = False):
    """
    Returns the angle between the line from center_one to center_two
    and the line from center_one to center_three.
    """
    A = np.array([center_one[0], center_one[1]])
    B = np.array([center_two[0], center_two[1]])
    C = np.array([center_three[0], center_three[1]])

    AB = B - A
    AC = C - A

    # AB dot AC = Cos(theta) * |AB| * |AC|       
    dot_product = np.dot(AB, AC)
    magnitude_AB = np.linalg.norm(AB)
    magnitude_AC = np.linalg.norm(AC)

    cos_theta = dot_product / (magnitude_AB * magnitude_AC)
    theta = np.arccos(cos_theta)
    
    if deg:
        theta_degrees = np.degrees(theta)
        return round(theta_degrees, 2)
    return round(theta, 2)


# Open the video file 
vid = cv2.VideoCapture(PATH)

if not vid.isOpened():
    print("Error: Could not open video.")
    exit()

def ver(ret, img):

    # Flip image and Convert the frame from BGR to HSV
    img = cv2.flip(img, -1)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Create masks for the colors
    green_mask = cv2.inRange(img_hsv, LOW_GREEN, HIGH_GREEN)
    red_mask = cv2.inRange(img_hsv, LOW_RED, HIGH_RED)
    blue_mask = cv2.inRange(img_hsv, LOW_BLUE, HIGH_BLUE)
    yellow_mask = cv2.inRange(img_hsv, LOW_YELLOW, HIGH_YELLOW)
    purple_mask = cv2.inRange(img_hsv, LOW_PURPLE, HIGH_PURPLE)
    navy_mask = cv2.inRange(img_hsv, LOW_NAVY, HIGH_NAVY)


    # Apply the masks to the frame on img_masked
    img_masked_red = cv2.bitwise_and(img, img, mask=red_mask)
    img_masked_blue = cv2.bitwise_and(img, img, mask=blue_mask)
    img_masked_yellow = cv2.bitwise_and(img, img, mask=yellow_mask)
    img_masked_purple = cv2.bitwise_and(img, img, mask=purple_mask)
    img_masked_navy = cv2.bitwise_and(img, img, mask=navy_mask)

    img_masked = cv2.bitwise_or(img_masked_red, img_masked_blue)
    img_masked = cv2.bitwise_or(img_masked, img_masked_yellow)
    #img_masked = cv2.bitwise_or(img_masked, img_masked_purple)
    #img_masked = cv2.bitwise_or(img_masked, img_masked_navy)


    # For each mask find contours and draw the boxes 
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_center = draw_box(img, img_masked, contours, RED, "R")

    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_center = draw_box(img, img_masked, contours, BLUE, "B")

    contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    yellow_center = draw_box(img, img_masked, contours, YELLOW, "Y")

    #contours, _ = cv2.findContours(purple_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #purple_center = draw_box(img, img_masked, contours, PURPLE, "P")

    #contours, _ = cv2.findContours(navy_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #navy_center = draw_box(img, img_masked, contours, NAVY, "N")

    # If it detects the circles, make the lines and labels
    if red_center != False and blue_center != False:
        end_x = red_center[0] + ((blue_center[0] - red_center[0]) * 10)
        end_y = red_center[1] + ((blue_center[1] - red_center[1]) * 10)
        end_point = (end_x, end_y)
            
        cv2.line(img, red_center, end_point, BLUE, thickness=1)
        cv2.line(img_masked, red_center, end_point, BLUE, thickness=1)

    if red_center != False and yellow_center != False:
        cv2.line(img, red_center, yellow_center, RED, thickness=1)
        cv2.line(img_masked, red_center, yellow_center, RED, thickness=1)

        # Adding distance (in pixels) label 
        dis = distance(red_center, yellow_center)
        cv2.putText(img, f"d: {dis}", (20, 300), FONT, 1, GREEN, 2, cv2.LINE_AA)
        cv2.putText(img_masked, f"d: {dis}", (20, 300), FONT, 1, GREEN, 2, cv2.LINE_AA)

    if red_center != False and blue_center != False and yellow_center != False:
        # Adding theta (in degrees) label 
        theta = angle(red_center, blue_center, yellow_center, True)
        cv2.putText(img, f"theta: {theta}", (20, 330), FONT, 1, GREEN, 2, cv2.LINE_AA)
        cv2.putText(img_masked, f"theta: {theta}", (20, 330), FONT, 1, GREEN, 2, cv2.LINE_AA)

    # Show the images
    cv2.imshow('original', img)
    cv2.imshow('masked', img_masked)

    return (dis, theta)


if __name__ == "__main__":
    while(True):
        ret, img = vid.read()

        dis, theta = ver(ret, img)
        print(f"distancia: {dis:3f}, angulo: {theta:3f}")
        
        # Press 'q' to exit the loop
        if cv2.waitKey(25) & 0xFF == ord('q'):
            vid.release()
            cv2.destroyAllWindows()
            exit()



            

# if __name__ == "__main__":
#     # Infinite loop of the video
#     while True:  
#         while vid.isOpened():

#             if not vid:
#                 break

#             ret, img = vid.read()
            
#             ver(ret, img)

#             # Press 'q' to exit the loop
#             if cv2.waitKey(25) & 0xFF == ord('q'):
#                 vid.release()
#                 cv2.destroyAllWindows()
#                 exit()

#         Reset the video capture to the start
#         vid.set(cv2.CAP_PROP_POS_FRAMES, 0)