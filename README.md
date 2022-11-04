# Dinamik Kmeans | Dynamic Kmeans

Merhaba arkadaşlar, bu dökümanda bir kümeleme algoritması olan k-means algoritmasında kaç kümeye ayrışacağını belirttiğimiz K parametresini dinamik yaparak kaç küme 
ayrılacağını kendisi karar vermesini sağladık. :)

# Nasıl Çalışır ? | How does is work ?

Asağıda gördüğünüz örnek bir veri seti vardır. Bu dağılıma baktığımızda veri setinin kolayca 3 küme halinde değerlendirebileceğimizi görebilmekteyiz. Beraberinde aynı
işlemi kmeans'i bir döngüye alıp wcss (Küme İçi Kare Toplamı | Within-Cluster Sum of Square) değerleri grafiğinde kırılıma bakarakta yorumlayabilmekteyiz. Peki  verileri
inceleyemeceğimiz yada wcss değerlerini görerek yorumlayamayacğımız; uygulamaların arka planları, web sunucuları, görüntüde nesne ayrıştırma işlemleri gibi yerlerde kaç
k değeri olacağını söyleyemeyiz. Bu tarz durumlarda k-means en iyi şekilde kaç adet k değeri alacağına kendisi karar vermelidir. Statik değil dinamik çalışmalıdır.

<div style="display:flex;">
<img src="https://raw.githubusercontent.com/umutkaanbaser/dinamikkmeans/main/resimler/Dagilim.PNG" width="350" title"veri seti dağılımı"/>
<img src="https://raw.githubusercontent.com/umutkaanbaser/dinamikkmeans/main/resimler/dagilimKume.png" width="350" title="veri seti dağılımı kümelenmesi"/>
</div>

K-means'i biz yorumlarken wcss değerlerine bakıyorduk ve dirsekleşme, kırılım olduğu noktanın en iyi K değeri olduğunu söylüyorduk. Algoritma da tam olarak bunu 
yapmakta. Wcss değerler grafiği aslında bir x,y düzlemidir. X düzlemindeki k değeri Y düzlemindeki wcss değerine karşılık gelmektedir. Bu noktada kırılım dediğimiz şey 
aslında düzemlede kırılan k'nın, bir önceki k ve bir sonraki k ile yaptığı açıdır. Bu açıların en küçüğü kırılm noktası dirsek noktası olmaktadır.

<div style="display:flex;">
<img src="https://raw.githubusercontent.com/umutkaanbaser/dinamikkmeans/main/resimler/wCSS.png" width="350" title="wcss grafiği"/>
<img src="https://raw.githubusercontent.com/umutkaanbaser/dinamikkmeans/main/resimler/wcssKirilim.png" width="350" title="wcss grafiği kırılım"/>
</div>
    Wcss grafiğinde X düzleminde k değerlerinden kırılımını kaç derece açıyla kırıldığını 
