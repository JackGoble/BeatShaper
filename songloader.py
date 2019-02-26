import numpy as np
import librosa
from beatmaploader import *


def chunks(l, n): #Yield successive n-sized chunks from l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def transformsong(y, num_beats, song_secs, chunks_per_beat, verbose=0):
    num_chunks = num_beats * chunks_per_beat #the total number of chunks
    chunk_size = int(len(y) / num_chunks) #how many points there are in a chunk

    assert chunk_size == 300
        
    chunker = chunks(y, int(chunk_size))
    List = [np.abs(np.fft.fft(next(chunker)))[0:int(chunk_size/2)+1] for i in range(int(num_chunks))]

    if verbose == 1:
        print("minutes   :", mins)
        print("num beats :", num_beats)
        print("num chunks:", num_chunks)
        print("chunk size:", chunk_size)
    
    return List
        
def loadsong(audio, beatmap, samples_per_chunk=300, num_chunks_per_slice=65, num_chunks_per_beat=8):
    if audio[len(audio)-4:len(audio)] != ".ogg":
        print("Audio file " + audio + " is not of type .ogg")
        return -1
    
    y, sr = librosa.load(audio)
    
    song_length = librosa.get_duration(y=y,sr=sr) / 60.0
    tempo = np.round(librosa.beat.tempo(y, sr=sr))
    new_sample_rate = (tempo/200)*8000

    y = librosa.resample(y, sr, new_sample_rate)
    
    number_of_beats = int(tempo * song_length)
    
    y = transformsong(y, number_of_beats, song_length, num_chunks_per_beat)
    
    y_bm = loadbeatmap_3dout(beatmap, number_of_beats)

    
    return y, y_bm