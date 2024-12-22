import sys
import librosa

from sound_to_midi.monophonic import wave_to_midi

def audio_to_midi(file_in, file_out):
    print("Starting...")
    y, sr = librosa.load(file_in, sr=None)
    print(y, sr)
    print("Audio file loaded!")
    midi = wave_to_midi(y)
    print("Conversion finished!")
    with open (file_out, 'wb') as f:
        midi.writeFile(f)
    print("Done. Exiting!")