# ALGO IT Telegram Channel Forwarder

Telegram kanallarından mesajları otomatik olarak hedef kanala ileten bot.

## Versiyon

**v1.1.0**

## Ozellikler

- **Coklu Kanal Desteği:** Birden fazla kaynak kanaldan mesajlari aktarabilir
- **Medya Destegi:** Metin, fotograf, video, dosya, sticker, GIF
- **Filtreleme:** Belirli kelimeleri iceren mesajlari aktarir (text ve caption)
- **FloodWait Yonetimi:** Telegram API limit asildiginda otomatik bekler
- **Async Veritabani:** aiosqlite ile performansli veri islemi
- **Medya Grubu Destegi:** Album mesajlarini tanir
- **Logging:** Detayli log ciktisi

## Kurulum

1. **Bagimliliklari yukleyin:**
```bash
pip install -r requirements.txt
```

2. **Ayarlari yapilandirin:**
```bash
copy .env.example .env
```

`.env` dosyasini duzenleyin:
- `API_ID` ve `API_HASH`: [my.telegram.org](https://my.telegram.org) adresinden alin
- `SOURCE_CHANNEL_ID`: Kaynak kanal ID'leri (virgulle ayrilmis, opsiyonel)
- `TARGET_CHANNEL_ID`: Hedef kanal ID
- `FILTER_KEYWORDS`: Virgulle ayrilmis filtre kelimeleri

Ornek:
```env
SOURCE_CHANNEL_ID=-1001234567890,-1001234567891
TARGET_CHANNEL_ID=-1009876543210
FILTER_KEYWORDS=kazanc,bonus
```

3. **Botu baslatin:**
```bash
python main.py
```

## VPS Kurulum (Ubuntu/Debian)

1. Projeyi kopyalayın:
```bash
cd /opt
git clone https://github.com/yourrepo/telegram-forwarder.git
cd telegram-forwarder
```

2. Ortami hazirlayin:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Servisi kurun:
```bash
sudo cp telegram-forwarder.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable telegram-forwarder
sudo systemctl start telegram-forwarder
```

4. Durumu kontrol edin:
```bash
sudo systemctl status telegram-forwarder
```

## Komutlar

- `/start` - Botu baslat (DM'de)
- `/status` - Durumu goster

## Notlar

- Hedef kanalda bot **yonetici** olmali
- Kaynak kanallarda okuma yetkisi yeterli
- Surekli calismasi icin VPS önerilir

---

## Teknik

- Python 3.10+
- Pyrogram 2.0+
- aiosqlite (async veritabani)
- Polling tabanli (5 saniye periyot)