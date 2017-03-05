# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 13:19:29 2017

@author: Will
"""

import numpy as np
import sklearn.linear_model.SGDClassifier
import sklearn.preprocessing
from sklearn.externals import joblib
import pyedflib
import sys

scaler = joblib.load(place);
classy = joblib.load(alsoplace);

#receive data
raweeg = np.loadtxt("writed.csv");
##TODO read in previous value!

#format
readyeeg = scaler.transform(raweeg);

#classify
classed = classy.predict(readyeeg);

#switch case sonic pi
if classed == '0':
    #do something
elif classed == '1':
    #something else


#close down, save previous value!