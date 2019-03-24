import numpy as np
import sklearn
import librosa
from onset_offset import onset,offset
from pitch_track import p_track, quantizeNotes, pitch_smoothing
from sort import sort

def audio_to_data(audio_path, bpm, key):
    '''
    input audio path and an optional bpm and key
    '''
    #print(bpm)
    x,sr = librosa.load(audio_path)
    pitches,pitch_change = p_track(x,sr,bpm,key)
    #pitch_number = quantizeNotes(pitches,key)
    #print(pitches) 
    velocity = 67
    #onset_array = onset(x,sr,bpm,len(pitches))
    offset_array = offset(x,sr,bpm,len(pitches))
    print(offset_array)
    onset_array = []
    #offset_array = []
    midi_array = []
    event_time, event_type = sort(onset_array,offset_array,pitch_change)
    last_event_time = 0
    #print(event_time)
    #print(event_type)
    last_end = 0
    for i in range(len(event_time)):
        if event_type[i]=="on" or "pitch":
            if event_time[i]!= last_event_time:
                j = find_next_time(event_time,i)
                if i == j:
                    end = 1
                    start = event_time[i]-last_end
                    last_end = event_time[j]
                    #print([pitches[event_time[i]],velocity,start,end])
                    midi_array.append([pitches[event_time[i]],velocity,start,end])
                else:
                    end = event_time[j]-event_time[i]
                    start = event_time[i]-last_end
                    #print([pitches[event_time[i]],velocity,start,end])
                    midi_array.append([pitches[event_time[i]],velocity,start,end])
                    last_end = event_time[j]
            last_event_time = event_time[i]
    return_array = pitch_smoothing(midi_array)
    return return_array

def find_next_time(time_array,pos):
    if pos == len(time_array):
        return pos
    else:
        for j in range(pos,len(time_array)):
            if time_array[pos]!= time_array[j]:
                return j
    return j
    
