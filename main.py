# ========================================================
# CRITICAL PYTHON 3.12+ / 3.14 LOOP PATCH
# Is patch ko sabse upar hona zaroori hai taaki Pyrogram import crash na kare
# ========================================================
import asyncio
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
# ========================================================

import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPermissions
from config import Config
import database as db
from aiohttp import web

bot = Client(
    "GuardianProBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# --- HARDCODED LINKS & CONFIG VARIATIONS ---
OWNER_USERNAME = "CoderNova"
UPDATE_CHANNEL_LINK = "https://t.me/Gc_help_update"
SUPPORT_GROUP_LINK = "https://t.me/Genu_Bot_Support"
BOT_USERNAME = "Group_secu_bot"

BAD_WORDS = ["bhenchod", "madarchod", "gand", "chutiya", "luda", "lavda", "bsdk", "harami", "randi", "sala"]

# --- RENDER WEB PORT SERVER SYSTEM ---
async def handle(request):
    return web.Response(text="Bot Security Infrastructure is Running 24/7 Alive!")

async def start_server():
    try:
        app = web.Application()
        app.router.add_get('/', handle)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', Config.PORT)
        await site.start()
        print("🌐 WEB PORT BINDING SERVER ALIVE!")
    except Exception as e:
        print(f"⚠️ Web Server Binding Error: {e}")

# --- INTERNAL SYSTEM HELPERS ---
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

async def is_admin(chat, user_id):
    if chat.type.value in ["private"]: return True
    try:
        m = await bot.get_chat_member(chat.id, user_id)
        return m.status.value in ["administrator", "owner"]
    except: return False

def get_action_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✨ ᴀᴅᴅ ᴍᴇ ✨", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
            InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇ", url=UPDATE_CHANNEL_LINK)
        ]
    ])

def parse_buttons(text):
    if not text: return None
    try:
        kb = []
        matches = re.findall(r'\[([^\]]+)\|([^\]]+)\]', text)
        for name, url in matches:
            kb.append([InlineKeyboardButton(name.strip(), url=url.strip())])
        return kb if kb else None
    except: return None

# --- STYLISH PROSE DISPLAY TEMPLATES ---
START_TEXT = (
    "⚡ **ʜᴇʟʟᴏ {name}!**\n\n"
    "🛡️ **ɪ ᴀᴍ ɢᴜᴀʀᴅɪᴀɴ ᴘʀᴏ**, ʏᴏᴜʀ ᴜʟᴛɪᴍᴀᴛᴇ ɢʀᴏᴜᴘ sᴇᴄᴜʀɪᴛʏ ᴀɴᴅ ᴍᴏᴅᴇʀᴀᴛɪᴏɴ sʏsᴛᴇᴍ.\n\n"
    "👤 **ᴅᴇᴠᴇʟᴏᴘᴇʀ:** @{owner}"
)

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("✨ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ✨", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
    [InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url=UPDATE_CHANNEL_LINK), InlineKeyboardButton("👥 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_GROUP_LINK)],
    [InlineKeyboardButton("⚙️ sᴇᴛᴛɪɴɢ ᴍᴇɴᴜ", callback_data="modules_menu")]
])

SETTING_MENU_TEXT = "⚙️ **ɢᴜᴀʀᴅɪᴀɴ ᴘʀᴏ - sᴇᴄᴜʀɪᴛʏ ᴄᴏɴғɪɢᴜʀᴀᴛɪᴏɴs**\n\nᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ᴍᴏᴅᴜʟᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ sᴇᴇ ᴛʜᴇɪʀ sᴇᴄᴜʀɪᴛʏ ɢᴜɪᴅᴇs:"
SETTING_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔗 ᴀɴᴛɪ-ʟɪɴᴋ", callback_data="guide_link"), InlineKeyboardButton("🔞 ɴsғᴡ & ᴅʀᴜɢs", callback_data="guide_nsfw")],
    [InlineKeyboardButton("🛡️ ʙɪᴏ & ᴇᴅɪᴛ ɢᴜᴀʀᴅ", callback_data="guide_bio"), InlineKeyboardButton("🛠️ ᴀᴅᴍɪɴ ᴄᴍᴅs", callback_data="guide_admin")],
    [InlineKeyboardButton("⬅️ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ", callback_data="back_start")]
])

# --- DYNAMIC SECURITY WARN & AUTOMATED MUTE PATH ---
async def handle_member_violation(client, message: Message, target_user, reason):
    chat_id = message.chat.id
    count = await db.add_warn(chat_id, target_user.id)
    
    if count >= 3:
        try:
            await client.restrict_chat_member(
                chat_id, 
                target_user.id, 
                permissions=ChatPermissions(can_send_messages=False),
                until_date=int(asyncio.get_event_loop().time() + 1800)
            )
            await db.reset_warns(chat_id, target_user.id)
            await message.reply_text(f"🤐 {target_user.mention} ko **3/3 Warnings** exceed karne par **30 Mins** ke liye mute kar diya gaya.\n\n⚠️ **Reason:** {reason}", reply_markup=get_action_buttons())
        except Exception as e:
            print(f"Auto Mute Error: {e}")
    else:
        await message.reply_text(f"⚠️ {target_user.mention} ko warning di gayi! (**{count}/3**)\n\n🚫 **Reason:** {reason}", reply_markup=get_action_buttons())

# --- USER ENTRY AND CORE ENTRY HANDLERS ---
@bot.on_message(filters.command(["start", f"start@{BOT_USERNAME}"]))
async def start_cmd(client, message: Message):
    if message.chat.type.value == "private": 
        await db.add_served_user(message.chat.id)
    else: 
        await db.add_served_chat(message.chat.id)
    text = START_TEXT.format(name=message.from_user.first_name, owner=OWNER_USERNAME)
    try: 
        await message.reply_photo(photo=Config.START_IMG, caption=text, reply_markup=START_BUTTONS)
    except: 
        await message.reply_text(text, reply_markup=START_BUTTONS)

@bot.on_message(filters.command(["setting", f"setting@{BOT_USERNAME}"]))
async def setting_cmd(client, message: Message):
    if message.chat.type.value != "private" and not await is_admin(message.chat, message.from_user.id):
        await message.reply_text("❌ Is command ko use karne ke liye aapka Group Admin hona zaroori hai!")
        return
    try: 
        await message.reply_photo(photo=Config.START_IMG, caption=SETTING_MENU_TEXT, reply_markup=SETTING_BUTTONS)
    except: 
        await message.reply_text(SETTING_MENU_TEXT, reply_markup=SETTING_BUTTONS)

# --- FILTER COMMAND LOGIC ---
@bot.on_message(filters.command(["filter", f"filter@{BOT_USERNAME}"]) & filters.group)
async def add_filter_cmd(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): return
    
    if message.reply_to_message and len(message.command) >= 2:
        keyword = message.command[1].lower().strip()
        reply_text = message.reply_to_message.text or message.reply_to_message.caption
        if not reply_text:
            await message.reply_text("❌ Filter reply sirf text messages par hi kaam karega!")
            return
        await db.add_filter(message.chat.id, keyword, reply_text)
        await message.reply_text(f"✅ Filter Added! Jab bhi koi `{keyword}` bolega, main reply karunga.")
    elif len(message.command) >= 3:
        keyword = message.command[1].lower().strip()
        reply_text = message.text.split(None, 2)[2]
        await db.add_filter(message.chat.id, keyword, reply_text)
        await message.reply_text(f"✅ Filter Added! Jab bhi koi `{keyword}` bolega, main reply karunga.")
    else:
        await message.reply_text("❌ **Sahi format use karein:**\n1. Kisi text ko reply karein: `/filter [keyword]`\n2. Ya direct likhein: `/filter [keyword] [reply text]`")

@bot.on_message(filters.command(["stop", f"stop@{BOT_USERNAME}"]) & filters.group)
async def stop_filter_cmd(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): return
    if len(message.command) < 2:
        await message.reply_text("❌ Kripya keyword likhein: `/stop [keyword]`")
        return
    keyword = message.command[1].lower().strip()
    deleted = await db.stop_filter(message.chat.id, keyword)
    if deleted: 
        await message.reply_text(f"🗑️ Filter `{keyword}` ko delete kar diya gaya hai.")
    else: 
        await message.reply_text("❌ Is naam ka koi filter nahi mila.")

@bot.on_message(filters.command(["stopallfilter", f"stopallfilter@{BOT_USERNAME}"]) & filters.group)
async def stop_all_filters_cmd(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): return
    await db.stop_all_filters(message.chat.id)
    await message.reply_text("🗑️ Group ke saare filters ek sath delete kar diye gaye hain.")

# --- CALLBACK ROUTING ENGINE ---
@bot.on_callback_query()
async def cb_handler(client, cb: CallbackQuery):
    if cb.data in ["modules_menu", "back_modules"]: 
        await cb.message.edit_caption(caption=SETTING_MENU_TEXT, reply_markup=SETTING_BUTTONS)
    elif cb.data == "back_start":
        text = START_TEXT.format(name=cb.from_user.first_name, owner=OWNER_USERNAME)
        await cb.message.edit_caption(caption=text, reply_markup=START_BUTTONS)
    elif cb.data == "guide_link":
        await cb.message.edit_caption(caption="🔗 **ᴀɴᴛɪ-ʟɪɴᴋ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ**\n\n● Non-admins ke links instant delete honge aur warning active hogi.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="back_modules")]]))
    elif cb.data == "guide_nsfw":
        await cb.message.edit_caption(caption="🔞 **ɴsғᴡ sᴇᴄᴜʀɪᴛʏ**\n\n● 18+ content aur words instant delete honge.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="back_modules")]]))
    elif cb.data == "guide_admin":
        await cb.message.edit_caption(caption="🛠️ **ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ**\n\nCommands: `/ban`, `/unban`, `/mute`, `/unmute`, `/warn`, `/diswarn`, `/approve`, `/disapprove`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="back_modules")]]))

# --- STRUCTURAL MODERATION ACTIONS ---
@bot.on_message(filters.command(["ban", "unban", "mute", "unmute", "warn", "diswarn", "approve", "disapprove",
                                 f"ban@{BOT_USERNAME}", f"unban@{BOT_USERNAME}", f"mute@{BOT_USERNAME}", f"unmute@{BOT_USERNAME}",
                                 f"warn@{BOT_USERNAME}", f"diswarn@{BOT_USERNAME}", f"approve@{BOT_USERNAME}", f"disapprove@{BOT_USERNAME}"]))
async def admin_commands_engine(client, message: Message):
    if message.chat.type.value == "private": return
    if not await is_admin(message.chat, message.from_user.id): return

    command = message.command[0].lower().split("@")[0]
    target_user = await extract_user(client, message)

    if not target_user:
        await message.reply_text(f"❌ Target user invalid ya missing hai.")
        return

    if await is_admin(message.chat, target_user.id) and command not in ["approve", "disapprove"]:
        await message.reply_text("❌ Main admins par action nahi le sakta!")
        return

    try:
        if command == "ban":
            await message.chat.ban_member(target_user.id)
            await message.reply_text(f"🚨 {target_user.mention} ko group se **Ban** kar diya gaya.")
        elif command == "unban":
            await message.chat.unban_member(target_user.id)
            await message.reply_text(f"✅ {target_user.mention} ko **Unban** kar diya gaya.")
        elif command == "mute":
            await message.chat.restrict_member(target_user.id, ChatPermissions(can_send_messages=False))
            await message.reply_text(f"🤐 {target_user.mention} ko **Mute** kar diya gaya.")
        elif command == "unmute":
            await message.chat.restrict_member(target_user.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
            await message.reply_text(f"🔊 {target_user.mention} ko **Unmute** kar diya gaya.")
        elif command == "warn":
            await handle_member_violation(client, message, target_user, "Admin Manual Warning")
        elif command == "diswarn":
            await db.reset_warns(message.chat.id, target_user.id)
            await message.reply_text(f"🔄 {target_user.mention} ki warnings reset kar di gayi hain.")
        elif command == "approve":
            await db.approve_user(message.chat.id, target_user.id)
            await message.reply_text(f"🟢 {target_user.mention} ko whitelist kar diya gaya hai.")
        elif command == "disapprove":
            await db.disapprove_user(message.chat.id, target_user.id)
            await message.reply_text(f"🔴 {target_user.mention} ko whitelist se hata diya gaya.")
    except Exception as e: 
        await message.reply_text(f"⚠️ Action Fail: {e}")

# --- SECURITY MONITORING + DYNAMIC INLINE FILTERS WATCHER ---
@bot.on_message(filters.group & ~filters.service, group=1)
async def security_and_filter_watcher(client, message: Message):
    if not message.from_user: return
    
    user_id = message.from_user.id
    is_user_admin = await is_admin(message.chat, user_id)
    try: is_user_approved = await db.is_approved(message.chat.id, user_id)
    except: is_user_approved = False
    
    text_content = (message.text or message.caption or "").strip()
    if not text_content: return

    try:
        current_filters = await db.get_filters(message.chat.id)
        for filter_obj in current_filters:
            if filter_obj["keyword"].lower() in text_content.lower():
                await message.reply_text(filter_obj["reply_text"])
                break  
    except Exception as fe:
        print(f"Filter Engine Exception: {fe}")

    if is_user_admin or is_user_approved: return

    if bool(re.search(r"t\.me|http|www\.", text_content)):
        try: await message.delete()
        except: pass
        await handle_member_violation(client, message, message.from_user, "Sent Forbidden Link")
        return

    if any(word in text_content.lower() for word in BAD_WORDS):
        try: await message.delete()
        except: pass
        await handle_member_violation(client, message, message.from_user, "Used Profanity/Bad words")
        return

# --- WELCOME CONTROLLERS ---
@bot.on_message(filters.command(["welcomeset", f"welcomeset@{BOT_USERNAME}"]) & filters.group)
async def set_welcome_msg(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): return
    photo_msg = message if message.photo else (message.reply_to_message if message.reply_to_message and message.reply_to_message.photo else None)
    if not photo_msg:
        await message.reply_text("❌ Custom greeting setup ke liye kisi image ke caption me command use karein!")
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
    await message.reply_text("✅ Custom Welcome image state saved database side successfully!")

@bot.on_message(filters.new_chat_members & filters.group)
async def welcome_action(client, message: Message):
    try: await db.add_served_chat(message.chat.id)
    except: pass
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

# --- MAIN RUNNER ENGINE ---
async def start_bot():
    await start_server()
    db.init_db()
    print("🤖 STARTING BOT RUNTIME CLIENT ENGAGEMENT...")
    await bot.start()
    print("✅ GUARDIAN PRO SECURITY ENGINE IS LIVE!")
    
    # Render execution context mapping
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    # Event loop context verification
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
            await db.reset_warns(chat_id, target_user.id)
            await message.reply_text(f"🤐 {target_user.mention} ko **3/3 Warnings** exceed karne par **30 Mins** ke liye mute kar diya gaya.\n\n⚠️ **Reason:** {reason}", reply_markup=get_action_buttons())
        except Exception as e:
            print(f"Auto Mute Error: {e}")
    else:
        await message.reply_text(f"⚠️ {target_user.mention} ko warning di gayi! (**{count}/3**)\n\n🚫 **Reason:** {reason}", reply_markup=get_action_buttons())

# --- USER ENTRY AND CORE ENTRY HANDLERS ---
@bot.on_message(filters.command(["start", f"start@{BOT_USERNAME}"]))
async def start_cmd(client, message: Message):
    if message.chat.type.value == "private": 
        await db.add_served_user(message.chat.id)
    else: 
        await db.add_served_chat(message.chat.id)
    text = START_TEXT.format(name=message.from_user.first_name, owner=OWNER_USERNAME)
    try: 
        await message.reply_photo(photo=Config.START_IMG, caption=text, reply_markup=START_BUTTONS)
    except: 
        await message.reply_text(text, reply_markup=START_BUTTONS)

@bot.on_message(filters.command(["setting", f"setting@{BOT_USERNAME}"]))
async def setting_cmd(client, message: Message):
    if message.chat.type.value != "private" and not await is_admin(message.chat, message.from_user.id):
        await message.reply_text("❌ Is command ko use karne ke liye aapka Group Admin hona zaroori hai!")
        return
    try: 
        await message.reply_photo(photo=Config.START_IMG, caption=SETTING_MENU_TEXT, reply_markup=SETTING_BUTTONS)
    except: 
        await message.reply_text(SETTING_MENU_TEXT, reply_markup=SETTING_BUTTONS)

# --- 🟢 FILTER COMMAND LOGIC (DYNAMIC MANAGEMENT) 🟢 ---
@bot.on_message(filters.command(["filter", f"filter@{BOT_USERNAME}"]) & filters.group)
async def add_filter_cmd(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): return
    
    if message.reply_to_message and len(message.command) >= 2:
        keyword = message.command[1].lower().strip()
        reply_text = message.reply_to_message.text or message.reply_to_message.caption
        if not reply_text:
            await message.reply_text("❌ Filter reply sirf text messages par hi kaam karega!")
            return
        await db.add_filter(message.chat.id, keyword, reply_text)
        await message.reply_text(f"✅ Filter Added! Jab bhi koi `{keyword}` bolega, main reply karunga.")
    elif len(message.command) >= 3:
        keyword = message.command[1].lower().strip()
        reply_text = message.text.split(None, 2)[2]
        await db.add_filter(message.chat.id, keyword, reply_text)
        await message.reply_text(f"✅ Filter Added! Jab bhi koi `{keyword}` bolega, main reply karunga.")
    else:
        await message.reply_text("❌ **Sahi format use karein:**\n1. Kisi text ko reply karein: `/filter [keyword]`\n2. Ya direct likhein: `/filter [keyword] [reply text]`")

@bot.on_message(filters.command(["stop", f"stop@{BOT_USERNAME}"]) & filters.group)
async def stop_filter_cmd(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): return
    if len(message.command) < 2:
        await message.reply_text("❌ Kripya keyword likhein: `/stop [keyword]`")
        return
    keyword = message.command[1].lower().strip()
    deleted = await db.stop_filter(message.chat.id, keyword)
    if deleted: 
        await message.reply_text(f"🗑️ Filter `{keyword}` ko delete kar diya gaya hai.")
    else: 
        await message.reply_text("❌ Is naam ka koi filter nahi mila.")

@bot.on_message(filters.command(["stopallfilter", f"stopallfilter@{BOT_USERNAME}"]) & filters.group)
async def stop_all_filters_cmd(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): return
    await db.stop_all_filters(message.chat.id)
    await message.reply_text("🗑️ Group ke saare filters ek sath delete kar diye gaye hain.")

# --- CALLBACK ROUTING ENGINE ---
@bot.on_callback_query()
async def cb_handler(client, cb: CallbackQuery):
    if cb.data in ["modules_menu", "back_modules"]: 
        await cb.message.edit_caption(caption=SETTING_MENU_TEXT, reply_markup=SETTING_BUTTONS)
    elif cb.data == "back_start":
        text = START_TEXT.format(name=cb.from_user.first_name, owner=OWNER_USERNAME)
        await cb.message.edit_caption(caption=text, reply_markup=START_BUTTONS)
    elif cb.data == "guide_link":
        await cb.message.edit_caption(caption="🔗 **ᴀɴᴛɪ-ʟɪɴᴋ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ**\n\n● Non-admins ke links instant delete honge aur warning active hogi.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="back_modules")]]))
    elif cb.data == "guide_nsfw":
        await cb.message.edit_caption(caption="🔞 **ɴsғᴡ sᴇᴄᴜʀɪᴛʏ**\n\n● 18+ content aur words instant delete honge.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="back_modules")]]))
    elif cb.data == "guide_admin":
        await cb.message.edit_caption(caption="🛠️ **ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ**\n\nCommands: `/ban`, `/unban`, `/mute`, `/unmute`, `/warn`, `/diswarn`, `/approve`, `/disapprove`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="back_modules")]]))

# --- STRUCTURAL MODERATION ACTIONS ---
@bot.on_message(filters.command(["ban", "unban", "mute", "unmute", "warn", "diswarn", "approve", "disapprove",
                                 f"ban@{BOT_USERNAME}", f"unban@{BOT_USERNAME}", f"mute@{BOT_USERNAME}", f"unmute@{BOT_USERNAME}",
                                 f"warn@{BOT_USERNAME}", f"diswarn@{BOT_USERNAME}", f"approve@{BOT_USERNAME}", f"disapprove@{BOT_USERNAME}"]))
async def admin_commands_engine(client, message: Message):
    if message.chat.type.value == "private": return
    if not await is_admin(message.chat, message.from_user.id): return

    command = message.command[0].lower().split("@")[0]
    target_user = await extract_user(client, message)

    if not target_user:
        await message.reply_text(f"❌ Target user invalid ya missing hai.")
        return

    if await is_admin(message.chat, target_user.id) and command not in ["approve", "disapprove"]:
        await message.reply_text("❌ Main admins par action nahi le sakta!")
        return

    try:
        if command == "ban":
            await message.chat.ban_member(target_user.id)
            await message.reply_text(f"🚨 {target_user.mention} ko group se **Ban** kar diya gaya.")
        elif command == "unban":
            await message.chat.unban_member(target_user.id)
            await message.reply_text(f"✅ {target_user.mention} ko **Unban** kar diya gaya.")
        elif command == "mute":
            await message.chat.restrict_member(target_user.id, ChatPermissions(can_send_messages=False))
            await message.reply_text(f"🤐 {target_user.mention} ko **Mute** kar diya gaya.")
        elif command == "unmute":
            await message.chat.restrict_member(target_user.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
            await message.reply_text(f"🔊 {target_user.mention} ko **Unmute** kar diya gaya.")
        elif command == "warn":
            await handle_member_violation(client, message, target_user, "Admin Manual Warning")
        elif command == "diswarn":
            await db.reset_warns(message.chat.id, target_user.id)
            await message.reply_text(f"🔄 {target_user.mention} ki warnings reset kar di gayi hain.")
        elif command == "approve":
            await db.approve_user(message.chat.id, target_user.id)
            await message.reply_text(f"🟢 {target_user.mention} ko whitelist kar diya gaya hai.")
        elif command == "disapprove":
            await db.disapprove_user(message.chat.id, target_user.id)
            await message.reply_text(f"🔴 {target_user.mention} ko whitelist se hata diya gaya.")
    except Exception as e: 
        await message.reply_text(f"⚠️ Action Fail: {e}")

# --- SECURITY MONITORING + DYNAMIC INLINE FILTERS WATCHER ---
@bot.on_message(filters.group & ~filters.service, group=1)
async def security_and_filter_watcher(client, message: Message):
    if not message.from_user: return
    
    user_id = message.from_user.id
    is_user_admin = await is_admin(message.chat, user_id)
    try: is_user_approved = await db.is_approved(message.chat.id, user_id)
    except: is_user_approved = False
    
    text_content = (message.text or message.caption or "").strip()
    if not text_content: return

    # 🟢 CHAT FILTERS PARALLEL EXECUTION TRIGGER 🟢
    try:
        current_filters = await db.get_filters(message.chat.id)
        for filter_obj in current_filters:
            if filter_obj["keyword"].lower() in text_content.lower():
                await message.reply_text(filter_obj["reply_text"])
                break  
    except Exception as fe:
        print(f"Filter Engine Exception: {fe}")

    if is_user_admin or is_user_approved: return

    # Anti-Link Validation Logic
    if bool(re.search(r"t\.me|http|www\.", text_content)):
        try: await message.delete()
        except: pass
        await handle_member_violation(client, message, message.from_user, "Sent Forbidden Link")
        return

    # Anti-Abuse Profanity Logic
    if any(word in text_content.lower() for word in BAD_WORDS):
        try: await message.delete()
        except: pass
        await handle_member_violation(client, message, message.from_user, "Used Profanity/Bad words")
        return

# --- WELCOME CONTROLLERS ---
@bot.on_message(filters.command(["welcomeset", f"welcomeset@{BOT_USERNAME}"]) & filters.group)
async def set_welcome_msg(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): return
    photo_msg = message if message.photo else (message.reply_to_message if message.reply_to_message and message.reply_to_message.photo else None)
    if not photo_msg:
        await message.reply_text("❌ Custom greeting setup ke liye kisi image ke caption me command use karein!")
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
    await message.reply_text("✅ Custom Welcome image state saved database side successfully!")

@bot.on_message(filters.new_chat_members & filters.group)
async def welcome_action(client, message: Message):
    try: await db.add_served_chat(message.chat.id)
    except: pass
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

# --- GLOBAL SINGLE LOOP EXECUTION ENGINE ---
async def start_bot():
    # 1. Pehle port framework register karo (Render demands)
    await start_server()
    
    # 2. Lazy loading ke through db connection initialize karo safe loop pe
    db.init_db()
    
    # 3. Ab pure control ke sath Pyrogram start karo
    print("🤖 STARTING BOT RUNTIME CLIENT ENGAGEMENT...")
    await bot.start()
    print("✅ GUARDIAN PRO SECURITY ENGINE IS LIVE!")
    
    # Keeping the main loop alive forever on Render
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    # Natively master loop control to fix "no current event loop" crash
    asyncio.run(start_bot())
