import cv2
import numpy as np
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageSequenceClip, concatenate_videoclips, TextClip, AudioFileClip, concatenate_audioclips, ImageClip
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

    def create_rotating_breathing_video(self, image_path, output_path, fps=30, duration=10, max_angle=10, start_scale=1.5, end_scale=1.8):
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
        tts_path = f'assets\\tts\\{text}.mp3'
        if (os.path.exists(tts_path)):
            return AudioFileClip(tts_path)
        else:
            # en_male_narration, slow, maybe something faster?
            # en_us_006 is okay
            tts(text, voice = 'en_us_006', filename = tts_path, play_sound = False)
            return AudioFileClip(tts_path)
 

    def create_random_clip(self):
        # Consolas-Bold
        # Gadugi-Bold
        font = 'Consolas-Bold'
        df = pd.read_csv('items_list.csv')
        df = df.fillna("NA")
        df['NameEdit'] = df['Name'].str.replace(' | ', '_', regex=False)
        df['comb'] = df['NameEdit'] + df['Condition']
        background_path = 'assets\\base\\background.mp4'
        
        price_duration = AudioFileClip("assets\\base\\ending_sound.mp3").duration

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
            audio_clips = []
            audio = ""
            folder_list = self.get_folder_names('assets\\vids\\raw')
            print("creating clips", i)
            for index, folder in enumerate(folder_list): 
                print(folder)
                match = df[(df['comb'].str.strip() == folder)] 
                folder_dir = f'assets\\vids\\raw\\{folder}'
                length_items = len(os.listdir(folder_dir))
                item_name = folder.split('\\')[-1]
                image_files = [f'{folder_dir}/frame_{i:04d}.png' for i in range(length_items)]  # Adjust pattern as needed
                
                # print(match)
                gun_name = ''
                gun_type = ''
                if ("|" in match['Name'].values[0]):
                    gun = match['Name'].values[0].split(' | ')
                    gun_type = gun[0]
                    gun_name = gun[1]
                else:
                    gun = match['Name'].values[0]
                    gun_type = gun
                gun_codition = match['Condition'].values[0]

                if gun_codition == "NA":
                    gun_codition = ""

                gun_price = match['Price'].values[0]

                if (index == 0):  
                    audio = "What cost more " + gun_type + " " +  gun_name + gun_codition + " or " 
                else:   
                    audio += gun_type + " " +  gun_name + gun_codition + "  "

                # Create an image sequence clip
                original_name_text = TextClip(f"{gun_type}\n{gun_name} {gun_codition}", fontsize=60, color='white', font=font).set_duration(10)
                overlay_names.append(original_name_text) 
                original_price_text = TextClip(f"${gun_price}", fontsize=70, color='white', font=font).set_duration(price_duration) 
                overlay_prices.append(original_price_text) 
                overlay_videos.append(ImageSequenceClip(image_files, fps=30)) 
            

            clip_audio = self.create_tts(audio)
            voice_duration = clip_audio.duration
            start_point_ending = 10 - voice_duration + 0.15
            # create the audio file ending
            ticking_sound = AudioFileClip("assets\\base\\ticking_sound.mp3")
            ending_sound = AudioFileClip("assets\\base\\ending_sound.mp3")
            ending_sound_duration = ending_sound.duration   
            ticking_sound_duration = ticking_sound.duration
            ticking_duration = 10 - clip_audio.duration - ending_sound.duration - 0.1
            ticking_sound = ticking_sound.subclip(round(ticking_duration,2))

            audio_clips.extend([clip_audio, ticking_sound, ending_sound])

            # Create outline clip of the "OR" text 
            or_clip = TextClip(f"OR\n{i+1}/{loops}", fontsize=70, color='white', font=font).set_duration(10)
            # Set the position of the text clip to the center of the video 
            or_clip = or_clip.set_pos('center')

            # item 1
            clip1_image = overlay_videos[0].set_position(first_item_pos)
            clip1_name = overlay_names[0].set_position(first_item_name_pos) 
            clip1_price = overlay_prices[0].set_position(first_item_price_pos).set_start(10 - price_duration) 

            # item 2
            clip2_image = overlay_videos[1].set_position(second_item_pos)
            clip2_name = overlay_names[1].set_position(second_item_name_pos) 
            clip2_price = overlay_prices[1].set_position(second_item_price_pos).set_start(10 - price_duration) 
            
            # item 1 audio
            clips_audio = concatenate_audioclips(audio_clips)


            # twitch banner with opacity
            twitch_clip = ImageClip('assets\\base\\twitch_banner.png')
            twitch_clip = twitch_clip.set_duration(10).set_opacity(0.5).resize(0.15).set_position('left', 'center')

            temp_vids = [background_video, clip1_name, clip1_price, clip2_name, clip2_price, or_clip, twitch_clip, clip2_image, clip1_image]
            clip = CompositeVideoClip(temp_vids, size=background_video.size)
            # Set the audio to the video clip starting at the specific time
            clip = clip.set_audio(clips_audio)

            clip.write_videofile(f'assets\\vids\\finished\\{str(i)}.mp4', fps=30, codec='libx264', audio_codec='aac')
            # input()
            # Overlay the video
            # videos.append(clip)

            # Write the result to a file 
        print("Done creating small clips")
        path_to_vids = 'assets\\vids\\finished'
        video_files = [f for f in os.listdir(path_to_vids) if f.endswith('.mp4')]
        video_files.sort()
        clips = [VideoFileClip(os.path.join(path_to_vids, filename)) for filename in video_files]
        final_clip = concatenate_videoclips(clips)

        output_path = f'assets\\vids\\{uuid.uuid4()}.mp4'
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac') 
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


    
