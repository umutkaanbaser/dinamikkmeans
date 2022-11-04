# Dinamik Kmeans | Dynamic Kmeans
   Merhaba arkadaşlar, bu dökümanda bir kümeleme algoritması olan k-means algoritmasında kaç kümeye ayrışacağını belirttiğimiz K parametresini dinamik yaparak kaç küme 
ayrılacağını kendisi karar vermesini sağladık. :)

# Nasıl Çalışır ? | How does is work ?

* Asağıda gördüğünüz örnek bir veri seti vardır. Bu dağılıma baktığımızda veri setinin kolayca 3 küme halinde değerlendirebileceğimizi görebilmekteyiz. Beraberinde aynı
işlemi kmeans'i bir döngüye alıp wcss (Küme İçi Kare Toplamı | Within-Cluster Sum of Square) değerleri grafiğinde kırılıma bakarakta yorumlayabilmekteyiz. Peki  verileri
inceleyemeceğimiz yada wcss değerlerini görerek yorumlayamayacğımız; uygulamaların arka planları, web sunucuları, görüntüde nesne ayrıştırma işlemleri gibi yerlerde kaç
k değeri olacağını söyleyemeyiz. Bu tarz durumlarda k-means en iyi şekilde kaç adet k değeri alacağına kendisi karar vermelidir. Statik değil dinamik çalışmalıdır.

<div style="display:flex;">
<img src="https://raw.githubusercontent.com/umutkaanbaser/dinamikkmeans/main/resimler/Dagilim.PNG" width="250" title"veri seti dağılımı"/>
<img src="https://raw.githubusercontent.com/umutkaanbaser/dinamikkmeans/main/resimler/dagilimKume.png" width="250" title="veri seti dağılımı kümelenmesi"/>
</div>

* K-means'i biz yorumlarken wcss değerlerine bakıyorduk ve dirsekleşme, kırılım olduğu noktanın en iyi K değeri olduğunu söylüyorduk. Algoritma da tam olarak bunu 
yapmakta. Wcss değerler grafiği aslında bir x,y düzlemidir. X düzlemindeki k değeri Y düzlemindeki wcss değerine karşılık gelmektedir. Bu noktada kırılım dediğimiz şey 
aslında düzemlede kırılan k'nın, bir önceki k ve bir sonraki k ile yaptığı açıdır. Bu açıların en küçüğü kırılm noktası dirsek noktası olmaktadır.

<div style="display:flex;width:100%;">
<img src="https://raw.githubusercontent.com/umutkaanbaser/dinamikkmeans/main/resimler/wCSS.png" width="250" title="wcss grafiği"/>
<img src="https://raw.githubusercontent.com/umutkaanbaser/dinamikkmeans/main/resimler/wcssKirilim.png" width="250" title="wcss grafiği kırılım"/>
</div>

* Bu durumda bu açıyı kolayca pisagor ve diskriminant ile bulabilir. 3 noktayı ele aldıktan her 3 noktadan mesafe hesaplamasıyla [((x1-x2)^2 + (y1-y2)^2)^(1/2)] 3 noktanın köşe olduğu bir üçgen çizebilir. Üçgene sahip olduktan sonra kolayca pisagoru uygulamayabilmekteyiz. Istenilen k bölgesinin [ (a^2+b^2-c^2)/(2*a*b) ] 
denklemiyle noktanın açısını kosinüs (cos) değerini bulabilmekteyiz. Arccos işlemiyle de kırılım açısını bulabililiriz. Kırılım açılarının en küçüğü bizim istediğimiz 
en iyi sonucu veren K değeri olacaktır. Böylece k-means ihtiyacı olan k değerini kendi yakalamış olacak ve dinamikleşicektir.
  
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

#X sizin veri setinizdir.

dKnn.egit(X)
#dKnn.fit(X)

dKnn.tani(X)
#dKnn.predict(X)
```
