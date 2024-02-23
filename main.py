from ImagerMoviePy import Imager
import pandas as pd
import cv2
from moviepy.editor import ImageClip, CompositeVideoClip


# output_path = "C:\\Users\\iusup\\python\\MoreOrLess\\assets\\vids\\"
# image_path = "C:\\Users\\iusup\\python\\MoreOrLess\\assets\\img\\"
output_path = "assets\\vids\\"
image_path = "assets\\img\\"
base_path = "assets\\base\\"

def main():
    df = pd.read_csv('items_list.csv')
    imager = Imager()
    # create background video for a minute
    background_path = imager.create_background()
    print(background_path)
    df['Name'] = df['Name'].str.replace(' | ', '_', regex=False)
    for index, row in df.iterrows(): 
        img_name = row['Name'] + row['Condition']+".png"
        vid_name = row['Name'] + row['Condition']+".mp4"
        # vid_path = imager.create_rotating_breathing_video(image_path+img_name, output_path+vid_name)

        # Load the image with transparency
        img = ImageClip(image_path+img_name).set_duration(10)

        # Create the rotating animation using MoviePy's transformations
        rotated_animation = img.rotate(lambda f: max_angle * np.sin(np.pi * 2 * f)).scale(
            lambda f: start_scale + (np.sin(np.pi * 2 * f) * scale_diff) / 2
        )

        # Create the final video with transparent background
        final_clip = CompositeVideoClip([rotated_animation]).set_duration(duration)

        # Export the video using a transparency-enabled codec
        final_clip.write_videofile(output_path+vid_name, fps=fps, codec='hap')
        print(vid_path)
    
    imager.create_clip(video_fragment_path = vid_path, position = (50,100))
    

    

def get_six_random_items():
    pass


if __name__ == "__main__":
    main()