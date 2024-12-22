# create the ogg letters audio files
import os
from gtts import gTTS
import tkinter as tk
from pygame import mixer
import tkinter.ttk as ttk
from time import sleep
def get_audio(mword,filename):
    audioname = "audio/" + filename + ".ogg"
    if "audio" not in os.listdir():
        os.mkdir("audio")
    language = "ru"
    print("looking for word in dictionary")
    if f"{mword}.ogg" not in os.listdir("audio/"):
        if mword != "":
            print("This is not present... creating")
            t = gTTS(mword, lang=language)
            t.save(audioname)
    return audioname

        
            