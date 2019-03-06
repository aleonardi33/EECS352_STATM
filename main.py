import numpy as np
from file_create import midi_file_create
from mido import Message, MidiFile, MidiTrack

notes = np.zeros((1,4))
notes[0,0]=int(63)
notes[0,1]=int(63)
notes[0,2]=int(0)
notes[0,3]=int(30)
midi_file_create(notes,'test')