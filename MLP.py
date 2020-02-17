import math
import random
import copy
import xlrd
import math
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,Dropout
import matplotlib.pyplot as plt
import  pandas as pd
from sklearn import preprocessing
import tensorflow as tf
import glob,os
import keras
import csv
input=[]
path = r'E:\new_ai\输入\input'+str(101)+'.csv'
with open(path,encoding = 'utf-8') as f:
     data = np.loadtxt(f,int,delimiter = ",")


for i in range(101,201):
  path = r'E:\new_ai\输入\input'+str(i)+'.csv'
  with open(path,encoding = 'utf-8') as f:
     da = np.loadtxt(f,int,delimiter = ",")
     data=np.vstack((data,da ))

label=keras.utils.to_categorical(data[:,36])
data=data[:,0:35]
msk=np.random.rand(len(data))<0.8
train_data=data[msk]
test_data=data[~msk]
train_label=label[msk]
test_label=label[~msk]
print(test_label)

minmax_scale = preprocessing.MinMaxScaler(feature_range=(0, 1))
train_data = minmax_scale.fit_transform(train_data)
test_data = minmax_scale.fit_transform(test_data)
print(np.shape(train_data))
print(np.shape(train_label))

model=Sequential()
model.add(Dense(units=30,input_dim=35,kernel_initializer='uniform',activation='relu'))
model.add(Dense(units=30,kernel_initializer='uniform',activation='relu'))
model.add(Dense(units=30,kernel_initializer='uniform',activation='relu'))
model.add(Dense(units=20,kernel_initializer='uniform',activation='softmax'))
model.compile(loss='categorical_crossentropy',optimizer='sgd',metrics=['accuracy'])
train_history=model.fit(x=train_data,y=train_label,validation_split=0.2,epochs=2000,batch_size=1000,verbose=2)

def show_train_history(train_history,train,validation):
    plt.plot(train_history.history[train])
    plt.plot(train_history.history[validation])
    plt.title('Train history')
    plt.ylabel(train)
    plt.xlabel('epoch')
    plt.legend(['train','validation'],loc='upper left')
    plt.show()



scores=model.evaluate(x=test_data,y=test_label)
print('最终得分为：'+str(scores[1]))
show_train_history(train_history,'val_acc')
all_probability=model.predict(train_data)
print(all_probability[0])
