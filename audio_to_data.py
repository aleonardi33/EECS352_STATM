import numpy as np
import sklearn
import librosa
from onset_offset import onset,offset
from pitch_track import p_track, quantizeNotes
from sort import sort

def audio_to_data(audio_path, bpm=120, key = "chromatic"):
    x,sr = librosa.load(audio_path)
    pitches,pitch_change = p_track(x,sr,bpm)
    pitch_number = quantizeNotes(pitches,key)
    velocity = 67
    onset_array = onset(x,sr,bpm)
    offset_array = offset(x,sr,bpm)
    midi_array = []
    event_time, event_type = sort(onset_array,offset_array,pitch_change)
    for i in range(len(event_time)):
        if event_type[i]=="on" or "pitch":
            j = i + 1
            while event_time[i]==event_time[j]:
                j =j+1
            midi_array.append(pitch_number[event_time[i]],velocity,[event_time[i],event_time[j]])
    return midi_array