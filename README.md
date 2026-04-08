# OpenCV Diameter Gauge - Para/Pul Çap Ölçüm Sistemi

**Açıklama:** OpenCV kullanarak görüntüdeki paraların (puların) çapını otomatik olarak ölçen Python uygulaması.

## 🎯 Proje Özellikleri

- **Otomatik Kalibrasyon:** Çapı bilinen referans görüntülerden mm/piksel oranı hesapla
- **Çap Ölçümü:** Hedef görüntülerdeki paraların çapını milimetre cinsinden ölçme
- **Güvenilirlik Skoru:** Her ölçüm için güvenilirlik derecesi hesaplama
- **CSV Raporu:** Sonuçları otomatik olarak CSV dosyasına kaydetme
- **Debug Modu:** `-debug` flag'ı ile detaylı çıktı ve görselleştirmeler

## 📁 Proje Yapısı

```
opencvDiameterGauge/
├── main.py              # Ana uygulama
├── calibration.py       # Kalibrasyon modülü
├── detector.py          # Görüntü işleme ve çap algılama
├── measure.py           # Ölçüm ve raporlama
├── images/              # Referans ve target görüntüler
│   ├── 1e.bmp - 5b.bmp (Kalibrasyon - referans görüntüler)
│   └── 6e.bmp - 11a.bmp (Target - ölçülecek görüntüler)
└── results.csv          # Çıktı raporu
```

## 🔧 Teknik Detaylar

### Kalibrasyon (`calibration.py`)
- **CalibrationResult:** Kalibrasyon sonuçlarını saklayan dataclass
  - `ratios`: Her referans görüntüden hesaplanan mm/piksel oranları
  - `mean_ratio`: Ortalama oran
  - `std_ratio`: Standart sapma (ölçüm güvenilirliği göstergesi)

### Referans Görüntüler (Kalibrasyonda Kullanılan)
| Görüntü | Çap (mm) |
|---------|---------|
| 1e.bmp | 10.4905 |
| 2a.bmp | 10.4992 |
| 3e.bmp | 10.4826 |
| 4a.bmp | 10.5005 |
| 5b.bmp | 10.5005 |

### Target Görüntüler
- 6e.bmp, 7a.bmp, 8e.bmp, 9a.bmp, 10e.bmp, 11a.bmp

## 💻 Kullanım

### Temel Kullanım
```bash
python main.py
```

### Debug Modu (Detaylı Çıktı)
```bash
python main.py --debug
```

## 📊 Çıktı Format

**Ekran Çıktısı:**
```
╔══════════════════════════════════════════╗
║      PUL ÇAP ÖLÇÜM SİSTEMİ              ║
╚══════════════════════════════════════════╝

1. Calibration started...
2. Measurement started...
3. Measurement Report:
4. Results saved to results.csv
```

**CSV Çıktısı (results.csv):**
```
Image,Measured Diameter (mm),Trust
images/6e.bmp,10.4905,0.95
...
```

## 🛠️ Gereksinimler

```
python >= 3.9
opencv-python
numpy
```

### Kurulum
```bash
pip install opencv-python numpy
```

## 📈 Çalışma Akışı

```
1. KALIBRASYON
   ├─ Referans görüntüleri yükle (5 adet)
   ├─ Her görüntüdeki para çapını piksel cinsinden algıla
   ├─ mm/piksel oranını hesapla
   ├─ Ortalamasını ve standart sapmasını hesapla
   └─ Kalibrasyon katsayısını kaydet

2. ÖLÇÜM
   ├─ Target görüntüleri yükle (6 adet)
   ├─ Her görüntüdeki para çapını piksel cinsinden algıla
   ├─ Kalibrasyon katsayısı kullanarak mm'ye dönüştür
   ├─ Güvenilirlik skoru hesapla
   └─ Sonuçları listele

3. RAPORLAMA
   ├─ Ölçüm sonuçlarını ekrana yazdır
   ├─ İstatistiksel özeti göster
   └─ CSV dosyasına kaydet
```

## 📊 Algoritma

### Çap Algılama (Hough Circle Detection)
```
1. Görüntüyü gri tonlamaya dönüştür
2. Gausian bulanıklık uygula (iyileştirme)
3. Hough Circle Detection çalıştır
4. Algılanan dairenin çapını piksel cinsinden al
```

### Kalibrasyonlu Ölçüm
```
diameter_mm = diameter_px × mean_ratio
confidence = 1 - (std_ratio / mean_ratio) × weight
```

## 🐛 Hata Yönetimi

- Kalibrasyon başarısız olursa → programı durdur
- Ölçüm yapılmayan görüntüler → atlama ve devam
- Eksik görüntü dosyaları → hata mesajı

## 👨‍💻 Teknolojiler

- **OpenCV:** Görüntü işleme ve çap algılama
- **Python:** Programlama dili
- **CSV:** Veri depolama ve raporlama
- **Dataclasses:** Veri yapıları

## 📝 Lisans

Bu proje İnsan Kaynakları/Staj programı altında geliştirilmiştir.

**Yazar:** 2024-06-01

## 🚀 Gelecek İyileştirmeler

- [ ] Batch işleme desteği
- [ ] Web arayüzü (Flask/Django)
- [ ] Gerçek zamanlı kamera desteği
- [ ] Birden fazla para algılama
- [ ] İstatistiksel analiz (min/max/avg)
- [ ] Kalibrasyonu dosyaya kaydetme/yükleme
