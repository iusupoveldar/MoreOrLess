from Imager import Imager
import pandas as pd
import cv2
from moviepy.editor import ImageClip, CompositeVideoClip
from os.path import exists

 
output_path = "assets\\vids\\raw\\"
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
        vid_name = row['Name'] + row['Condition']
        vid_path = imager.create_rotating_breathing_video(image_path+img_name, output_path+vid_name)   

    imager.create_random_clip() 
    

    
def create_gif_with_transparency(images_path, output_gif_path, duration=100):
    images = [Image.open(os.path.join(images_path, img_path)) for img_path in sorted(os.listdir(images_path)) if img_path.endswith('.png')]
    images[0].save(output_gif_path, save_all=True, append_images=images[1:], duration=duration, loop=0, transparency=0, disposal=2)

def get_six_random_items():
    pass


if __name__ == "__main__":
    main()