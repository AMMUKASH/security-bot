# 🤖 MULTI-FORCE JOIN TELEGRAM BOT

<p align="center">
  <img src="https://files.catbox.moe/ko5i86.jpg" alt="Bot Start Image" width="450"/>
</p>

<p align="center">
  <a href="https://t.me/Insta_mmmmmsss_bot">
    <img src="https://img.shields.io/badge/Telegram-@Insta__mmmmmsss__bot-blue?style=for-the-badge&logo=telegram" alt="Bot Username"/>
  </a>
  <img src="https://img.shields.io/badge/Language-Python%203-yellow?style=for-the-badge&logo=python" alt="Language"/>
  <img src="https://img.shields.io/badge/Framework-Pyrogram-orange?style=for-the-badge" alt="Framework"/>
</p>

---

## 📌 Features
* 🔄 **Multiple Buttons:** Ek sath 13+ channels ko inline keyboard me handle karta hai.
* ⚡ **Auto-Update Buttons:** User jo channel join kar leta hai, wo button automatic list se gayab ho jata hai.
* 🚀 **FastAPI Integration:** Web server backend ke sath 24/7 active rehta hai.
* ⏱️ **Cron Job Compatible:** Render par bina sleep huye continuous run karne ke liye optimized hai.
* 🎯 **Smart Clean:** Saare channels join hote hi purana buttons wala message delete hokar fresh start image aur caption send karta hai.

---

## 🛠️ Configuration (Environment Variables)

Agar aap variables ko hide rakhna chahte hain, to Render par ye keys add karein:

| Key | Value |
| :--- | :--- |
| `API_ID` | `38138069` |
| `API_HASH` | `2ed313ebcc45cbcf65d1fc736ec71681` |
| `BOT_TOKEN` | `8469456367:AAHnPUxDa1246b3O4p0yHkM4CKkIfSsToW0` |

---

## 🚀 Deployment On Render

1. Is repository ko apne **GitHub** par fork ya upload karein.
2. [Render Dashboard](https://dashboard.render.com) par jayein aur **Web Service** create karein.
3. Apni repository ko connect karein aur neeche di gayi settings fill karein:

* **Runtime:** `Python 3`
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## ⏱️ Keeping Bot Alive (Cron Job)

Render free tier par bot ko active rakhne ke liye ek **Cron Job** create karein:
* **Schedule:** `*/10 * * * *` (Every 10 minutes)
* **Command:** `curl -s https://your-web-service-url.onrender.com`

---

## ⚠️ Important Note
> **⚠️ CRITICAL:** Bot tabhi work karega jab **@Insta_mmmmmsss_bot** ko aapke saare 13 channels/groups me **Admin Rights** mile honge. Agar bot admin nahi hoga, to wo membership verify nahi kar payega!

<p align="center">
  <b>Made with ❤️ by Amrit</b>
</p>
