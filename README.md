# Telegram food delivery bot template
<p align="center">
  <img src="https://github.com/ozxmn/previews/blob/main/giphy.gif" alt="My GIF" width="400">
</p>

A ready-to-use Telegram bot template built with **Python** and **pyTelegramBotAPI**, designed for food delivery services.  
Supports **Kazakh** and **English** languages with Web App menus and both reply and inline keyboards.

---

## Features

- Multi-language support (Kazakh / English)
- Location-based address confirmation via OpenStreetMap API 
- Buttons for menu, location, and language  
- Modular and customizable structure  

---

## Setup & installation

### 1️⃣ Clone the repo
```bash
git clone https://github.com/ozxmn/delivery-bot.git
cd telegram-delivery-bot
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Add your bot tolen
Open `bot.py` and replace:
```python
bot = telebot.TeleBot("YOUR_BOT_TOKEN")
```
with your actual token from [@BotFather](https://t.me/BotFather).

### 4️⃣ Run the bot
```bash
python bot.py
```

---

## Usage

1. User selects a language (Kazakh or English)  
2. Bot requests their location  
3. Reverse-geocoding via OpenStreetMap confirms address  
4. User confirms → Menu & actions displayed 5. User can change the language or location anytime using inline buttons  

---

## Project structure

```
delivery-bot/
├── bot.py                # Main bot logic
├── requirements.txt      # Dependencies
├── README.md             # Project description
└── .gitignore            # Ignore unnecessary files
```

---

## Technologies Used

- [Python 3.x](https://www.python.org/)
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [OpenStreetMap Nominatim API](https://nominatim.openstreetmap.org/)

---

## Developer

**Mansur Ozaman**  
[GitHub](https://github.com/ozxmn)


---


