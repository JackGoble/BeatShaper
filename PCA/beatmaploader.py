import json
import numpy as np
from sympy import *
init_printing(use_latex=True)
import scipy.spatial.distance as ssd
from pprint import pprint

def loadbeatmap_2dout(beatmap, num_beats, num_chunks_per_beat=8):
    if beatmap[len(beatmap)-5:len(beatmap)] != ".json":
        print("Beatmap file " + audio + " is not of type .json")
        return -1
    
    with open(beatmap) as f:
        data = json.load(f)
  
    notes = "_notes"
    time = "_time"
    line_index = "_lineIndex" #column number
    line_layer = "_lineLayer" #row number
    note_color = "_type" #0 is one color and 1 is the other
    cut_direction = "_cutDirection"#9 cut directions

    num_rows = num_beats * num_chunks_per_beat
    
    # number of rows and columns in the playfield
    # number of cells in the playfield (each cell can hold at most 1 note)
    playfield_rows = 3
    playfield_cols = 4
    playfield_cell_count = playfield_rows * playfield_cols
    
    # number of colors (2): red, blue (order unknown)
    # number of directions notes can face (9): 
    # up, down, left, right, up-left, up-right, down-left, down-right, dot (order unknown)
    note_color_count = 2
    note_direction_count = 9
    
    # number of columns required for a '1-hot' representation of a single time unit (chunk)
    num_cols = playfield_cell_count * (note_color_count + note_direction_count) 
    
    outMatrix = np.zeros(shape=(num_rows,num_cols))    

    # for every note in the beatmap, set the color and direction bits for the proper cell to 1
    # cell_start_index = line_layer * (note_color_count + note_direction_count) + line_index
    # color bit = cell_index + note_color
    # direction bit = cell_index + note_color_count + cut_direction
    for n in range(len(data[notes])):
        row = int(np.round(data[notes][n][time]*num_chunks_per_beat)) #convert time to row index by rounding to nearest 1/8 beat
        if data[notes][n][note_color] < 2:
            cell_start_index = data[notes][n][line_layer] * (note_color_count + note_direction_count) + data[notes][n][line_index]
            outMatrix[row][cell_start_index + data[notes][n][note_color]] = 1
            outMatrix[row][cell_start_index + data[notes][n][cut_direction]] = 1

    return outMatrix, num_cols


def loadbeatmap_3dout(beatmap, num_beats, num_chunks_per_beat=8):
    if beatmap[len(beatmap)-5:len(beatmap)] != ".json":
        print("Beatmap file " + audio + " is not of type .json")
        return -1
    
    with open(beatmap) as f:
        data = json.load(f)
  
    notes = "_notes"
    time = "_time"
    line_index = "_lineIndex" #column number
    line_layer = "_lineLayer" #row number
    note_color = "_type" #0 is one color and 1 is the other
    cut_direction = "_cutDirection"#9 cut directions

    dim_0 = num_beats * num_chunks_per_beat
    
    # number of rows and columns in the playfield
    # number of cells in the playfield (each cell can hold at most 1 note)
    playfield_rows = 3
    playfield_cols = 4
    playfield_cell_count = playfield_rows * playfield_cols
    
    # number of colors (2): red, blue (order unknown)
    # number of directions notes can face (9): 
    # up, down, left, right, up-left, up-right, down-left, down-right, dot (order unknown)
    note_color_count = 2
    note_direction_count = 9
    
    # dimensions for a 'one-hot' representation of a single time unit (chunk)
    dim_1 = playfield_cell_count 
    dim_2 = (note_color_count + 1) + note_direction_count
    
    # initialize matrix to zeros, then set the "no note" bit for each block at each timestep to 1
    outMatrix = np.zeros(shape=(dim_0, dim_1, dim_2, dim_3))
    for n in range(dim_0):
        for m in range(dim_1):
            for o in range(dim_2):
                outMatrix[n][m][o][0] = 1

    # for every note in the beatmap, set the color and direction bits for the proper cell to 1
    for n in range(len(data[notes])):
        entry = int(np.round(data[notes][n][time]*num_chunks_per_beat)) #convert time to row index by rounding to nearest 1/8 beat
        if data[notes][n][note_color] < 2:
            cell_index = (data[notes][n][line_layer] * playfield_cols) + data[notes][n][line_index]
            outMatrix[entry][cell_index][data[notes][n][note_color]+1] = 1
            outMatrix[entry][cell_index][0] = 0
            outMatrix[entry][cell_index][data[notes][n][cut_direction]+3] = 1

    return outMatrix