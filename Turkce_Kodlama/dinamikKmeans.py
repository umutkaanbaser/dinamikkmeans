from sklearn.cluster import KMeans
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import cv2

class dinamikKmeans():
    def __init__(self, maxK:int=10, goster:bool=True, **kmeansArg) -> None:
        """
            aciklama:
            dinamik bir bicimde kmeans'i kullanmayı saglar.
            k degeri vermeyin sadece en fazla kaç tane k degeri alabilir onu verin,
            birakin o veri setini iyi sekilde en iyi grup sayisiyla gruplasin

        
            argumanlar:
            maxK : en fazla kaç adet k degeri alabileceğidir -> wcss grafiginde diresek olusması icin en az 5 veriniz
            goster : yapılan işlemlerin gelistiriciye gosterilip gosterilmeyeceğidir.
            kmeansArg : kmeans için gerekli argumanlar init,random_state gibi sklearn.cluster.KMeans'in argumanlarıdır 
                detayli bilgi için bakınız :  https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html

        """
        self.maxK=maxK  
        self.kmeansArg=kmeansArg # init="k-means++",random_state=123
        self.anaKmeans = None
        self.goster = goster

    def mesafeHesapla(self, n1:tuple, n2:tuple) -> float:
        """
            aciklama:
            2 nokta arasındaki uzaklıgı hesaplamak için kullanılır
            
            argumanlar:
            n1: nokta1
            n2: nokta2
        """
        x1,y1 = n1
        x2,y2 = n2
        mes = (x1-x2)**2 + (y1-y2)**2
        mes = mes**(1/2)
        return mes

    def dereceHesapla(self, n1:tuple, n2:tuple, n3:tuple) -> float:
        """
        aciklama:
        wcss grafiğinde o an ki k degerinin kaç derece açı yaptıgını hesaplamak için kullanılır

        argunmanlar:
        n1:bir onceki k degerinin wcss'deki kordinati
        n2:suanki k degerinin wcss'deki kordinati
        n3:bir sonraki k degerinin wcss'deki kordinati
        
        """
        a = self.mesafeHesapla(n1,n2)
        b = self.mesafeHesapla(n2,n3)
        c = self.mesafeHesapla(n1,n3)
        a,b,c = [int(i) for i in [a,b,c]]
        
        try:
            cos_c = (a**2+b**2-c**2)/(2*a*b)
            derece = np.arccos(cos_c)
            if str(derece) == "nan":
                derece= math.pi
        except ZeroDivisionError:
            derece = math.pi
        if self.goster:
            print("hesaplananlar noktalar:",n1,n2,n3)
            rsm = np.zeros((1000,1000,3),np.uint8)
            cv2.line(rsm,n1,n2,(0,255,0),10)
            cv2.line(rsm,n2,n3,(255,0,0),10)
            cv2.line(rsm,n1,n3,(255,255,255),10)
            plt.figure()
            plt.title(f"beyazi goren aci deg:{derece}")
            plt.imshow(rsm)
            plt.show()
        return derece
    
    def retKmeans(self, dereceler:list, kmeansler:list) -> KMeans:
        """
        aciklama:
        kmeansler arasından en iyi k degerine sahip olanı doner

        argumanlar:
        dereceler : wcss grafiginde k degerlerinin yaptıgı açılar
        kmeanslar : o anki k degeri ile hesaplanan kmeans
        """
        derecelerInd = dereceler.index(min(dereceler))
        return kmeansler[derecelerInd]

    def normalle(self, _sonuclar:list, kat:int=1000) -> list:
        """
        aciklama:
        daha kolay bi şekilde acı hesaplama için butun wcss degerlerini 0 ile 'kat' arasına sıkıştır.

        argumanlar:
        _sonuclar : wcss sonucları
        kat : en buyuk degerin alabileceği sayidir -> buna gore diger degerler normallenir
        """
        sonuclar = _sonuclar.copy()
        maxSonuc = max(sonuclar)
        sonuclar = [int((sonuc/maxSonuc)*kat) for sonuc in sonuclar]
        return sonuclar
    
    def egit(self, X:list) -> None:
        """
        aciklama:
        verilen X veri kümesine göre dinamik kmeans egitimini yapar

        argumanlar:
        X: veri seti
        """
        wcssler = []
        dereceler = []
        kmeansler = []
        bas = time.time()
        for i in range(1,self.maxK):

            kmeans = KMeans(n_clusters=i,**self.kmeansArg)
            kmeans.fit(X)
            wcss = kmeans.inertia_ 
            wcssler.append(wcss)
            kmeansler.append(kmeans)

        kat =1000
        sonuclar = self.normalle(wcssler,kat)
        xAxis = [int(i*kat/10) for i in range(1,len(sonuclar)+1)]

        sonuclar = list(zip(xAxis,sonuclar))

        for i in range(0,len(sonuclar)):    
            derece = self.dereceHesapla(sonuclar[max(0,i-1)],sonuclar[max(1,i)],sonuclar[min(len(sonuclar)-1,i+1)])
            dereceler.append(derece)

        bit = time.time()
        fark = bit-bas
        self.anaKmeans = self.retKmeans(dereceler,kmeansler)
        sonuclar = np.array(sonuclar)[:,0]
        if self.goster:
            plt.figure()
            plt.subplot(1,2,1)
            plt.title("hesap")
            plt.plot(xAxis,sonuclar)
            plt.subplot(1,2,2)
            plt.title(f"hesaplanma suresi:{fark:.2f}, k:{len(self.anaKmeans.cluster_centers_)}")
            plt.plot([i for i in range(1,len(sonuclar)+1)],wcssler)
            plt.show()
    
    def tani(self, X_tani:list) -> list:
        """
        aciklama:
        verilen X_tanidaki verileri tanima işlemine tabii tutar hangi bolge de oldugunu tahmin eder

        argumanlar:
        X_tani : taninacak olan veri listesi
        """
        return self.anaKmeans.predict(X_tani)
        
