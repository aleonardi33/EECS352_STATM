import numpy as np
import librosa

def p_track(audio,sr,bpm):
    '''
    returns pitches as well as times in which the pitch changes
    '''
    hl = int((sr*24)/bpm)
    raw_pitches = librosa.piptrack(audio,sr,hop_length=hl)
    pitches = quantizeNotes(raw_pitches,"C")
    pitch_change = []
    for pitch in range(len(pitches)):
        if pitches[pitch] != pitches[pitch+1]:
            pitch_change.append(pitch)
    return pitches, pitch_change

def quantizeNotes(inputArr, key):
    scale, midi = getNotesInKeyOf(key)
    quantizedArr = np.zeros(np.shape(inputArr)[0])
    for i,sample in enumerate(inputArr):
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
    midi_output[0] = allMIDINotes[0]
    midi_output[1] = allMIDINotes[2]
    midi_output[2] = allMIDINotes[4]
    midi_output[3] = allMIDINotes[5]
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