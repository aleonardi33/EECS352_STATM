import numpy as np
import sklearn
import librosa

def audio_to_data(audio):
    x,sr = librosa.load("sinesweep_recording.wav")
    pitches, magnitudes = librosa.piptrack(x,sr=sr)
    scaler = sklearn.preprocessing.MinMaxScaler((0,127))
    int_mag = int(scaler.fit(magnitudes))


def findNearestNote(freq,scale):
    noteIndex = np.argmin(np.abs(scale-freq))
    #print(freq)
    return scale[noteIndex]

def getBaseFreq(freq):
    #multiplier = np.zeros(np.shape(freqArr)[0])
    #for i, freq in enumerate(freqArr):
    multiplier = 0
    while(freq>61.73541):
        #freqArr[i] = freqArr[i]/2
        freq = freq/2
        multiplier += 1
    return freq, multiplier