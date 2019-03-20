from audio_to_data import audio_to_data
from file_create import midi_file_create

def wavtomid (path,nof,bpm=120,key='chromatic',clocks_per_click = 24):
    '''
    takes in a file path, a bpm, a key and the name of a file and creates a midi file
    '''
    mid = midi_file_create((audio_to_data(path,bpm,key)),nof,bpm,key,clocks_per_click)
    return mid 