from sklearn.cluster import KMeans
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import cv2

class dynamicKmeans():
    def __init__(self, maxK:int=10, show:bool=True, **kmeansArg) -> None:
        """
            Description:
            It allows to use kmeans in a dynamic way.
            Don't give the k value, just give the maximum how many k values ​​it can take,
            let it group that dataset well with the best number of groups
        
            Args:
            maxK : is how many k values ​​it can take at most -> give at least 5 to create an elbow on the wcss chart
            show : whether the transactions made will be shown to the developer.
            kmeansArg : Required arguments for kmeans are those of sklearn.cluster.KMeans like init,random_state
                see for detailed information:  https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html

        """
        self.maxK=maxK  
        self.kmeansArg=kmeansArg # init="k-means++",random_state=123
        self.mainKmeans = None
        self.show = show

    def calculateDistance(self, n1:tuple, n2:tuple) -> float:
        """
            Description:
            Used to calculate the distance between 2 points
            
            Args:
            n1: point 1
            n2: point 2
        """
        x1,y1 = n1
        x2,y2 = n2
        dis = (x1-x2)**2 + (y1-y2)**2
        dis = dis**(1/2)
        return dis

    def calculateDegree(self, n1:tuple, n2:tuple, n3:tuple) -> float:
        """
        Description:
        It is used to calculate how many degrees angle the current k value makes in the wcss graph.

        Args:
        n1 : coordinate of previous k value in wcss
        n2 : coordinate of the current value of k in wcss
        n3 : coordinate of next k value in wcss
        
        """
        a = self.calculateDistance(n1,n2)
        b = self.calculateDistance(n2,n3)
        c = self.calculateDistance(n1,n3)
        a,b,c = [int(i) for i in [a,b,c]]
        
        try:
            cos_c = (a**2+b**2-c**2)/(2*a*b)
            degree = np.arccos(cos_c)
            if str(degree) == "nan":
                degree= math.pi
        except ZeroDivisionError:
            degree = math.pi
        if self.show:
            print("calculated points:",n1,n2,n3)
            img = np.zeros((1000,1000,3),np.uint8)
            cv2.line(img,n1,n2,(0,255,0),10)
            cv2.line(img,n2,n3,(255,0,0),10)
            cv2.line(img,n1,n3,(255,255,255),10)
            plt.figure()
            plt.title(f"white-seeing degree:{degree}")
            plt.imshow(img)
            plt.show()
        return degree
    
    def retKmeans(self, degress:list, kmeanses:list) -> KMeans:
        """
        Description:
        return the kmeans, the one with the best k value is donated.

        Args:
        degress : Degree made by k values ​​in wcss chart
        kmeanses : kmeanses calculated with the current value of k
        """
        degressInd = degress.index(min(degress))
        return kmeanses[degressInd]

    def doNormalization(self, _returnes:list, times:int=1000) -> list:
        """
        Description:
        Compress all wcss values ​​between 0 and 'floor' for an easier degree calculation.

        Args:
        _returnes : wcss results
        times : is the number that the largest value can take -> accordingly other values ​​are normalized
        """
        returnes = _returnes.copy()
        maxReturn = max(returnes)
        returnes = [int((_return/maxReturn)*times) for _return in returnes]
        return returnes
    
    def fit(self, X:list) -> None:
        """
        Description:
        performs dynamic kmeans training based on the given X dataset

        Args:
        X: dataset
        """
        wscces = []
        degress = []
        kmeanses = []
        start = time.time()
        for i in range(1,self.maxK):

            kmeans = KMeans(n_clusters=i,**self.kmeansArg)
            kmeans.fit(X)
            wcss = kmeans.inertia_ 
            wscces.append(wcss)
            kmeanses.append(kmeans)

        times = 1000
        returnes = self.doNormalization(wscces,times)
        xAxis = [int(i*times/10) for i in range(1,len(returnes)+1)]

        returnes = list(zip(xAxis,returnes))

        for i in range(0,len(returnes)):    
            degree = self.calculateDegree(returnes[max(0,i-1)],returnes[max(1,i)],returnes[min(len(returnes)-1,i+1)])
            degress.append(degree)

        stop = time.time()
        diss = stop-start
        self.mainKmeans = self.retKmeans(degress,kmeanses)
        returnes = np.array(returnes)[:,0]
        if self.show:
            plt.figure()
            plt.subplot(1,2,1)
            plt.title("plot for calculate")
            plt.plot(xAxis,returnes)
            plt.subplot(1,2,2)
            plt.title(f"calculation time:{diss:.2f}, k:{len(self.mainKmeans.cluster_centers_)}")
            plt.plot([i for i in range(1,len(returnes)+1)],wscces)
            plt.show()
    
    def predict(self, X_pred:list) -> list:
        """
        Description:
        It recognizes the data in the given X_pred and estimates which region it is in.

        Args:
        X_pred : dataset for prediction
        """
        return self.mainKmeans.predict(X_pred)
        
