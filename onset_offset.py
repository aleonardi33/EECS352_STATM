import numpy as np
import librosa
from stft import stft
import scipy as sp

def onset(audio, sr, bpm,length):
    '''
    Returns onset times already modified for MIDI time
    
    hl = int((sr*60)/(bpm*24))
    onset_list = librosa.onset.onset_detect(audio, sr = sr, hop_length = hl)
    index = 0
    while index < len(onset_list):
        if onset_list[index] > length:
            onset_list = onset_list[0:index]
            break
        else:
            index = index + 1
            
    '''
    hop_size = int((sr*60)/(bpm*48))
    window_size = hop_size*2
    window = sp.signal.windows.hann(window_size, sym=False)
    threshold = .1
    last_value = 0
    last_onset = -1
    onset_list = []

    length_to_cover_with_hops = len(audio) - window_size
    assert (length_to_cover_with_hops >= 0), "window_size cannot be longer than the signal to be windowed"
    #num_hops = int(1 + np.floor(length_to_cover_with_hops/hop_size))
    num_hops = length
    for hop in range(num_hops):
        start = hop*hop_size
        end = start + window_size
        unwindowed_sound = audio[start:end]
        windowed_sound =  unwindowed_sound * window
        rms = np.sqrt(np.mean(windowed_sound**2))
        #print(hop)
        #print(last_value/rms)
        try:
            if (last_value/rms) < threshold:
                if last_onset is not (hop - 1):
                    onset_list.append(hop)
                    last_onset = hop
                else:
                    last_onset = hop
        except:
            last_onset = hop
        last_value = rms
    
    #print(onset_list)
    return onset_list

def offset (audio, sr, bpm,length):
    '''
    Returns the offset times already modified for MIDI time
    '''
    hop_size = int((sr*60)/(bpm*24))
    window_size = hop_size*2
    window = sp.signal.windows.hann(window_size, sym=False)
    threshold = .005

    offset_list = []

    length_to_cover_with_hops = len(audio) - window_size
    assert (length_to_cover_with_hops >= 0), "window_size cannot be longer than the signal to be windowed"
    #num_hops = int(1 + np.floor(length_to_cover_with_hops/hop_size))
    num_hops = length
    last_offset = -1
    #print(num_hops)
    for hop in range(num_hops-1):
        start = hop*hop_size
        end = start + window_size
        #print(start)
        #print(end)
        unwindowed_sound = audio[start:end]
        if len(unwindowed_sound)!=len(window):
            zeros = np.zeros(len(window)-len(unwindowed_sound))
            unwindowed_sound = np.append(unwindowed_sound, zeros,0)
        windowed_sound =  unwindowed_sound * window
        print(np.sqrt(np.mean(windowed_sound**2)))
        if np.sqrt(np.mean(windowed_sound**2)) < threshold:
            #print(np.sqrt(np.mean(windowed_sound**2)))
            print(hop)
            if last_offset is not (hop - 1) and last_offset is not (hop-2):
                offset_list.append(hop)
                last_offset = hop
            else:
                last_offset = hop
    return offset_list