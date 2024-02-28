import cv2
import numpy as np

def rotate_image(image, angle):
    """Rotate the image by the given angle around its center."""
    h, w = image.shape[:2]
    center = (w // 2, h // 2)

    # Compute the rotation matrix.
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # Perform the rotation.
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def create_rotating_video(image_path, output_path, fps=60, duration=10, max_angle=10):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frames = duration * fps
    half_frames = frames // 2
    angle_step = max_angle / half_frames
    
        if frame <= half_frames:
            angle = angle_step * frame
        else:
            angle = max_angle - angle_step * (frame - half_frames)
        
        rotated_img = rotate_image(image, angle)
        out.write(rotated_img)
    
    out.release()

# Example usage:
image_path = '1.png'  # Change to your image path
output_path = 'rotating_effect60fps10angle.mp4'
create_rotating_video(image_path, output_path)
