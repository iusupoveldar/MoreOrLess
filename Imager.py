import cv2
import numpy as np
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageSequenceClip

class Imager:
    def __init__(self):
        pass

    def rotate_and_scale_image(self, image, angle, scale):
        """Rotate and scale the image by the given angle and scale around its center, preserving transparency."""
        h, w = image.shape[:2]
        center = (w // 2, h // 2)

        # Split the image into its color channels and alpha channel
        if image.shape[2] == 4:
            color_channels = image[:, :, :3]
            alpha_channel = image[:, :, 3]
        else:
            # If there's no alpha channel, create one filled with 255 (opaque)
            color_channels = image
            alpha_channel = np.ones((h, w), dtype=image.dtype) * 255

        # Compute the rotation matrix for the color channels
        M = cv2.getRotationMatrix2D(center, angle, scale)
        # Perform the rotation on color channels and alpha channel
        rotated_color = cv2.warpAffine(color_channels, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        rotated_alpha = cv2.warpAffine(alpha_channel, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

        # Merge the color channels and alpha channel back into one image
        rotated_scaled = cv2.merge((rotated_color, rotated_alpha))

        return rotated_scaled

    def create_rotating_breathing_video(self, image_path, output_path, fps=30, duration=10, max_angle=10, start_scale=1.0, end_scale=1.2):
        img = cv2.imread(image_path, -1) # Make sure to load the alpha channel 
        
        height, width = img.shape[:2]
        frame_count = duration * fps
        scale_diff = end_scale - start_scale

        if not os.path.exists(output_path):
            os.makedirs(output_path) 
            for frame in range(frame_count):
                # Calculate current rotation angle and scale for breathing effect
                angle = max_angle * np.sin(np.pi * 2 * frame / frame_count)
                scale = start_scale + (scale_diff * np.sin(np.pi * 2 * frame / frame_count)) / 2

                # Apply the rotation and scaling to the image
                rotated_scaled_img = self.rotate_and_scale_image(img, angle, scale) 
                # Save the frame as a PNG image
                frame_file = os.path.join(output_path, f"frame_{frame:04d}.png")
                cv2.imwrite(frame_file, rotated_scaled_img)
        else:
            print("Folder already exists")
        
        print(f"Frames saved to {output_path}")
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


    # , duration = 10, fps = 30, font = '', text = '', position = (50,100), font_size = 24
    def create_clips(self):
        # background_path = 'assets\\base\\background.mp4'

        # background_video = VideoFileClip(background_path)

        # width, height = background_video.size

        # Load the video you've just created 
        folder_list = [x[0] for x in os.walk('assets\\vids\\raw')][1::]
        for index, folder in enumerate(folder_list): 
            length_items = len(os.listdir(folder))
            item_name = folder.split('\\')[-1]
            image_files = [f'{folder}/frame_{i:04d}.png' for i in range(length_items)]  # Adjust pattern as needed

            # Create an image sequence clip
            overlay_video = ImageSequenceClip(image_files, fps=30)
            
            # Save the video
            output_video_path = f'assets\\vids\\finished\\{item_name}.mp4'
            overlay_video.write_videofile(output_video_path, fps=30)

            # Set the position of the overlay video on the existing video (e.g., top middle)
            # overlay_position = ('center', 'top')  # Adjust as needed

            # output_video_path = f'assets\\result\\output{index}.mp4'
            # # Overlay the video
            # final_video = CompositeVideoClip([background_video, overlay_video.set_position((-200,-275)), overlay_video.set_position((-200,275))], size=background_video.size)

            # # Write the result to a file 
            # final_video.write_videofile(output_video_path, fps=background_video.fps)
            print("Done")

    def create_clip(self, filename):   
        folder_name = f'assets\\vids\\raw\\{filename}'
        length_items = len(os.listdir(folder_name))
        item_name = folder_name.split('\\')[-1]
        image_files = [f'{folder_name}/frame_{i:04d}.png' for i in range(length_items)]  # Adjust pattern as needed

        # Create an image sequence clip
        overlay_video = ImageSequenceClip(image_files, fps=30)
        
        # Save the video
        output_video_path = f'assets\\vids\\finished\\{item_name}.mp4'
        overlay_video.write_videofile(output_video_path, fps=30) 
        print("Done")

    def get_folder_names(self, path):
        """
        Gets a list of folder names in the given path.

        Args:
            path: The path to the directory.

        Returns:
            A list of folder names.
        """

        # Get a list of all entries (files and directories)
        entries = os.listdir(path)

        # Filter out files and keep only directories
        folder_names = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]

        return folder_names


    
