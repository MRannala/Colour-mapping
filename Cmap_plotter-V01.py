# -*- coding: utf-8 -*-
"""
Created on Sat May 06 22:04:55 2017

@author: J.M.Rannala
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd
import os

# log or linear?

# x,y,cbar labels
#X-label = 
#Y-label =
#cbar_label = 


def get_files(filetype):
    ''' Obtain a list of files ending in the desired specified extension '''
     
    # list of files to cycle over
    filelist = []

    # Get current working directory (cwd)
    cwd = os.getcwd()
    
    # Add all files ending in filetype (.msht) to filelist
    for file in os.listdir(cwd):
        if file.endswith(filetype):
            filelist.append(file)
    
    return filelist

def get_array(filename):
    ''' import data from file into an array of lines '''
    
    data = []

    # open file to read
    afile = open(filename, 'r')
    
    # Append each line to an array element
    for line in afile:
        data.append(line)
    
    # close file
    afile.close()
    
    return data
    
def get_df(data, start_ind):

    datarray = []
    inds = []
    
    # start at first line of numbers
    i = start_ind
   
    #do until blank line
    while data[i] != '\n':
        
        linetext = data[i].split()
        datarray.append(linetext)
        
        i = i + 1
    
    # make first row column lables
    cols = datarray[0]
    #remove first row of array
    datarray = datarray[1:]   
        
    for j in range(len(datarray)):
        
        # make first value of each line index value
        inds.append(datarray[j][0])
        # remove value from array
        datarray[j] = datarray[j][1:]

    df = pd.DataFrame(datarray, columns=cols, index=inds)

    return df

def make_cmap(df, chartname):
    
    X=df.columns.values
    Y=df.index.values
    Z=df.values
    x,y=np.meshgrid(X, Y)
    # log cmap
    pic = plt.contourf(x, y, Z,cmp='hot', norm = LogNorm())
    # add axis labels
    pic.ax.set_xlabel('Dimensions [cm]')
    pic.ax.set_ylabel('Dimensions [cm]')
    clb = plt.colorbar()
    clb.ax.set_title('µSv/h')
    
    # Reduces white spaces around cbar.
    plt.savefig(chartname, bbox_inches='tight')
    
    # closes plot window to ensure c bar reset each plot.
    plt.close()
    
def count_Ntally(datarray):
    
    Ntallies = 0
    tally_numbers = []
    tally_cord = []
    tally_index = []

    for i in range(len(datarray)):
        linetext = datarray[i].split(' ')
        
        # if line of file is long enough to be Mesh tally number, it is checked
        if len(linetext) > 3 :
            if linetext[0] + linetext[1] + linetext[2] + linetext[3] == 'MeshTallyNumber':
                Ntallies += 1
                tally_numbers.append(linetext[-1].rstrip('\n'))
                tc , ti = find_cord_data(datarray,i)               
                tally_cord.append(tc)
                tally_index.append(ti)
    
    return Ntallies, tally_numbers, tally_index, tally_cord
    
def find_cord_data(data, start):
       
    escp = False
    counter = start

    # Maximum 1mil lines without success
    while escp == False and counter < 1000000:
        
        linetext = data[counter].split()
        if len(linetext) > 2:
            if linetext[0] + linetext[1] == 'TallyResults:':
                cords = linetext[2] + linetext[5]
                tal_ind = counter + 1
                escp = True
        counter = counter + 1

    return  cords, tal_ind
# ============================================================================
if __name__ == "__main__":
    
    #get list of files
    filelist = get_files('.msht')
       
    for files in filelist:
        data = get_array(files)
        Ntal, tally_num, tall_ind, tally_cord = count_Ntally(data)
        
        if Ntal == 0:
            print('No tallies found in {0}'.format(files))
            
        elif Ntal > 0:
            
            #
            for i in range(Ntal):
                
                #tally_num[i], tall_ind[i], tally_cord
                df = get_df(data, tall_ind[i])  
                
                o_name = files.split('.')[0] + '-T' + tally_num[i] + '-' + tally_cord[i] + '.png'
                               
                make_cmap(df, o_name)
                

       
        