import numpy as np
import librosa
from stft import stft
import scipy as sp

def onset(audio, sr, bpm):
    '''
    Returns onset times already modified for MIDI time
    '''
    hl = int((sr*32)/bpm)
    #y = stft(audio,(hl*2),hl,window_type = 'hann')
    #hop size should be samples*32/bpm=hop size
    onset = librosa.onset.onset_detect(audio, sr = sr, hop_length = hl)
    return onset

def offset (audio, sr, bpm):
    '''
    Returns the offset times already modified for MIDI time
    '''
    hop_size = int((sr*32)/bpm)
    window_size = hop_size*2
    window = sp.signal.windows.hann(window_size, sym=False)
    threshold = 1

    offset_list = []

    length_to_cover_with_hops = len(audio) - window_size
    assert (length_to_cover_with_hops >= 0), "window_size cannot be longer than the signal to be windowed"
    num_hops = int(1 + np.floor(length_to_cover_with_hops/hop_size))

    for hop in range(num_hops):
        start = hop*hop_size
        end = start + window_size
        unwindowed_sound = audio[start:end]
        windowed_sound =  unwindowed_sound * window
        if np.sqrt(np.mean(windowed_sound**2)) < threshold:
            offset_list.append(hop)
    return offset_list