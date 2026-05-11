# Changelog

## [1.1.0] - 2025-05-11

### Eklendi
- Coklu kaynak kanal destegi (virgulle ayrilmis ID listesi)
- FloodWait yonetimi - API limit asildiginda otomatik bekler ve tekrar eder
- aiosqlite ile async veritabani islemleri
- Album/medya grubu kontrolu
- Caption filtreleme (sadece text degil, caption da kontrol edilir)
- Systemd servis dosyasi (VPS icin)

### Düzeltmeler
- `await app.stop()` eksikligi giderildi
- Event loop hatalari duzeltildi
- Print yerine log formatlamasi

### Bilinen Sorunlar
- Album mesajlari henüz tam desteklenmiyor (atlanıyor)

---

## [1.0.0] - 2025-05-11

### Eklendi
- Kaynak kanaldan hedef kanala mesaj aktarimi
- Medya destegi:
  - Fotograf (send_photo)
  - Video (send_video)
  - Dosya (send_document)
  - Sticker (send_sticker)
  - GIF/Animation (send_animation)
- Filtreleme ozelligi (FILTER_KEYWORDS)
- SQLite veritabani ile son mesaj ID takibi
- Polling tabanli calisma (gercek zamanli update sorunu cozuldu)
- /start komutu
- /status komutu

### Teknik
- Pyrogram 2.0.x kullanimi
- Python 3.10+ uyumlu
- UTF-8 encoding destegi
- Windows uyumlu calisma