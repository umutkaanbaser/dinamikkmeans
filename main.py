import cv2
from dynamicKmeans import dynamicKmeans
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# we are giving kmeans parametres
#init : selection of initial weights distribution algorithm
#random_state : random reference
dKnn = dynamicKmeans(show=True,init="k-means++",random_state=12) 

# Set the data to True to see that the distribution is clearer and the most logical choice will be 3, dynamicKmeans will split the dataset into 3 parts
easySet = True
if easySet:

    # creating example
    X = [[20,30],[25,40],[15,30],[25,35],[20,40],[55,50],[60,70],[50,60],[61,54],[40,70],[55,12]]

    # we will look distribution
    img = np.zeros((100,100,3),np.uint8)
    for data in X:
        cv2.circle(img,data,1,(255,255,255),1,1)

    plt.title("Distribution")
    plt.imshow(img)
    plt.show()
else:
    
    dataSet = pd.read_csv("veri.csv")
    X = dataSet.iloc[:,2:4].values

dKnn.fit(X)
dKnn.predict(X)
