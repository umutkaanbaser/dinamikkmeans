# Dinamik Kmeans | Dynamic Kmeans
   Merhaba arkadaşlar, bu dökümanda bir kümeleme algoritması olan k-means algoritmasında kaç kümeye ayrışacağını belirttiğimiz K parametresini dinamik yaparak kaç küme ayrılacağını kendisi karar vermesini sağladık. :)
   
   Hello friends, In this document, we have made the K parameter, which we specified in the k-means algorithm, which is a clustering algorithm, dynamically, to 
decide how many clusters will be separated.

# Nasıl Çalışır ? | How does is work ?

* Asağıda gördüğünüz örnek bir veri seti vardır. Bu dağılıma baktığımızda veri setinin kolayca 3 küme halinde değerlendirebileceğimizi görebilmekteyiz. Beraberinde aynı
işlemi kmeans'i bir döngüye alıp wcss (Küme İçi Kare Toplamı | Within-Cluster Sum of Square) değerleri grafiğinde kırılıma bakarakta yorumlayabilmekteyiz. Peki  verileri
inceleyemeceğimiz yada wcss değerlerini görerek yorumlayamayacğımız; uygulamaların arka planları, web sunucuları, görüntüde nesne ayrıştırma işlemleri gibi yerlerde kaç
k değeri olacağını söyleyemeyiz. Bu tarz durumlarda k-means en iyi şekilde kaç adet k değeri alacağına kendisi karar vermelidir. Statik değil dinamik çalışmalıdır.

   
* There is an example data set you see below. When we look at this distribution, we can see that we can easily evaluate the data set in 3 clusters.
along with the same We can interpret the process by looping kmeans and looking at the breakdown in the wcss (Within-Cluster Sum of Square) values graph. Well the
data that we cannot examine or interpret by seeing the wcss values; in places such as backgrounds of applications, web servers, object parsing processes in the 
image We cannot say that there will be a value of k. In such cases, k-means must decide for itself how many k-values ​​it will best take. It should work 
dynamically, not statically.

<div style="display:flex;">
<img src="https://raw.githubusercontent.com/umutkaanbaser/dinamikkmeans/main/resimler/Dagilim.PNG" width="250" title="veri seti dağılımı"/>
<img src="https://raw.githubusercontent.com/umutkaanbaser/dinamikkmeans/main/resimler/dagilimKume.png" width="250" title="veri seti dağılımı kümelenmesi"/>
</div>

* K-means'i biz yorumlarken wcss değerlerine bakıyorduk ve dirsekleşme, kırılım olduğu noktanın en iyi K değeri olduğunu söylüyorduk. Algoritma da tam olarak bunu 
yapmakta. Wcss değerler grafiği aslında bir x,y düzlemidir. X düzlemindeki k değeri Y düzlemindeki wcss değerine karşılık gelmektedir. Bu noktada kırılım dediğimiz şey 
aslında düzemlede kırılan k'nın, bir önceki k ve bir sonraki k ile yaptığı açıdır. Bu açıların en küçüğü kırılm noktası dirsek noktası olmaktadır.

* While we were interpreting K-means, we were looking at the wcss values and we were saying that the point where the bend and break is the best K value. The algorithm
does exactly that. doing. The Wcss values graph is actually an x,y plane. The k value in the X plane corresponds to the wcss value in the Y plane. At this point
what we call refraction it is actually the angle that the k refracted in the plane makes with the previous k and the next k. The smallest of these angles is the 
bend point.

<div style="display:flex;width:100%;">
<img src="https://raw.githubusercontent.com/umutkaanbaser/dinamikkmeans/main/resimler/wCSS.png" width="250" title="wcss grafiği"/>
<img src="https://raw.githubusercontent.com/umutkaanbaser/dinamikkmeans/main/resimler/wcssKirilim.png" width="250" title="wcss grafiği kırılım"/>
</div>

* Bu durumda bu açıyı kolayca pisagor ve diskriminant ile bulabilir. 3 noktayı ele aldıktan her 3 noktadan mesafe hesaplamasıyla [((x1-x2)^2 + (y1-y2)^2)^(1/2)] 3 noktanın köşe olduğu bir üçgen çizebilir. Üçgene sahip olduktan sonra kolayca pisagoru uygulamayabilmekteyiz. Istenilen k bölgesinin [ (a^2+b^2-c^2)/(2*a*b) ] 
denklemiyle noktanın açısını kosinüs (cos) değerini bulabilmekteyiz. Arccos işlemiyle de kırılım açısını bulabililiriz. Kırılım açılarının en küçüğü bizim istediğimiz 
en iyi sonucu veren K değeri olacaktır. Böylece k-means ihtiyacı olan k değerini kendi yakalamış olacak ve dinamikleşicektir.

* In this case, he can easily find this angle with pythagoras and discriminant. Considering 3 points and calculating distance from each 3 points
[((x1-x2)^2 + (y1-y2)^2)^(1/2)] can draw a triangle where 3 points are vertices. Once we have the triangle, we can easily apply the Pythagorean. Desired k region 
[ (a^2+b^2-c^2)/(2*a*b) ] With the equation, we can find the angle of the point, the cosine (cos) value. We can also find the angle of refraction with the Arccos
operation. The smallest of the refractive angles is what we want will be the K value that gives the best result. Thus, k-means will catch the k value it needs and
will become dynamic.

<div style="display:flex;">
<img src="https://raw.githubusercontent.com/umutkaanbaser/dinamikkmeans/main/resimler/aci1.png" width="250" title="wcss'in içindeki üçgen"/>
<img src="https://github.com/umutkaanbaser/dinamikkmeans/blob/main/resimler/aci2.png" width="250" title="wcss'in içindeki üçgen"/>
<img src="https://github.com/umutkaanbaser/dinamikkmeans/blob/main/resimler/aci3.png" width="250" title="wcss'in içindeki üçgen"/>
</div>

# Argumanlar | Args
<br> **goster / show = True (boolean)** <br/>
goster : yapılan işlemlerin gelistiriciye gosterilip gosterilmeyeceğidir.

<br> **maxK = 10 (int)** <br/>
maxK : en fazla kaç adet k degeri alabileceğidir -> wcss grafiginde diresek olusması icin en az 5 veriniz
# Kullanım | Usage

* İlk başta gerekli modulleri yüklemelisiniz.
```
pip install requirements.txt
```
* Sonraki isterseniz bir üst klasorun altında isterseniz doğrudan çağırarak kütüphaneyi dahil edebilir ardından aşağıdaki kodlar ile eğitip, tanıma işlemi
yapabilirsiniz.

* Eğer ingilizce kod dosyasından dahil ediyorsanız yorum satırlarını kullanınız.
```
from dinamikKmeans import dinamikKmeans
#from dynamicKmeans import dynamicKmeans


dKnn = dinamikKmeans(goster=True,init="k-means++",random_state=12) 
#dKnn = dynamicKmeans(show=True,init="k-means++",random_state=12) 

#X sizin veri setinizdir.

dKnn.egit(X)
#dKnn.fit(X)

dKnn.tani(X)
#dKnn.predict(X)
```
