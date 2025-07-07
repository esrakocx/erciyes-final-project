# ✈️ CloudDelay - Uçuş Gecikme Tahmin Sistemi

CloudDelay, uçuş gecikmelerini tahmin etmek ve analiz etmek amacıyla geliştirilmiş, AWS üzerinde çalışan gerçek zamanlı veri işleme ve web tabanlı tahmin sistemidir. Proje, modern veri mühendisliği tekniklerini ve bulut servislerini bir araya getirerek hem yolcular hem de havayolu şirketleri için değerli öngörüler sunar.

---

## 🚀 Proje Özeti

- 🔍 **Amaç:** Uçuşların gecikme riskini önceden tahmin etmek ve olasılık sınıflarına göre kullanıcıya sunmak  
- ☁️ **Altyapı:** Amazon Web Services (AWS)  
- 📡 **Veri Kaynağı:** [Amadeus Flight Delay Prediction API](https://developers.amadeus.com/self-service/category/flights/api-doc/flight-delay-prediction)  
- 📊 **Analiz:** SQL, Python, Tableau  
- 🌐 **Arayüz:** Flask tabanlı web uygulaması

---

## 🛠️ Kullanılan Teknolojiler

### 🔄 Veri İşleme & Backend
- Python (Pandas, NumPy)
- Flask (RESTful API & Web arayüzü)
- AWS S3 (Veri depolama)
- AWS Glue (ETL işlemleri)
- AWS Athena (SQL tabanlı veri analizi)

### 🎨 Arayüz & Görselleştirme
- Bootstrap 5, HTML/CSS, JavaScript
- Chart.js ve Tableau dashboard'ları

---

## 📦 Kurulum (Local Test Amaçlı)

> Not: Proje AWS üzerinde çalışmak üzere yapılandırılmıştır. Aşağıdaki adımlar lokal ortamda test içindir.

```bash
# Gerekli kütüphaneleri kurun
pip install flask pandas numpy requests boto3

# Uygulamayı başlatın
python app.py
```

Uygulama, `http://localhost:5000` adresinden erişilebilir olacaktır.

---

## 📈 Örnek Kullanım

Web arayüzüne uçuş bilgileri girildiğinde sistem şu şekilde çıktı verir:

> 📍 Rota: ESB → IST  
> ⏰ Kalkış Saati: 16:00  
> 🔎 Tahmin: `OVER_120_MINUTES_OR_CANCELLED`  
> 🎯 Olasılık: %73

---

## 📊 Model Başarımı

| Metrik        | Değer |
|---------------|-------|
| Doğruluk      | 87.3% |
| ROC-AUC       | 0.91  |
| F1-Skoru      | 0.84  |

---

## 📁 Proje Yapısı

```bash
cloud-delay/
├── app.py                  # Flask backend
├── templates/              # HTML şablonları
├── static/                 # CSS, JS dosyaları
├── utils/                  # Veri işleme scriptleri
├── data/                   # Örnek veri setleri
├── README.md               # Proje açıklaması
└── requirements.txt        # Gerekli kütüphaneler
```

---

## 🔮 Gelecek Geliştirmeler

- ☁️ Hava durumu API'si entegrasyonu  
- 📱 Mobil uygulama (iOS & Android)  
- 📧 E-posta / SMS bildirim sistemi  
- 🧠 Gelişmiş makine öğrenmesi modelleri

---

## 👩‍💻 Geliştirici

**Esra Koç**  
📧 [Email adresiniz]  
🔗 [LinkedIn / GitHub adresiniz]  

---
<img width="1541" alt="veri_analizi (1)" src="https://github.com/user-attachments/assets/a4cb9273-e459-4742-b503-4e9936d9892c" />

## 📚 Referanslar

- [AWS Console](https://aws.amazon.com/console/)
- [Amadeus Flight Delay Prediction API](https://developers.amadeus.com/self-service/category/flights/api-doc/flight-delay-prediction)
  
---

### Projeye Ait Görseller <img width="1710" alt="anasayfa (1)" src="https://github.com/user-attachments/assets/f1662394-aad3-44ac-8710-1b1200b08528" /><img width="1416" alt="gecikme_tahmini (1)" src="https://github.com/user-attachments/assets/f7bb2168-728e-4518-bd03-6d09c9c18e8f" />

<img width="1487" alt="sql_sayfasi (1)" src="https://github.com/user-attachments/assets/8dd9a3ad-8b25-41e3-b8ef-52e1c24cc1c7" /><img width="949" alt="tahmin (1)" src="https://github.com/user-attachments/assets/82b70dc2-5323-4539-84a1-2b8b83bf1566" />
<img width="1399" alt="sql_ornek (1)" src="https://github.com/user-attachments/assets/4d189df7-a864-4a28-b834-106844493166" />
<img width="1415" alt="gorsel_ornek (1)" src="https://github.com/user-attachments/assets/65c5e3d8-8c37-499c-94bc-cfb7dfaeb6fa" />

