import cv2
import numpy as np

image_path = "1.png"  # Placeholder path, replace with your actual image path
img = cv2.imread(image_path)

# Video parameters
output_path = "rotating_breathing_effect.mp4"
fps = 30
duration = 10  # seconds for the whole effect
frame_count = duration * fps

# Rotation parameters
max_angle = 20  # Maximum rotation angle

# Breathing effect parameters
start_scale = 1.0
end_scale = 1.2
scale_diff = end_scale - start_scale

# Prepare video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
height, width = img.shape[:2]
video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

for frame in range(frame_count):
    # Calculate current rotation angle
    angle = max_angle * np.sin(np.pi * 2 * frame / frame_count)
    
    # Calculate current scale for breathing effect
    scale = start_scale + (np.sin(np.pi * 2 * frame / frame_count) * scale_diff) / 2
    
    # Rotate the image
    M_rot = cv2.getRotationMatrix2D((width / 2, height / 2), angle, scale)
    rotated_scaled_img = cv2.warpAffine(img, M_rot, (width, height))
    
    # Write the frame
    video.write(rotated_scaled_img)

# Release the video writer
video.release()

# Provide the path to the output video file
output_path
