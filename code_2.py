#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 21:39:46 2018

@author: Jessica Saini Hardika Goyal
"""

# Importing the libraries
import pip
pip.main(["install","numpy"])
pip.main(["install","matplotlib"])
pip.main(["install","scipy"])
pip.main(["install","pandas"])
import sys
#sys.path.insert(0,"/Users/jessicasaini/Library/Python/2.7/lib/python/site-packages")
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import keras


dataset = pd.read_csv('data.csv')
X = dataset.iloc[:, 1:179].values
y = dataset.iloc[:, 179:].values

for i in range(len(y)):
    if y[i] == 1:
        y[i] = 1
    else:
        y[i] = 0



# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


#Making the ANN

#Importing keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense

#Initializing the ANN
classifier = Sequential()

#Adding input layer and first hidden layer
classifier.add(Dense(output_dim = 80, init = 'uniform', activation = 'relu', input_dim = 178))

#Adding second hidden layer
classifier.add(Dense(output_dim = 80, init = 'uniform', activation = 'relu'))

#Adding the output layer
classifier.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid'))

#Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

#Fitting the ANN to the training set
classifier.fit(X_train, y_train, batch_size = 10, epochs = 100)

# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

#--------_Addition in the code----
# K Fold Validation 
from sklearn.model_selection import StratifiedKFold
seed = 7
np.random.seed(seed)
kfold = StratifiedKFold(n_splits = 5, shuffle = True, random_state = seed)
cvscores = []
for train, test in kfold.split(X, y):
    # Create model
	model = Sequential()
	model.add(Dense(output_dim = 80, init = 'uniform', activation = 'relu', input_dim = 178))
	model.add(Dense(output_dim = 80, init = 'uniform', activation = 'relu'))
	model.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid'))
	# Compile model
	model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
	# Fit the model
	history=model.fit(X_train, y_train, validation_split=0.33,epochs=15, batch_size=10, verbose=0)
	# Evaluate the model
	scores = model.evaluate(X_test, y_test, verbose=0)
	print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
	cvscores.append(scores[1] * 100)
print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
print("The cvscores are:",cvscores)
print("The history is: ")
print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
'''plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()'''

