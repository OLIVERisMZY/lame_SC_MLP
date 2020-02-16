import math
import pandas as pd
import numpy as np
import random
from sklearn.decomposition import PCA
from sklearn.datasets import make_gaussian_quantiles
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import tensorflow as tf
import glob,os
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


train_data = data[:,0:35]
label=data[:,36]

pca = PCA(n_components=20)
train_data = pca.fit_transform(train_data)



x_train,x_test,y_train,y_test = train_test_split(train_data,label,test_size=0.2,random_state=0)
clf= MLPClassifier(hidden_layer_sizes=[18,18],max_iter=20000,learning_rate='constant', alpha=1e-5, learning_rate_init=0.0001,activation='relu',solver ='adam',verbose=True)
clf.fit(x_train, y_train)
print('模型得分:{:.2f}'.format(clf.score(x_test,y_test)))
