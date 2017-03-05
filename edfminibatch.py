# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:37:06 2017

@author: Will
"""
import numpy as np
import pyedflib
import sys
from pathlib import Path
from sklearn.externals import joblib
import sklearn.linear_model.SGDClassifier
import sklearn.preprocessing
import sklearn.cross_validation
import sklearn.metrics
import xml.etree.ElementTree as ET

#fname = r"c:\users\will\cfs\polysomnography\edfs\cfs-visit5-800011.edf"
fname = sys.argv[1];
#answername = r"C:\Users\Will\cfs\polysomnography\annotations-events-profusion\cfs-visit5-800011-profusion.xml"
answername = sys.argv[2];
classypath = Path("savedclassy.pkl");
datanump = [];


#poly edf parsing
with pyedflib.EdfReader(fname) as f:
    nepochs = round(f.getFileDuration()/30.0);
    record = [];
    for channel in range(4):
        step_size = 30 * f.getSampleFrequency(channel);
        dump = f.readSignal(channel);
        series = [];
        for step in range(nepochs-1):
            series.append(dump[step*step_size : (step+1)*step_size]);
        series.append(dump[-step_size:]);
        record.append(series);
    datanump = np.asanyarray(record, dtype=np.float16);

#poly annotations parsing
answertree = ET.parse(answername);
root = answertree.getroot();
stages = [];
offsetstages = [0];
for epoch in root.findall('.//SleepStage'):
    stages.append(int(epoch.text));
offsetstages = offsetstages.append(stages[:-1]);
stages = np.asarray(stages);
offsetstages = np.asarray(offsetstages);


#final array processing
datanump = datanump.transpose((1,0,2));
datanump = np.reshape(datanump, (len(datanump[0]),-1));
enc = sklearn.preprocessing.OneHotEncoder(sparse=False, n_values=5);
offsetstages = enc.fit_transform(offsetstages);

datanump = np.concatenate((datanump, offsetstages), axis=1);


#Machine Learning

if not classypath.is_file():
    clf = sklearn.SGDClassifier(class_weight = 'balanced');
    scaler = sklearn.preprocessing.StandardScaler();
else:
    clf = joblib.load(classypath);
    scaler = joblib.load("savedscaler.pkl");

scaler.partial_fit(datanump);    
datanump = scaler.transform(datanump);
clf.partial_fit(datanump, stages);


print(clf.score(datanump[-100:], stages[-100:]));

joblib.dump(clf, 'savedclassy.pkl');
joblib.dump(scaler, 'savedscaler.pkl');


""" #Performance evaluation
scores = sklearn.cross_validation.cross_val_score(clf, X_train, y_train, cv = 8);
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2));
predicted = sklearn.cross_validation.cross_val_predict(clf, X_train, y_train, cv = 10);
sklearn.metrics.accuracy_score(y_train, predicted);
clf.fit(X_train, y_train);
tested = clf.score(X_test, y_test);
tested2 = clf.predict(X_test);
print(sklearn.metrics.confusion_matrix(y_test, tested2));
testedconf = clf.decision_function(X_test);
print(clf.get_params());
print(sklearn.metrics.classification_report(y_test, tested2))

"""
