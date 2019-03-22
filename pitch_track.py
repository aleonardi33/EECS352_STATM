import numpy as np
import librosa
import statistics

def p_track(audio,sr,bpm,key):
    '''
    returns pitches as well as times in which the pitch changes
    '''
    #bpm = 130
    hl = int((sr*60)/(bpm*24))
    raw_pitches, magnitudes = librosa.piptrack(audio,sr,hop_length=hl)
    #print(raw_pitches)
    melody = getFundFreqs(raw_pitches)
    unclean = quantizeNotes(melody,key)
    pitches = clean_input(unclean)
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
    
    if key == 7:
        return allNotes, allMIDINotes
    
    output = np.zeros(7)
    output[0] = allNotes[0]
    output[1] = allNotes[2]
    output[2] = allNotes[4]
    output[3] = allNotes[5]
    output[4] = allNotes[7]
    output[5] = allNotes[9]
    output[6] = allNotes[11]

    midi_output = np.zeros(7)
    midi_output[0] = allMIDINotes[0]
    midi_output[1] = allMIDINotes[2]
    midi_output[2] = allMIDINotes[4]
    midi_output[3] = allMIDINotes[5]
    midi_output[4] = allMIDINotes[7]
    midi_output[5] = allMIDINotes[9]
    midi_output[6] = allMIDINotes[11]
    
    notesArr = np.array([0,2,4,5,7,9,11])
    keyDict = {
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
        "chromatic":7
    }
    if key == 7:
        return allNotes, allMIDINotes
    key = keyDict[key]
    accidentals = key
    if accidentals >= 0:
        if accidentals > 0:
            notesArr[3] += 1
        if accidentals > 1:
            notesArr[0] += 1
        if accidentals > 2:
            notesArr[4] += 1
        if accidentals > 3:
            notesArr[1] += 1
        if accidentals > 3:
            notesArr[5] += 1
        if accidentals > 4:
            notesArr[2] += 1
    if accidentals < 0:
        if accidentals < 0:
            notesArr[6] -= 1
        if accidentals < -1:
            notesArr[2] -= 1
        if accidentals < -2:
            notesArr[5] -= 1
        if accidentals < -3:
            notesArr[1] -= 1
        if accidentals < -4:
            notesArr[4] -= 1
        
    for i, note in enumerate(notesArr):
        output[i] = allNotes[note]
        midi_output[i] = allMIDINotes[note]
        
    
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
            if midi_array_np[i-1,0]==midi_array_np[i+1,0] and midi_array_np[i-1,0]!=midi_array_np[i,0]:
                if midi_array_np[i,3]<4:
                    midi_array_np[i-1,3]=midi_array_np[i,3]+midi_array_np[i-1,3]+midi_array_np[i+1,3]
                    midi_array_np = np.delete(midi_array_np,i+1,0)
                    midi_array_np = np.delete(midi_array_np,i,0)
                    i = i-1
                else:
                    i = i+1
            else:
                i = i+1
        else:
            i = i+1
    i = 0
    '''
    #if long string of unreasonably short notes take their mode and if two modes use first note
    while i < midi_array_np.shape[0]-1:
        note_list = []
        time = 0
        priority_note = 0
        delete_n = 1
        if midi_array_np[i,3]<3:
            #print('r1')
            j = i +1
            time = midi_array_np[i,3]
            note_list.append(midi_array_np[i,0])
            priority_note = midi_array_np[i,0]
            while j < midi_array_np.shape[0]-1:
                #print('r2')
                if midi_array_np[j,3]<3:
                    time = midi_array_np[j,3]+time
                    note_list.append(midi_array_np[j,0])
                    j = j+1
                    delete_n = delete_n +1
                else:
                    break
            midi_array_np = np.delete(midi_array_np,[i+1,i+delete_n],0)
            try:
                note = statistics.mode(note_list)
            except:
                note = priority_note
            midi_array_np[i,0]=note
            midi_array_np[i,3] = time  
        i = i+1
    '''
    return midi_array_np

def clean_input(quantizedD):
    lastNote = 70
        
    for i,currNote in enumerate(quantizedD):
        if i<(np.size(quantizedD)-1) and lastNote != currNote and currNote != quantizedD[i+1]:
            isMinNoteLen = True
        else:
            isMinNoteLen = False
        if currNote<25 or currNote > 90 or isMinNoteLen:
            quantizedD[i]=lastNote
        else:
            lastNote=currNote
    return quantizedD


            