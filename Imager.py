import cv2
import numpy as np
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageSequenceClip, concatenate_videoclips, TextClip
import random
import uuid
import pandas as pd
from tiktokvoice import *

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

    def create_tts(self, text):
        pass

    def create_clip_scene(self):
        pass

    def create_random_clip(self):
        # Consolas-Bold
        # Gadugi-Bold
        font = 'Consolas-Bold'
        df = pd.read_csv('items_list.csv')
        df['NameEdit'] = df['Name'].str.replace(' | ', '_', regex=False)
        df['comb'] = df['NameEdit'] + df['Condition']
        background_path = 'assets\\base\\background.mp4'

        background_video = VideoFileClip(background_path).set_duration(10)

        width, height = background_video.size
        first_item_pos = (-200,-275) 
        first_item_price_pos = ('center',700) 
        first_item_name_pos = ('center',100) 
        second_item_pos = (-200,775)
        second_item_price_pos = ('center',1150) 
        second_item_name_pos = ('center',1700) 

        # Load the video you've just created 
        videos = []
        loops = 6
        for i in range(loops): 
            overlay_videos = []
            overlay_prices = []
            overlay_names = []
            folder_list = self.get_folder_names('assets\\vids\\raw')
            print("creating clips", i)
            for index, folder in enumerate(folder_list): 
                print(folder)
                match = df[(df['comb'] == folder)]
                print(f"this is the price i found {match['Price'].values[0]}")
                folder_dir = f'assets\\vids\\raw\\{folder}'
                length_items = len(os.listdir(folder_dir))
                item_name = folder.split('\\')[-1]
                image_files = [f'{folder_dir}/frame_{i:04d}.png' for i in range(length_items)]  # Adjust pattern as needed

                # Create an image sequence clip
                original_name_text = TextClip(f"{match['Name'].values[0].split(' | ')[0]}\n{match['Name'].values[0].split(' | ')[1]} {match['Condition'].values[0]}", fontsize=70, color='white', font=font).set_duration(10)
                overlay_name_text = TextClip(f"{match['Name'].values[0].split(' | ')[0]}\n{match['Name'].values[0].split(' | ')[1]} {match['Condition'].values[0]}", fontsize=74, color='black', font=font).set_duration(10)
                overlay_names.append(original_name_text)
                # overlay_names.append(overlay_name_text)
                original_price_text = TextClip(f"${match['Price'].values[0]}", fontsize=70, color='white', font=font).set_duration(5)
                overlay_price_text = TextClip(f"${match['Price'].values[0]}", fontsize=74, color='black', font=font).set_duration(5)
                overlay_prices.append(original_price_text)
                # overlay_prices.append(overlay_price_text)
                overlay_videos.append(ImageSequenceClip(image_files, fps=30)) 
            
            # Create outline clip of the "OR" text
            or_clip_outline = TextClip(f"OR\n{i+1}/{loops}", fontsize=74, color='black', font=font).set_duration(10)
            or_clip = TextClip(f"OR\n{i+1}/{loops}", fontsize=70, color='white', font=font).set_duration(10)
            
            # Set the position of the text clip to the center of the video
            or_clip_outline = or_clip_outline.set_pos('center')
            or_clip = or_clip.set_pos('center')

            # item 1
            clip1_image = overlay_videos[0].set_position(first_item_pos)
            clip1_name = overlay_names[0].set_position(first_item_name_pos)
            # clip1_name_out = overlay_names[1].set_position(first_item_name_pos)
            clip1_price = overlay_prices[0].set_position(first_item_price_pos).set_start(5)
            # clip1_price_out = overlay_prices[1].set_position(first_item_price_pos).set_start(5)

            # item 2
            clip2_image = overlay_videos[1].set_position(second_item_pos)
            clip2_name = overlay_names[1].set_position(second_item_name_pos)
            # clip2_name_out = overlay_names[3].set_position(second_item_name_pos)
            clip2_price = overlay_prices[1].set_position(second_item_price_pos).set_start(5)
            # clip2_price_out = overlay_prices[3].set_position(second_item_price_pos).set_start(5)

            temp_vids = [background_video, clip1_image, clip1_name, clip1_price, clip2_image, clip2_name, clip2_price,or_clip_outline, or_clip]
            clip = CompositeVideoClip(temp_vids, size=background_video.size)
            clip.write_videofile(f'assets\\vids\\finished\\{uuid.uuid4()}.mp4', fps=30)
            input()
            # Overlay the video
            videos.append(clip)

            # Write the result to a file 
        print("Done creating small clips")
        output_video_path = f'assets\\vids\\finished\\{uuid.uuid4()}.mp4'  
        final_video = concatenate_videoclips(videos)
        final_video.write_videofile(output_video_path, fps=background_video.fps)
        print("Done")
 
    def create_clips(self): 

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

            print("Done")

    # get price where it matches
    def get_price(self, name, condition):
        # Filter the dataframe based on the Name and Condition
        
        
        # If there is a match, return the Price, else return None or a custom message
        if not match.empty:
            return match['Price'].values[0]
        else:
            return "No match found"

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
        Gets two random folder names from the given path.

        Args:
            path: The path to the directory.

        Returns:
            A list of two random folder names.
        """

        # Get a list of all entries (files and directories)
        entries = os.listdir(path)

        # Filter out files and keep only directories
        folder_names = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
        # Return two random folder names, or all if there are less than two
        return random.sample(folder_names, min(len(folder_names), 2))


    
