# -*- coding: utf-8 -*-
"""Car_sales_prediction.ipynb
Automatically generated by Colaboratory.
"""

#read in data
import pandas as pd
import numpy as np
carSales = pd.read_csv("car_sales.csv")

#carSales.head()

from sklearn.model_selection import train_test_split

#drop "Sale"
X = carSales.drop("Sale",axis=1)
y = carSales["Sale"]

#X.head()

#y.head()

#split data to 80% for training and 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#import keras
import keras
#import sequential module to initializa the artificial neural network
from keras.models import Sequential
#import dense module to add layers to deep learning model
from keras.layers import Dense

#define sequential model with 3 layers
model = keras.Sequential(
    [
    Dense(16, activation = 'relu', input_dim=5,kernel_initializer = 'normal', name = 'layer_1'),
    Dense(5, activation = 'relu',kernel_initializer = 'normal', name = 'layer_2'),  
    Dense(1, activation = 'relu',kernel_initializer = 'normal', name = 'layer_3'),
     ]
)

#model.summary()

#optmization
opt = keras.optimizers.Adam(learning_rate = 0.05) 
model.compile(optimizer = opt, loss = 'mae')

#fit train data to model
model.fit(X_train, y_train, batch_size = 32, epochs = 140)

#make prediction
y_prediction = model.predict(X_test)

from sklearn.metrics import mean_absolute_error

print(mean_absolute_error(y_test, y_prediction))
