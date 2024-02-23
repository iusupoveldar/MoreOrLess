import cv2
import numpy as np
import os
from moviepy.editor import ImageClip, CompositeVideoClip, vfx, VideoClip, VideoFileClip
from moviepy.video.fx import rotate
from moviepy.video.fx.resize import resize
from PIL import Image

class Imager:
    def __init__(self):
        pass

    def rotate_and_scale_image(self, image, angle, scale):
        """Rotate and scale the image by the given angle and scale around its center, replacing transparent areas with green chroma key."""
        if image.shape[2] == 4:  # Check if the image has an alpha channel
            color_channel = image[..., :3]
            alpha_channel = image[..., 3]
        else:
            color_channel = image
            alpha_channel = None

        h, w = color_channel.shape[:2]
        center = (w // 2, h // 2)

        # Define the green chroma key color (typically bright green)
        green_background = np.full((h, w, 3), (0, 255, 0), dtype=np.uint8)

        # Compute the rotation and scaling matrix
        M = cv2.getRotationMatrix2D(center, angle, scale)

        # Rotate and scale the color channels and green background
        rotated_scaled_color = cv2.warpAffine(color_channel, M, (w, h))
        rotated_green_background = cv2.warpAffine(green_background, M, (w, h))

        if alpha_channel is not None:
            # Rotate and scale the alpha channel
            rotated_scaled_alpha = cv2.warpAffine(alpha_channel, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            # Convert alpha channel to 3 channels
            alpha_3_channel = cv2.merge([rotated_scaled_alpha, rotated_scaled_alpha, rotated_scaled_alpha])
            # Use the alpha channel as a mask to combine the rotated color image with the green background
            foreground = cv2.bitwise_and(rotated_scaled_color, alpha_3_channel)
            background = cv2.bitwise_and(rotated_green_background, 255 - alpha_3_channel)
            rotated_scaled = cv2.add(foreground, background)
        else:
            rotated_scaled = rotated_scaled_color

        return rotated_scaled

    def create_rotating_breathing_video(self, image_path, output_path, fps=30, duration=10, max_angle=10, start_scale=1.0, end_scale=1.2):
        if os.path.exists(output_path):
            print(f"Video already exists: {output_path}")
            return output_path
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  # Ensure alpha channel is read
        height, width = img.shape[:2]
        frame_count = duration * fps
        scale_diff = end_scale - start_scale

        # Prepare video writer, using a codec that supports transparency if available
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # Note: Transparency may not be preserved in all video codecs/formats
        video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        for frame in range(frame_count):
            angle = max_angle * np.sin(np.pi * 2 * frame / frame_count)
            scale = start_scale + (np.sin(np.pi * 2 * frame / frame_count) * scale_diff) / 2

            rotated_scaled_img = self.rotate_and_scale_image(img, angle, scale)

            # Handle images with and without alpha channel
            if rotated_scaled_img.shape[2] == 4:
                bgr_img = cv2.cvtColor(rotated_scaled_img, cv2.COLOR_BGRA2BGR)
                video.write(bgr_img)
            else:
                video.write(rotated_scaled_img)

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


    
