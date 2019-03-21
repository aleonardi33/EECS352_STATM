import numpy as np
from file_create import midi_file_create
from mido import Message, MidiFile, MidiTrack, tempo2bpm, MetaMessage
from sort import sort
from audio_to_data import audio_to_data
import librosa
from pitch_track import p_track
from wavtomid import wavtomid
#from onset_offset import onset,offset

###11, 15, 22, 25, 27, 31, 37, 39, 43, 45
'''
notes = np.zeros((1,4))
notes[0,0]=int(63)
notes[0,1]=int(63)
notes[0,2]=int(0)
notes[0,3]=int(30)
midi_file_create(notes,'test')
on = [0,5,2,17]
off = [0,1,6,3]
pitch = [8,3,10]
event_time, event_type = sort(on,off,pitch)
print(event_time)
print(event_type)
'''
'''
'''
#wavtomid('trumpet.wav',nof = 'test1',bpm=175)
test = 'MIR-QBSH-corpus/waveFile'
year = '/year'
person = '/person000'
number = '/000'
wav = '.wav'
mid = '.mid'
#wavtomid(test+year+'0'+person+'01'+number+'27'+wav,nof = '00035'+mid,bpm=120,clocks_per_click=24)
key_dict = {}
key_dict['C']=0
key_dict['D']=1
key_dict['E']=2
key_dict['F']=3
key_dict['G']=4
key_dict['A']=5
key_dict['B']=6
key_dict['C#']=10
key_dict['D#']=11
key_dict['E#']=12
key_dict['F#']=13
key_dict['G#']=14
key_dict['A#']=15
key_dict['B#']=16
key_dict['Cb']=20
key_dict['Db']=21
key_dict['Eb']=22
key_dict['Fb']=23
key_dict['Gb']=24
key_dict['Ab']=25
key_dict['Bb']=26
key_dict['chromatic']=7
correct_array = [0]*48
#number_n = ['17']
number_n = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48']
#mid = MidiFile('00027.mid')

def mid_to_audio(midi_file):
    key_dict = {
        "C" : 0,
        "G" : 1,
        "D" : 2,
        "A" : 3,
        "E" : 4,
        "B" : 5,
        "F#" : 6,
        "F" : -1,
        "Bb" : -2,
        "Eb" : -3,
        "Ab" : -4,
        "Db" : -5,
        "chromatic" :7
    }
    flag = False
    if isinstance(midi_file, str):
        mid = MidiFile(midi_file)
    else:
        mid = midi_file
    #print(mid)
    note_array = np.zeros(3)
    #print(mid)
    for i, track in enumerate(mid.tracks):
        if flag == False:
            #print('reached')
            #print('reached')
            #print('Track {}: {}'.format(i, track.name))
            key = 7
            clocks_per_click = 24
            bpm = 120
            for msg in track:
                #print(msg)
                if msg.type == 'key_signature':
                    key = key_dict[msg.key]  
                if msg.type == 'time_signature':
                    clocks_per_click = msg.clocks_per_click
                if msg.type == 'set_tempo':
                    bpm = tempo2bpm(msg.tempo)
                if msg.type == 'note_on' or msg.type =='note_off':
                    note = msg.note
                    #print(note)
                    flag = True
                    if msg.time != 0:
                        #print('reached')
                        if msg.time<60:
                            time=msg.time
                        else:
                            time = int(msg.time/30)
                        #print(time)
                        #print(note)
                        array = np.zeros(time)
                        array = array + note
                        #print(array)
                        note_array = np.append(note_array, array, axis=0)
                        #print(note_array)
    #print(note_array)
    note_array[0]=key
    note_array[1]=clocks_per_click
    note_array[2]=bpm
    #print(note_array)
    return note_array

'''

mid = MidiFile('MIR-QBSH-corpus/midiFile/00043.mid')
for i, track in enumerate(mid.tracks):
    #print('reached')
    #print('Track {}: {}'.format(i, track.name))
    key = 'chromatic'
    clocks_per_click = 24
    bpm = 120
    note_array = np.zeros(1)
    for msg in track:
    #print(msg)
        if msg.type == 'key_signature':
            key = msg.key
        if msg.type == 'time_signature':
            clocks_per_click = msg.clocks_per_click
        if msg.type == 'set_tempo':
            bpm = tempo2bpm(msg.tempo)
        if msg.type == 'note_on':
            note = msg.note
            if msg.time != 0:
                #print('reached')
                time = int(msg.time/60)
                array = np.zeros(time)
                array = array + note
                #print(array)
                note_array = np.append(note_array, array, axis=0)
note_array = note_array[1:len(note_array)-1]
print(note_array)
'''

def dataset_test(correct_array):
    correct = 0
    total = 1
    test = 'MIR-QBSH-corpus/waveFile'
    year = '/year'
    person = '/person000'
    number = '/000'
    wav = '.wav'
    midi = '.mid'
    #year_n = ['8']
    #person_n = ['07']
    #number_n = ['03']
    year_n = ['0','1','2','3','4','5','6','7','8']
    person_n = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35']
    number_n = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48']
    for y in year_n:
        for p in person_n:
            i = 0
            for n in number_n:
                if i != 11 and i != 15 and i != 22 and i !=  25 and i !=  27 and i !=  31 and i !=  37 and i !=  39 and i !=  43 and i !=  45:
                    try:
                        real_tf = correct_array[i]
                        #print(real_tf[0])
                        mid = wavtomid(test+year+y+person+p+number+n+wav,y+p+n,bpm=int(real_tf[2]),key=int(real_tf[0]))
                        #print(mid)
                        test_tf = mid_to_audio(mid)
                        test_tf = test_tf[3:len(test_tf)-3]
                        real_tf = real_tf[3:len(real_tf)-3]
                        #print(test_tf)
                        #print(real_tf)
                        i = i+1
                        for i in range(len(real_tf)):
                            #print('r')
                            if i < len(test_tf):
                                if real_tf[i]==test_tf[i]:
                                    correct = correct+1
                                    total = total +1
                                #print(total)
                                #print(correct)
                                else:
                                    total = total +1
                    except:
                        continue
    accuracy = correct/total
    return accuracy
  

j = 0
for n in number_n:
    #print(n)
    #mid = MidiFile('MIR-QBSH-corpus/midiFile/000'+n+'.mid')
    note_array = mid_to_audio('MIR-QBSH-corpus/midiFile/000'+n+'.mid')
    correct_array[j]=note_array
    j = j+1

#print(correct_array)
print(dataset_test(correct_array))  
