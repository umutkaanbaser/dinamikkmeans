import cv2
from dinamikKmeans import dinamikKmeans
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# k means parametrelerini veriyoruz
#init : baslangic agirlikilari dagilim algoritması secimi
#random_state : rastgelelik referansı
dKnn = dinamikKmeans(goster=True,init="k-means++",random_state=12) 

# verileri dagılımın daha net gozuktugu ve en mantık secimin 3 olacagını gorebilmek icin True yapınız, dinamikKmeans 3 parcaya bolecektir verisetini
kolayVeri = True
if kolayVeri:

    # ornek bir set olusturuyoruz
    X = [[20,30],[25,40],[15,30],[25,35],[20,40],[55,50],[60,70],[50,60],[61,54],[40,70],[55,12]]

    # dagilima bakicaz
    rsm = np.zeros((100,100,3),np.uint8)
    for veri in X:
        cv2.circle(rsm,veri,1,(255,255,255),1,1)

    plt.title("dagilim")
    plt.imshow(rsm)
    plt.show()
else:
    
    veriler = pd.read_csv("veri.csv")
    X = veriler.iloc[:,2:4].values

dKnn.egit(X)
dKnn.tani(X)
