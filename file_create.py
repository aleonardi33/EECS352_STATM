from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
import mido
import numpy as np

def midi_file_create(notes,nof,bpm,key,clocks_per_click):
    '''
    input should be an n by 4 numpy array with n being each note and input[n,0]=note
    input[n,1]=velocity, input[n,2]=starttime, imput[n,3]=endtime
    the second input is the name of the ouput file as a string
    '''
    mid = MidiFile(type=0)
    if key != 'chromatic':
        MetaMessage('key_signature', key = key, time = 0)
    MetaMessage('time_signature', clocks_per_click = clocks_per_click, time = 0)
    MetaMessage('set_tempo', tempo = bpm2tempo(bpm), time = 0)
    mid.ticks_per_beat = 24
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change',program=0,time=0))
    #MetaMessage('set_tempo',mido.bpm2tempo(bpm))
    notes_np = np.array(notes)
    num_notes = notes_np.shape[0]
    #print(num_notes)
    check = notes_np.shape[1]
    #print(notes)
    if check != 4:
        raise Exception('Height of Array does not equal 3')
    else:
        for i in range(num_notes):
            #print(notes_np[i])
            if notes_np[i,0]>127:
                raise Exception('Note not in range[0,127]')
            else:
                if notes_np[i,1]>127:
                    raise Exception('Velocity not in range[0,127]')
                else:
                    track.append(Message('note_on',note=int(notes_np[i,0]),velocity=int(notes_np[i,1]),time=int(notes_np[i,2])))
                    track.append(Message('note_off',note=int(notes_np[i,0]),velocity=int(notes_np[i,1]),time=int(notes_np[i,3])))
        #if nof.endswith('.mid'):
            #mid.save(filename=nof)
        #else:
            #mid.save(filename=nof+'.mid')
        return mid


