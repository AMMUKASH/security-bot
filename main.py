import asyncio
import re
import nest_asyncio  # Latest Python Event Loop Crash Fix

# Pyrogram Client init hone se pehle apply karna compulsory hai
nest_asyncio.apply()

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPermissions
from config import Config
import database as db

bot = Client(
    "GuardianProBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# --- CONFIG HARDCODED VALUES FOR LOGS & OWNER ---
LOG_GROUP_ID = -1003947649552
OWNER_USERNAME = "CoderNova"

# Bad words list for Anti Abuse Filter
BAD_WORDS = ["bhenchod", "madarchod", "gand", "chutiya", "luda", "lavda", "bsdk", "harami", "randi", "sala"]

# --- WEB SERVER SETUP FOR RENDER PORT BINDING ---
from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is Running and Alive 24/7!")

async def start_server():
    try:
        app = web.Application()
        app.router.add_get('/', handle)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', Config.PORT)
        await site.start()
        print("🌐 WEB SERVER ACTIVE ON PORT CONFIGURATION!")
    except Exception as e:
        print(f"⚠️ Web Server Error: {e}")

# --- HELPER FUNCTIONS ---
async def extract_user(client, message: Message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    if len(message.command) < 2:
        return None
    user_to_find = message.command[1]
    if user_to_find.isdigit():
        try: return await client.get_users(int(user_to_find))
        except: return None
    if user_to_find.startswith("@"):
        user_to_find = user_to_find.replace("@", "")
    try: return await client.get_users(user_to_find)
    except: return None

def parse_buttons(text):
    if not text: return None
    try:
        kb = []
        matches = re.findall(r'\[([^\]]+)\|([^\]]+)\]', text)
        for name, url in matches:
            kb.append([InlineKeyboardButton(name.strip(), url=url.strip())])
        return kb if kb else None
    except: return None

async def is_admin(chat, user_id):
    if chat.type.value in ["private"]: return True
    try:
        m = await bot.get_chat_member(chat.id, user_id)
        return m.status.value in ["administrator", "owner"]
    except: return False

def get_action_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✨ ᴀᴅᴅ ᴍᴇ ✨", url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true"),
            InlineKeyboardButton("📢 ᴜᴩᴅᴀᴛᴇ", url=f"https://t.me/{Config.UPDATE_CH}")
        ]
    ])

# --- DYNAMIC SECURITY WARN & MUTE HANDLER ---
async def handle_member_violation(client, message: Message, target_user, reason):
    chat_id = message.chat.id
    count = await db.add_warn(chat_id, target_user.id)
    
    if count >= 3:
        try:
            # 3 Warns complete hone par 30 minutes (1800 seconds) ke liye mute
            await client.restrict_chat_member(
                chat_id, 
                target_user.id, 
                permissions=ChatPermissions(can_send_messages=False),
                until_date=int(asyncio.get_event_loop().time() + 1800)
            )
            await db.reset_warns(chat_id, target_user.id) # Reset warns after mute action
            mute_text = f"🤐 {target_user.mention} ko **3/3 Warnings** exceed karne par **30 Mins** ke liye mute kar diya gaya.\n\n⚠️ **Reason:** {reason}"
            await message.reply_text(mute_text, reply_markup=get_action_buttons())
            
            if LOG_GROUP_ID:
                await client.send_message(LOG_GROUP_ID, f"🤐 **#AUTO_MUTE_REPORT**\n\n💬 **ɢʀᴏᴜᴘ:** {message.chat.title}\n👤 **ᴜsᴇʀ:** {target_user.mention}\n⚠️ **ʀᴇᴀsᴏɴ:** {reason} (3/3 Warns)")
        except Exception as e:
            print(f"Mute Error: {e}")
    else:
        warn_text = f"⚠️ {target_user.mention} ko warning di gayi! (**{count}/3**)\n\n🚫 **Reason:** {reason}"
        await message.reply_text(warn_text, reply_markup=get_action_buttons())
        
        if LOG_GROUP_ID:
            await client.send_message(LOG_GROUP_ID, f"⚠️ **#AUTO_WARN_REPORT**\n\n💬 **ɢʀᴏᴜᴘ:** {message.chat.title}\n👤 **ᴜsᴇʀ:** {target_user.mention}\n📊 **ᴡᴀʀɴs:** {count}/3\n🚫 **ʀᴇᴀsᴏɴ:** {reason}")

# --- COMMAND HANDLERS ---

@bot.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    if message.chat.type.value == "private":
        await db.add_served_user(message.chat.id)
    else:
        await db.add_served_chat(message.chat.id)

    text = (
        "╭────── • 𝐆𝐔𝐀𝐑𝐃𝐈𝐀𝐍 𝐏𝐑𝐎 • ──────╮\n"
        "│      ✨ **ADVANCED GROUP SECURITY** ✨      \n"
        "├──────────────────────────────┤\n"
        "│ 🛡️ **BIO LINK PROTECTION** (Mute/Warn)\n"
        "│ 🔗 **ANTI LINK SYSTEM** (Auto Delete)\n"
        "│ 🚫 **ANTI ABUSE FILTER** (A to Z Words)\n"
        "│ 📥 **FORWARD CONTROL** (Anti Forward)\n"
        "│ 📝 **EDIT SECURITY** (Edited Link Ban)\n"
        "│ 🗑️ **MEDIA CLEANUP** (Media Strict Control)\n"
        "├──────────────────────────────┤\n"
        f"│ 👤 **ᴅᴇᴠᴇʟᴏᴩᴇʀ:** @{OWNER_USERNAME}\n"
        "╰──────────────────────────────╯"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✨ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴩ ✨", url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true")],
        [
            InlineKeyboardButton("📢 sᴜᴩᴩᴏʀᴛ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{Config.UPDATE_CH}"),
            InlineKeyboardButton("👥 sᴜᴩᴩᴏʀᴛ ɢʀᴏᴜᴩ", url="https://t.me/GIRLS_FIGHTER_GROUP")
        ],
        [InlineKeyboardButton("🛠️ ʜᴇʟᴩ ᴍᴇɴᴜ", callback_data="help_menu")]
    ])
    try:
        await message.reply_photo(photo=Config.START_IMG, caption=text, reply_markup=buttons)
    except Exception:
        await message.reply_text(text, reply_markup=buttons)

@bot.on_callback_query(filters.regex("^help_menu$|^back_start$"))
async def cb_handler(client, cb: CallbackQuery):
    if cb.data == "help_menu":
        help_text = "🛠️ **GUARDIAN PRO - ADMIN CONTROL PANEL**\n\n• `/ban` | `/unban` - Ban/Unban Management\n• `/mute` | `/unmute` - Voice Mute Control\n• `/warn` | `/diswarn` - Warning System\n• `/approve` | `/disapprove` - Whitelist Users"
        await cb.message.edit_caption(caption=help_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="back_start")]]))
    elif cb.data == "back_start":
        text = "╭────── • 𝐆𝐔𝐀𝐑𝐃𝐈𝐀𝐍 𝐏𝐑𝐎 • ──────╮\n│      ✨ **ADVANCED GROUP SECURITY** ✨      \n╰──────────────────────────────╯"
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴩ ✨", url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true")],
            [InlineKeyboardButton("📢 sᴜᴩᴩᴏʀᴛ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{Config.UPDATE_CH}"), InlineKeyboardButton("👥 sᴜᴩᴩᴏʀᴛ ɢʀᴏᴜᴩ", url="https://t.me/GIRLS_FIGHTER_GROUP")],
            [InlineKeyboardButton("🛠️ ʜᴇʟᴩ ᴍᴇɴᴜ", callback_data="help_menu")]
        ])
        await cb.message.edit_caption(caption=text, reply_markup=buttons)

# --- BROADCAST SYSTEM ---
@bot.on_message(filters.command(["broadcast", "bc"]) & filters.private)
async def advanced_broadcast(client, message: Message):
    if message.from_user.username != OWNER_USERNAME and message.from_user.id != Config.OWNER_ID:
        return
    target_msg = message.reply_to_message if message.reply_to_message else message
    if target_msg == message and len(message.command) < 2:
        await message.reply_text("❌ `/bc -all [text]` use karein.")
        return

    cmd_text = message.text or ""
    should_pin = "-pin" in cmd_text.lower()
    send_to_users = "-users" in cmd_text.lower()
    send_to_groups = "-groups" in cmd_text.lower()
    send_to_all = "-all" in cmd_text.lower() or (not send_to_users and not send_to_groups)

    status_msg = await message.reply_text("⚡ **ʙʀᴏᴀᴅᴄᴀsᴛ ɪɴɪᴛɪᴀʟɪᴢɪɴɢ...**")
    targets = []
    if send_to_users or send_to_all:
        users = await db.get_served_users()
        targets.extend([{"id": u["user_id"]} for u in users])
    if send_to_groups or send_to_all:
        chats = await db.get_served_chats()
        targets.extend([{"id": c["chat_id"]} for c in chats])

    unique_targets = {t["id"]: t for t in targets}.values()
    success, failed = 0, 0

    for target in unique_targets:
        try:
            if message.reply_to_message:
                sent_msg = await target_msg.copy(chat_id=target["id"])
            else:
                clean_text = cmd_text.replace("/broadcast", "").replace("/bc", "").replace("-pin", "").replace("-users", "").replace("-groups", "").replace("-all", "").strip()
                sent_msg = await client.send_message(chat_id=target["id"], text=clean_text)
            if should_pin and sent_msg:
                try: await sent_msg.pin()
                except: pass
            success += 1
            await asyncio.sleep(0.3)
        except:
            failed += 1

    await status_msg.edit_text(f"📊 **ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ**\n\n✅ Success: {success}\n❌ Failed: {failed}")

# --- AUTOMATED ULTIMATE SECURITY WATCHER ENGINE ---
@bot.on_message(filters.group & ~filters.service, group=1)
async def security_watcher(client, message: Message):
    if not message.from_user: return
    
    user_id = message.from_user.id
    is_user_admin = await is_admin(message.chat, user_id)
    is_user_approved = await db.is_approved(message.chat.id, user_id)
    
    text_content = message.text or message.caption or ""
    has_link = bool(re.search(r"t\.me|http|www\.", text_content))

    # 1. ANTI LINK SYSTEM (Owner, Admin, Members - Sabka delete hoga)
    if has_link:
        try: await message.delete()
        except: pass
        if not (is_user_admin or is_user_approved):
            await handle_member_violation(client, message, message.from_user, "Anti Link Violation (Sent Forbidden Link)")
        return

    # 2. MEDIA CLEANUP (Owner, Admin, Members - Sabka delete hoga)
    if message.photo or message.video or message.document or message.audio or message.voice or message.sticker:
        try: await message.delete()
        except: pass
        if not (is_user_admin or is_user_approved):
            await handle_member_violation(client, message, message.from_user, "Media Cleanup Violation (Sent Restricted Media)")
        return

    # --- BELOW RESTRICTIONS ONLY FOR NON-ADMIN MEMBERS ---
    if is_user_admin or is_user_approved:
        return

    # 3. BIO LINK PROTECTION (Members scan only)
    try:
        full_user_info = await client.get_chat_member(message.chat.id, user_id)
        user_bio = (await client.get_users(user_id)).bio or ""
        if re.search(r"t\.me|http|www\.", user_bio):
            try: await message.delete()
            except: pass
            await handle_member_violation(client, message, message.from_user, "Bio Link Violation (Links inside Telegram Profile Bio)")
            return
    except:
        pass

    # 4. ANTI ABUSE PROTECTION (A to Z word scan)
    for word in BAD_WORDS:
        if word in text_content.lower():
            try: await message.delete()
            except: pass
            await handle_member_violation(client, message, message.from_user, "Anti Abuse System (Used Profanity/Abusive Language)")
            return

    # 5. FORWARD CONTROL
    if message.forward_date or message.forward_from or message.forward_from_chat:
        try: await message.delete()
        except: pass
        await handle_member_violation(client, message, message.from_user, "Forward Control System (Forwards strictly Prohibited)")
        return

# --- 5. EDIT SECURITY SYSTEM (Edited messages catch engine) ---
@bot.on_edited_message(filters.group)
async def edit_security_engine(client, message: Message):
    if not message.from_user: return
    
    text_content = message.text or message.caption or ""
    has_link = bool(re.search(r"t\.me|http|www\.", text_content))
    
    if has_link:
        try: await message.delete()
        except: pass
        
        is_user_admin = await is_admin(message.chat, message.from_user.id)
        is_user_approved = await db.is_approved(message.chat.id, message.from_user.id)
        
        if not (is_user_admin or is_user_approved):
            await handle_member_violation(client, message, message.from_user, "Edit Security (Tried to bypass anti-link via message Editing)")

# --- WELCOME AND TRACKING COMMANDS ---
@bot.on_message(filters.command("welcomeset") & filters.group)
async def set_welcome_msg(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): return
    photo_msg = message if message.photo else (message.reply_to_message if message.reply_to_message and message.reply_to_message.photo else None)
    if not photo_msg:
        await message.reply_text("❌ Kisi photo ke caption me `/welcomeset [text]` likhein!")
        return
    fid = photo_msg.photo.file_id
    full_text = message.text or message.caption or ""
    text_w = full_text.replace("/welcomeset", "").strip()
    cap = text_w
    btn_raw = ""
    if "[" in text_w and "]" in text_w:
        start_idx = text_w.find("[")
        cap = text_w[:start_idx].strip()
        btn_raw = text_w[start_idx:].strip()
    await db.set_welcome(message.chat.id, fid, cap, btn_raw if btn_raw else None)
    await message.reply_text("✅ Custom Welcome with Image Saved!")

@bot.on_message(filters.new_chat_members & filters.group)
async def welcome_action(client, message: Message):
    await db.add_served_chat(message.chat.id)
    w_data = await db.get_welcome(message.chat.id)
    if not w_data: return
    cnt = await client.get_chat_members_count(message.chat.id)
    for m in message.new_chat_members:
        un = f"@{m.username}" if m.username else "No Username"
        cap = w_data["caption"].replace("{mention}", m.mention).replace("{name}", m.first_name).replace("{id}", str(m.id)).replace("{username}", un).replace("{title}", message.chat.title).replace("{count}", str(cnt))
        btns = parse_buttons(w_data.get("buttons"))
        markup = InlineKeyboardMarkup(btns) if btns else None
        try: await client.send_photo(chat_id=message.chat.id, photo=w_data["file_id"], caption=cap, reply_markup=markup)
        except: pass

# --- MODERN ASYNC LOOP EXECUTION ENGINE ---
async def main():
    await start_server()
    print("🤖 STARTING BOT CLIENT SESSION...")
    try:
        await bot.start()
        print("✅ GUARDIAN PRO SECURITY ENGINE STARTED SUCCESSFULLY AND ALIVE!")
    except Exception as e:
        print(f"❌ BOT START CRASHED: {e}")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try: asyncio.run(main())
    except (KeyboardInterrupt, SystemExit): print("Bot deployment stopped safely.")
