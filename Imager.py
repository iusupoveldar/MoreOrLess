import cv2
import numpy as np
import os

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
