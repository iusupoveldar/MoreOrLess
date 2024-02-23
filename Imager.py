import cv2
import numpy as np
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip

class Imager:
    def __init__(self):
        pass

    def rotate_and_scale_image(self, image, angle, scale):
        """Rotate and scale the image by the given angle and scale around its center."""
        h, w = image.shape[:2]
        center = (w // 2, h // 2)

        # Compute the combined rotation and scaling matrix.
        M = cv2.getRotationMatrix2D(center, angle, scale)
        # Perform the rotation and scaling.
        rotated_scaled = cv2.warpAffine(image, M, (w, h))
        return rotated_scaled

    def create_rotating_breathing_video(self, image_path, output_path, fps=30, duration=10, max_angle=10, start_scale=1.0, end_scale=1.2):
        if os.path.exists(output_path):
            print(f"Video already exists: {output_path}")
            return output_path
        img = cv2.imread(image_path)
        height, width = img.shape[:2]
        frame_count = duration * fps
        scale_diff = end_scale - start_scale

        # Prepare video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        for frame in range(frame_count):
            # Calculate current rotation angle and scale for breathing effect
            angle = max_angle * np.sin(np.pi * 2 * frame / frame_count)
            scale = start_scale + (np.sin(np.pi * 2 * frame / frame_count) * scale_diff) / 2

            # Apply the rotation and scaling to the image
            rotated_scaled_img = self.rotate_and_scale_image(img, angle, scale)

            # Write the frame to the video
            video.write(rotated_scaled_img)

        # Release the video writer
        video.release()
        print(f"Video created: {output_path}")
        return output_path


    def create_background(self, fps = 30, duration = 60, base_path = 'assets\\base\\', output_path = 'assets\\base\\background.mp4'):
        if os.path.exists(base_path + 'background.mp4'):
            print(f"Video already exists: {base_path + 'background.mp4'}")
            return output_path
        background_path = base_path + 'background.png'  # Path to your image 

        # Read the image
        image = cv2.imread(background_path)
        image_height, image_width, _ = image.shape

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
        out = cv2.VideoWriter(output_path, fourcc, fps, (image_width, image_height))

        # Add frames to the video
        for i in range(duration * fps): 
            out.write(image)

        # Release everything when job is finished
        out.release()
        return output_path

    def create_clip(self, duration = 10, fps = 30, font = '', 
        background_path = 'assets\\base\\background.mp4', text = '', 
        position = (50,100), video_fragment_path = '',
        output_video_path = 'assets\\base\\out.mp4', font_size = 24):
         
        background_video = VideoFileClip(background_path)

        # Load the video you've just created
        overlay_video = VideoFileClip(video_fragment_path)

        # Set the position of the overlay video on the existing video (e.g., top middle)
        overlay_position = ('center', 'top')  # Adjust as needed

        # Overlay the video
        final_video = CompositeVideoClip([background_video, overlay_video.set_position(overlay_position).set_start(0)], size=background_video.size)

        # Write the result to a file 
        final_video.write_videofile(output_video_path, fps=background_video.fps)
        print("Done")


    
