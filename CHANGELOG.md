# Changelog

Tüm önemli değişiklikler bu dosyada belgelenmiştir.

## [1.0.0] - 2025-05-11

### Eklendi
- Kaynak kanaldan hedef kanala mesaj aktarımı
- Medya desteği:
  - Fotoğraf (send_photo)
  - Video (send_video)
  - Dosya (send_document)
  - Sticker (send_sticker)
  - GIF/Animation (send_animation)
- Filtreleme özelliği (FILTER_KEYWORDS ile belirli kelimeleri içeren mesajları aktarma)
- SQLite veritabanı ile son mesaj ID takibi
- Polling tabanlı çalışma ( gerçek zamanlı update sorunu çözüldü)
- /start komutu (bot durumu)
- /status komutu (son işlenen mesaj ID)

### Teknik
- Pyrogram 2.0.x kullanımı
- Python 3.10+ uyumlu
- UTF-8 encoding desteği
- Windows uyumlu çalışma