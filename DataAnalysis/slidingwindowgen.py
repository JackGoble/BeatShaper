import numpy as np

def sliding_window_gen(l, ncps, samples_per_chunk=300): #parameters: the list of numpy arrays, and the # of chunks per slice
    for i in range(int(ncps/2)): #pad both sides of the input list with numpy arrays of zeros 
        np.concatenate(np.zeros(int(samples_per_chunk/2)+1), l)
        np.concatenate(np.zeros(l, int(samples_per_chunk/2)+1))
    for j in range(len(l)):
        yield np.concatenate(l[j:j+ncps])
        
def windowify(l, ncps, samples_per_chunk=300):
    window_generator = sliding_window_gen(l, ncps)

    current_window = np.zeros(shape=(len(l), int(((samples_per_chunk/2)+1)*ncps)))
    
    for i in range(number_of_chunks):
        current_window[i] = next(window_generator)