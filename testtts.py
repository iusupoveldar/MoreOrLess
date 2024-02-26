from tiktokvoice import *
import os
import pandas
def create_tts(text):
        tts_path = f'assets\\tts\\{text}.mp3'
        if (os.path.exists(tts_path)):
            return tts_path
        else:
            tts(text, voice = 'en_male_narration', filename = tts_path, play_sound = False)
            return tts_path

create_tts("(Field-Tested)")