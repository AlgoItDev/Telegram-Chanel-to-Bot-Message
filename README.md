# Telegram Channel Mesaj Aktarıcı

Bir kanaldaki mesajları otomatik olarak başka bir kanala iletir.

## Versiyon

**v1.0.0**

## Özellikler

- Kaynak kanaldan mesajları otomatik olarak hedef kanala iletir
- Metin, fotoğraf, video, dosya, sticker, GIF desteği
- Filtreleme (belirli kelimeleri içeren mesajları aktarır)
- Veritabanı ile son mesaj takibi (yinelenmeleri önler)
- Polling tabanlı çalışma (私人 kanallar için optimize)
- 5 saniye periyotlu otomatik kontrol

## Kurulum

1. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

2. **Ayarları yapılandırın:**
```bash
copy .env.example .env
```

`.env` dosyasını düzenleyin:
- `API_ID` ve `API_HASH`: [my.telegram.org](https://my.telegram.org) adresinden alın
- `SOURCE_CHANNEL_ID`: Mesajların geldiği kanal ID (negatif, ör: -1001234567890)
- `TARGET_CHANNEL_ID`: Mesajların gönderileceği kanal ID
- `FILTER_KEYWORDS`: Opsiyonel, virgülle ayrılmış filtre kelimeleri

3. **Botu başlatın:**
```bash
python main.py
```

Bot ilk çalıştığında Telegram'dan oturum açma kodu isteyecek.

## Komutlar

- `/start` - Botu başlat (DM'de)
- `/status` - Durumu göster

## Notlar

- Hedef kanalda bot **yönetici** olmalı
- Kaynak kanalda okuma yetkisi yeterli
- Sürekli çalışması için VPS önerilir
- Windows'ta çalıştırırken UTF-8 encoding ayarlanmalıdır

---

## Changelog

### v1.0.0 (2025-05-11)
- İlk sürum
- Kaynak kanaldan hedef kanala mesaj aktarımı
- Medya desteği (fotoğraf, video, dosya, sticker, GIF)
- Filtreleme özelliği
- SQLite veritabanı ile mesaj takibi
- Polling tabanlı çalışma (updates sorunu çözüldü)
- /start ve /status komutları