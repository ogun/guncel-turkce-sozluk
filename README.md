# Projenin Amacı
Türk Dil Kurumu'nun yayınladığı Güncel Türkçe Sözlük'ü yazılımcıların kullanabileceği bir hale getirmek. Şu anda proje içerisinde 92.403 adet madde en güncel haliyle bulunmaktadır.

Sözlüğü üç farklı türde indirebilirsiniz.
1. JSON dosyası olarak: [gts.json.tar.gz](sozluk/gts.json.tar.gz)
2. MongoDB archive dosyası olarak: [gts.mongo4.gzip.archive](sozluk/gts.mongo4.gzip.archive)
3. SQLite veritabanı olarak: [gts.sqlite3.db](sozluk/gts.sqlite3.db)

## JSON
İndirdiğiniz dosya GZIP ile sıkıştırılmıştır. Sıkıştırmayı açtıktan sonra içeriğini herhangi bir text editörle görüntüleyebilirsiniz.

## MongoDB
İndirdiğiniz dosyayı aşağıdaki komutun yardımıyla kendi MongoDB sunucunuza aktarabilirsiniz.

`mongorestore --gzip --archive=gts.mongo4.gzip.archive`

## SQLite
İndirdiğiniz dosyayı herhangi bir SQLite görüntüleyici ile görüntüleyebilirsiniz ve kullanabilirsiniz. Veritabanının şeması aşağıdaki gibidir.
![alt text](static/schema.png "SQLite Schema")

## Bilinen Problemler
Şu anda sözlük güncel halindeki 3 adet maddeyi içermiyor. Bu maddeleri şu anki API üzerinden ulaşılamadığı için ekleyemedim. Eksik maddeler ve id'leri:
1. a / e (#6171)
2. da / de (#15889)
3. mı / mi, mu / mü (#31114)

# TDK 2007 Sözlüğü
TDK'nın 2007 yılında yayınladığı sözlüğe ise old klasöründeki [TDK-2007.rar](old/TDK-2007.rar) dosyasından ulaşabilirsiniz. Eski sözlük içerisinde 73.707 adet madde bulundurmaktadır.

# Güncel Türkçe Sözlük
Türk Dil Kurumunun 1945'ten beri yayımlanan Türkçe Sözlük'ünün 2011 yılında yapılan 11. baskısının gözden geçirilip güncellenmiş olarak genel ağdan sunulan sürümüdür. Türkçe Sözlük dilimizde yaşanan gelişmelere bağlı olarak sürekli güncellenmektedir.

http://www.sozluk.gov.tr/
