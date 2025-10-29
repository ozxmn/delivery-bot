# 🛵 Telegram Delivery Bot Template

A ready-to-use Telegram bot template built with **Python** and **pyTelegramBotAPI**, designed for food delivery or location-based services.  
Supports **Kazakh** and **English** languages with dynamic menus and both reply and inline keyboards.

---

## 🚀 Features

- 🌍 Multi-language support (Kazakh / English)  
- 📍 Location-based address confirmation via OpenStreetMap Nominatim API 
- 🧭 Buttons for menu, location, and language  
- 🔄 Error-safe polling loop (auto-reconnects)  
- 🧱 Modular and customizable structure  

---

## 🧩 Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/mansur_ozaman/delivery-bot.git
cd telegram-delivery-bot
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Add Your Bot Token
Open `bot.py` and replace:
```python
bot = telebot.TeleBot("YOUR_BOT_TOKEN")
```
with your actual token from [@BotFather](https://t.me/BotFather).

### 4️⃣ Run the Bot
```bash
python bot.py
```

---

## 🧠 How It Works

1. User selects a language (Kazakh or English)  
2. Bot requests their location  
3. Reverse-geocoding via OpenStreetMap confirms address  
4. User confirms → Menu & actions displayed  
5. Change language/location anytime with inline buttons  

---

## 🧱 Folder Structure

```
delivery-bot/
├── bot.py                # Main bot logic
├── requirements.txt      # Dependencies
├── README.md             # Project description
└── .gitignore            # Ignore unnecessary files
```

---

## 🧰 Technologies Used

- [Python 3.x](https://www.python.org/)
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [OpenStreetMap Nominatim API](https://nominatim.openstreetmap.org/)

---

## 🧑‍💻 Author

**Mansur Ozaman**  
🐙 [GitHub](https://github.com/mansur_ozaman)


---


