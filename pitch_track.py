import numpy as np
import librosa

def p_track(audio,sr,bpm):
    '''
    returns pitches as well as times in which the pitch changes
    '''
    hl = int((sr*60)/(bpm*24))
    raw_pitches, magnitudes = librosa.piptrack(audio,sr,hop_length=hl)
    #print(raw_pitches)
    melody = getFundFreqs(raw_pitches)
    pitches = quantizeNotes(melody,"C")
    #print(pitches)
    pitch_change = []
    for pitch in range(len(pitches)):
        if pitch != 0:
            if pitches[pitch] != pitches[pitch-1]:
                pitch_change.append(pitch)
    return pitches, pitch_change

def quantizeNotes(inputArr, key):
    scale, midi = getNotesInKeyOf(key)
    quantizedArr = np.zeros(np.shape(inputArr)[0])
    #print(inputArr)
    for i,sample in enumerate(inputArr):
        #print('sample')
        #print(sample)
        lowNote, octave = getBaseFreq(sample)
        note = findNearestNote(lowNote, scale, midi)
        quantizedArr[i] = note + (12*octave)
    return quantizedArr

def getNotesInKeyOf(key):
    allNotes = np.zeros(12)
    allMIDINotes = np.zeros(12)

    allNotes[0] = 32.70320
    allNotes[1] = 34.64783
    allNotes[2] = 36.70810
    allNotes[3] = 38.89087
    allNotes[4] = 41.20344
    allNotes[5] = 43.65353
    allNotes[6] = 46.24930
    allNotes[7] = 48.99943
    allNotes[8] = 51.91309
    allNotes[9] = 55.0
    allNotes[10] = 58.27047
    allNotes[11] = 61.73541

    allMIDINotes[0] = 24
    allMIDINotes[1] = 25
    allMIDINotes[2] = 26
    allMIDINotes[3] = 27
    allMIDINotes[4] = 28
    allMIDINotes[5] = 29
    allMIDINotes[6] = 30
    allMIDINotes[7] = 31
    allMIDINotes[8] = 32
    allMIDINotes[9] = 33
    allMIDINotes[10] = 34
    allMIDINotes[11] = 35
    
    output = np.zeros(7)
    output[0] = allNotes[0]
    output[1] = allNotes[2]
    output[2] = allNotes[4]
    output[3] = allNotes[5]
    output[4] = allNotes[7]
    output[5] = allNotes[9]
    output[6] = allNotes[11]

    midi_output = np.zeros(7)
    midi_output[0] = allMIDINotes[1]
    midi_output[1] = allMIDINotes[2]
    midi_output[2] = allMIDINotes[4]
    midi_output[3] = allMIDINotes[6]
    midi_output[4] = allMIDINotes[7]
    midi_output[5] = allMIDINotes[9]
    midi_output[6] = allMIDINotes[11]
    
    return output, midi_output

def findNearestNote(freq,scale,midi):
    noteIndex = np.argmin(np.abs(scale-freq))
    return midi[noteIndex]

def getBaseFreq(freq):
    #multiplier = np.zeros(np.shape(freqArr)[0])
    #for i, freq in enumerate(freqArr):
    multiplier = 0
    while(freq>61.73541):
        #freqArr[i] = freqArr[i]/2
        freq = freq/2
        multiplier += 1
    return freq, multiplier


def getFundFreqs(pitchesArr):
    fundFreqArr = np.array([])
    transformedPitches = pitchesArr.T

    for ind, time in enumerate(transformedPitches):
        for ind2, freq in enumerate(time):
            if freq>0:
                fundFreqArr = np.append(fundFreqArr,freq)
                break
    return fundFreqArr

def pitch_smoothing(midi_array):
    part_1 = False
    midi_array_np = np.array(midi_array)
    #shape = midi_array_np.shape[0]
    i=0
    while i < midi_array_np.shape[0]:
        #deal with repeating notes
        if i != 0 and i != midi_array_np.shape[0]:
            if midi_array_np[i-1,0]==midi_array_np[i,0] and midi_array_np[i,0] == midi_array_np[i+1,0]:
                #print('reached')
                if midi_array_np[i-1,3] < 10 and midi_array_np[i,3] < 10 and midi_array_np[i+1,3]<10:
                    #print('r1')
                    midi_array_np[i,3]=midi_array_np[i,3]+midi_array_np[i-1,3]+midi_array_np[i+1,3]
                    midi_array_np = np.delete(midi_array_np,i+1,0)
                    midi_array_np = np.delete(midi_array_np,i-1,0)
                else:
                    if midi_array_np[i-1,3] < 10 or midi_array_np[i,3]<10:
                        #print('r2')
                        #print(midi_array_np[i-1,3])
                        midi_array_np[i-1,3]=midi_array_np[i-1,3]+midi_array_np[i,3]
                        #print(midi_array_np[i-1,3])
                        part_1 = True
                    if midi_array_np[i+1,3] < 10 :
                        #print('r3')
                        #print(midi_array_np[i+1,3])
                        midi_array_np[i+1,3]=midi_array_np[i+1,3]+midi_array_np[i,3]
                        #print(midi_array_np[i+1,3])
                        part_1 = True
                    if part_1:
                        #print(midi_array_np.shape[0])
                        midi_array_np = np.delete(midi_array_np,i,0)
                        #print(midi_array_np.shape[0])
                        part_1 = False
        i = i+1
    #deal with short notes 1 - 2 semitones off
    i=0
    while i < midi_array_np.shape[0]-1:
        if i != 0 and i < midi_array_np.shape[0]:
            if 
            if midi_array_np[i-1,0]==midi_array_np[i+1,0] and midi_array_np[i-1,0]!=midi_array_np[i,0]:
                midi_array_np[i-1,3]=midi_array_np[i,3]+midi_array_np[i-1,3]+midi_array_np[i+1,3]
                midi_array_np = np.delete(midi_array_np,i+1,0)
                midi_array_np = np.delete(midi_array_np,i-1,0)
                i = i-1
            else:
                i = i+1
        else:
            i = i+1
    return midi_array_np


            