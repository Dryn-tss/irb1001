import cv2
import numpy as np

def create_blank_video(output_path: str, duration: int = 3, fps: int = 30, width: int = 640, height: int = 480, color: tuple[int, int, int] = (0, 0, 0)):
    """
    Create a blank video of a specified duration.

    Args:
        output_path (str): The path where the video will be saved.
        duration (int): The duration of the video in seconds.
        fps (int): Frames per second.
        width (int): Width of the video frame.
        height (int): Height of the video frame.
        color (Tuple[int, int, int]): The color of the blank frames (BGR format).
    """
    # Calculate the total number of frames
    total_frames = duration * fps
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use 'XVID' or 'MJPG' as well
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Create a blank frame
    blank_frame = np.full((height, width, 3), color, dtype=np.uint8)
    
    # Write the blank frames to the video file
    for _ in range(total_frames):
        out.write(blank_frame)
    
    # Release the video writer
    out.release()
    print(f"Blank video created and saved at {output_path}")

# Example usage
output_path = 'blank.mp4'
create_blank_video(output_path, duration=15, fps=30, width=640, height=480, color=(0, 0, 0))  # Black frames
