# 🛡️ GUARDIAN PRO SECURITY BOT

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Pyrogram-orange.svg)](https://docs.pyrogram.org/)
[![Database](https://img.shields.io/badge/database-MongoDB-green.svg)](https://www.mongodb.com/)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()

**Guardian Pro** ek advanced, fast aur highly customizable Telegram Group Security aur Moderation bot hai. Ye aapke Telegram groups ko spammers, abusers, aur unwanted links se bachaane ke liye design kiya gaya hai. Isme custom triggers (filters) aur fully customized welcome message features bhi in-built hain.

---

## 📸 Bot Interface

![Bot Banner](https://files.catbox.moe/bpktqb.jpg)

---

## ✨ Features

* 🛡️ **Anti-Link System:** Group me kisi bhi tarah ke links (`http`, `www.`, `t.me`) ko instantly delete karta hai.
* 📥 **Forward Control:** Kisi doosre channel ya group se forward kiye gaye messages ko auto-delete karta hai.
* 🚫 **Anti-Abuse Protection:** Bad words aur slangs ko detect karke messages ko automatic clean karta hai.
* 📝 **Edit Security:** Agar koi user message send karne ke baad use edit karke link daalta hai, toh bot use bhi pakad kar delete kar deta hai.
* 🎨 **Customized Welcome:** Aap kisi bhi image, custom text aur inline buttons ke sath group join karne wale members ke liye ek unique welcome style set kar sakte hain.
* 🔍 **Trigger Filters:** Apne group ke liye custom keywords par auto-replies set kar sakte hain.
* 🟢 **User Approval:** Admins kisi bhi trusted member ko whitelist (`/approve`) kar sakte hain taaki uspe security rules apply na hon.

---

## 🛠️ Commands Guide

### 👮 Moderation Commands
| Command | Usage | Description |
| :--- | :--- | :--- |
| `/ban` | Reply to User | User ko group se permanently ban karne ke liye. |
| `/unban` | `/unban [User_ID]` or Reply | Banned user ko wapas group me aane ki permission dene ke liye. |
| `/mute` | Reply to User | User ko group me message bhejne se rokne ke liye. |
| `/unmute` | `/unmute [User_ID]` or Reply | Muted user ko dubara chat karne dene ke liye. |
| `/warn` | Reply to User | User ko warning dene ke liye (3/3 warns par auto-ban). |
| `/diswarn` | Reply to User | User ki ek warning kam (remove) karne ke liye. |
| `/approve` | Reply to User | User ko whitelist karne ke liye (ispar anti-link kaam nahi karega). |
| `/disapprove` | Reply to User | Approved user ko whitelist se hatane ke liye. |

### ⚙️ Welcome Configuration
| Command | Usage | Description |
| :--- | :--- | :--- |
| `/welcomeset` | Reply to Photo + Text | Custom welcome message set karne ke liye. |
| `/welcomereset` | `/welcomereset` | Custom welcome message ko delete aur disable karne ke liye. |

#### Welcome Tags (For Customization):
* `{mention}` - User ko tag karne ke liye.
* `{name}` - User ka first name dikhane ke liye.
* `{id}` - User ki Telegram ID dikhane ke liye.
* `{username}` - User ka handle (`@username`) dikhane ke liye.
* `{title}` - Group ka naam automatic fetch karne ke liye.
* `{count}` - Group ke total members ki sankhya dikhane ke liye.

#### Inline Buttons Format:
```text
[ Button Name | [https://link.com](https://link.com) ]
