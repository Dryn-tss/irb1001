import cv2 
import numpy as np
# from PIL import Image

# VARIABLES
PATH_VID = 'vid.mp4'
VID = True
FONT = cv2.FONT_HERSHEY_SIMPLEX

# Colors
GREEN = (0, 200, 0)
RED = (0, 0, 200)
BLUE = (200, 0, 0)
YELLOW = (0, 200, 200)
PURPLE = (132, 10, 132)
NAVY = (134, 68, 68)
GRAY = (102, 102, 102)

# Range of the colors in HSV
LOW_GREEN = np.array([40, 100, 100])
HIGH_GREEN = np.array([80, 255, 255])

# LOW_RED = np.array([170, 50, 150])
# HIGH_RED = np.array([180, 255, 255])

LOW_RED = np.array([0, 50, 150])
HIGH_RED = np.array([20, 255, 255])

LOW_BLUE = np.array([100, 100, 100])
HIGH_BLUE = np.array([108, 255, 255])

LOW_YELLOW = np.array([20, 100, 100])
HIGH_YELLOW = np.array([30, 255, 255])

# Goal areas colors
LOW_PURPLE = np.array([120, 100, 50])
HIGH_PURPLE = np.array([160, 255, 255])

LOW_NAVY = np.array([80, 100, 50])
HIGH_NAVY = np.array([120, 255, 255])

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
    return (0, 0)

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

    cross_product = np.cross(AB, AC)
    if cross_product < 0:
        theta = -theta
    
    if deg:
        theta_degrees = np.degrees(theta)
        return round(theta_degrees, 2)
    return round(theta, 2)

def midpoint(red_center, blue_center):
    A = np.array([red_center[0], red_center[1]])
    B = np.array([blue_center[0], blue_center[1]])

    mid = (A + B) / 2
    return (int(mid[0]), int(mid[1]))

def draw_lines(img, red_center, blue_center, yellow_center):
    info = {}
    # With red and blue
    if red_center != False and blue_center != False:
        # draw orientation line
        end_x = red_center[0] + ((blue_center[0] - red_center[0]) * 10)
        end_y = red_center[1] + ((blue_center[1] - red_center[1]) * 10)
        end_point = (end_x, end_y)
        cv2.line(img, red_center, end_point, BLUE, thickness=1)

        # Draw a dot on the center of the robot
        robot_center = midpoint(red_center, blue_center)
        cv2.circle(img, robot_center, 2, YELLOW, thickness=2)
        info['robot_center'] = robot_center

    # With red and yellow
    if red_center != False and yellow_center != False:
        # draw ball line
        cv2.line(img, red_center, yellow_center, RED, thickness=1)

        # Adding distance (in pixels) label 
        dis = distance(red_center, yellow_center)
        cv2.putText(img, f"d: {dis}", (20, 300), FONT, 1, GREEN, 2, cv2.LINE_AA)
        info['dis'] = dis

    # With red, blue and yellow
    if red_center != False and blue_center != False and yellow_center != False:
        # Adding theta (in degrees) label 
        theta = angle(red_center, blue_center, yellow_center, True)
        cv2.putText(img, f"theta: {theta}", (20, 330), FONT, 1, GREEN, 2, cv2.LINE_AA)
        info['theta'] = theta

    return info

def masks(ret, img):
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
    img_masked = cv2.bitwise_or(img_masked, img_masked_purple)
    img_masked = cv2.bitwise_or(img_masked, img_masked_navy)

    # img_masked = cv2.bitwise_or(img_masked_purple, img_masked_navy)


    # For each mask find contours and draw the boxes 
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_center = draw_box(img, img_masked, contours, RED, "R")

    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_center = draw_box(img, img_masked, contours, BLUE, "B")

    contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    yellow_center = draw_box(img, img_masked, contours, YELLOW, "Y")

    contours, _ = cv2.findContours(purple_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    purple_center = draw_box(img, img_masked, contours, PURPLE, "P")

    contours, _ = cv2.findContours(navy_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    navy_center = draw_box(img, img_masked, contours, NAVY, "N")

    return (img, img_masked, red_center, blue_center, yellow_center, (purple_center, navy_center))
    
def ver(img, img_masked, red_center, blue_center, yellow_center, goal):

    # If it detects the circles, make the lines and labels
    info = draw_lines(img, red_center, blue_center, yellow_center)
    draw_lines(img_masked, red_center, blue_center, yellow_center)


    # Obtain the center of the image
    height, width = img.shape[:2]
    img_center = midpoint((0, 0), (width, height))
    info["img_center"] = img_center
    cv2.circle(img, img_center, 2, PURPLE, thickness=2)
    cv2.circle(img_masked, img_center, 2, PURPLE, thickness=2)

    theta_center = angle(red_center, blue_center, img_center)
    info['theta_center'] = theta_center

    dis_center = distance(info['robot_center'], img_center)
    info['dis_center'] = dis_center


    # Show the images
    cv2.namedWindow('original', cv2.WINDOW_NORMAL)
    cv2.moveWindow('original', 700, 10)
    cv2.imshow('original', img)
    cv2.namedWindow('masked', cv2.WINDOW_NORMAL)
    cv2.moveWindow('masked', 50, 10)
    cv2.imshow('masked', img_masked)

    info['goal_purple'] = goal[0]
    info['goal_navy'] = goal[1]

    theta_purple = angle(red_center, blue_center, info['goal_purple'])
    dis_purple = distance(info['robot_center'], info['goal_purple'])
    info['theta_purple'] = theta_purple
    info['dis_purple'] = dis_purple

    theta_navy = angle(red_center, blue_center, info['goal_navy'])
    dis_navy = distance(info['robot_center'], info['goal_navy'])
    info['theta_navy'] = theta_navy
    info['dis_navy'] = dis_navy

    return info


if __name__ == "__main__":
    if VID:
        # Open the video file 
        vid = cv2.VideoCapture(PATH_VID)

        if not vid.isOpened():
            vid = cv2.VideoCapture(1)

        if not vid.isOpened():
            vid = cv2.VideoCapture(0)

    if not vid.isOpened():
        print("Error: Could not open video or camera.")
        exit()

    while(True):
        vid.set(cv2.CAP_PROP_POS_FRAMES, 0)   # Reset the video capture to the start
        
        while vid.isOpened():
            ret, img = vid.read()
            if not ret:
                break

            img, img_masked, red_center, blue_center, yellow_center, goal = masks(ret, img)
            info = ver(img, img_masked, red_center, blue_center, yellow_center, goal)
            # print(f"distancia: {info['dis']:3f}, angulo: {info['theta']:3f}")
            if 'robot_center' in info:
                print(True)
            else:
                print(False)
            

            if cv2.waitKey(25) & 0xFF == ord('q'):  # Press 'q' to exit the loop
                vid.release()
                cv2.destroyAllWindows()
                exit()

            



            