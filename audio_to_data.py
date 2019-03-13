import numpy as np
import sklearn
import librosa
from onset_offset import onset,offset

def audio_to_data(audio_path, bpm):
    #x,sr = librosa.load("sinesweep_recording.wav")
    pitches = pitch_track
    onset = onset(x,sr,bpm)
    offset = offset(x,sr,bpm)
    offset_index=0
    #for event in range(len(onset)):
        #if offset[offset_index]<onset[event+1]:
        #then append note,onset[event],offset[offset_index],vel

        #if offset[offset_index]>onset[event+1]:
        #then append note,onset[event],onset[index+1],vel

        #if the pitch changes then redo for loop but with start as time of pitch change
    return False