from mido import Message, MidiFile, MidiTrack
import numpy as np
##input should be an n by 4 numpy array with n being each note and input[n,0]=note
##input[n,1]=velocity, input[n,2]=starttime, imput[n,3]=endtime
##the second input is the name of the ouput file as a string
def midi_file_create(notes,nof):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change',program=0,time=0))
    num_notes = notes.shape[0]
    check = notes.shape[1]
    print(notes)
    if check != 4:
        raise Exception('Height of Array does not equal 3')
    else:
        for i in range(num_notes):
            if notes[i,0]>127:
                raise Exception('Note not in range[0,127]')
            else:
                if notes[i,1]>127:
                    raise Exception('Velocity not in range[0,127]')
                else:
                    track.append(Message('note_on',note=int(notes[i,0]),velocity=int(notes[i,1]),time=int(notes[i,2])))
                    track.append(Message('note_off',note=int(notes[i,0]),velocity=int(notes[i,1]),time=int(notes[i,3])))
        if nof.endswith('.mid'):
            mid.save(filename=nof)
        else:
            mid.save(filename=nof+'.mid')

