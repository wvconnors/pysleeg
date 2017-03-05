# -*- coding: utf-8 -*-
"""
2/8/17, Will Connors
eegclassy.py - A program to take EDF polysomnography data and phase annotations, format, and create a classifier
"""
import numpy as np
#import pandas
#import io
#import tensorflow as tf 
#import matplotlib as plot



class Eeg:
    '''a class'''
   
    def __init__(self, f_location):
        self.nrecords = 0;
        self.duration = 0.0;
        self.nsignals = 0;
        self.names = [];
        self.samplesperrecord = [];
        self.table = None;
        with open(f_location, encoding='mbcs') as f:
            f.seek(236);
            self.nrecords = int(f.read(8));
            self.duration = float(f.read(8));
            self.nsignals = int(f.read(4));
            
            for x in range(self.nsignals):
                self.names.append(f.read(16).strip());
            f.read(200 * self.nsignals);

            for x in range(self.nsignals):
                self.samplesperrecord.append(int(f.read(8)));
            f.read(32 * self.nsignals);
            self.table = np.zeros((self.nsignals, self.nrecords * max(self.samplesperrecord)), dtype=np.int);
            for record in range(self.nrecords):
                for signal in range(self.nsignals):
                    for datum in range(self.samplesperrecord[signal]):
                        self.table[signal,(datum+record*self.samplesperrecord[signal])] = hex2compl(int(f.read(1), 16) * 10000 + int(f.read(1), 16), 16);
        print('done! whew');
            
        #pandas.read_table(f_location, delim_whitespace = True,  )

        
    def process(self):
        return self.nrecords
#        dadada;
#        
#    def crossval(self):
#        dadada;
#        
#    def export(self):
#        dadada;
#        
def hex2compl(x, n):
    if x > pow(2, n) / 2:
        x = x - (1 << n)
    return x

if __name__ == '__main__':
    ## run class object sequence
    import sys
    engine = Eeg(sys.argv[1]);
    print('Exit');
        
    