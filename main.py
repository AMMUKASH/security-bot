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

# --- WEB SERVER SETUP FOR RENDER PORT BINDING ---
from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is Running and Alive 24/7!")

async def start_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', Config.PORT)
    await site.start()

# --- ADVANCED USER EXTRACTION ENGINE ---
# Yeh function handle karega: Reply, Username, Mention, aur User ID
async def extract_user(client, message: Message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    
    if len(message.command) < 2:
        return None
        
    user_to_find = message.command[1]
    
    # Agar User ID (integer) di gayi hai
    if user_to_find.isdigit():
        try:
            return await client.get_users(int(user_to_find))
        except Exception:
            return None
            
    # Agar username ya mention (@username) diya gaya hai
    if user_to_find.startswith("@"):
        user_to_find = user_to_find.replace("@", "")
    try:
        return await client.get_users(user_to_find)
    except Exception:
        return None

# --- ADVANCED BUTTONS PARSER FOR WELCOME ---
def parse_buttons(text):
    if not text: 
        return None
    try:
        kb = []
        # Markdown button format check: [Button Name | https://link.com]
        matches = re.findall(r'\[([^\]]+)\|([^\]]+)\]', text)
        for name, url in matches:
            kb.append([InlineKeyboardButton(name.strip(), url=url.strip())])
        return kb if kb else None
    except Exception: 
        return None

async def is_admin(chat, user_id):
    if chat.type.value in ["private"]: 
        return True
    try:
        m = await bot.get_chat_member(chat.id, user_id)
        return m.status.value in ["administrator", "owner"]
    except Exception: 
        return False

# --- COMMAND HANDLERS ---

@bot.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    text = (
        "╭────── • 𝐆𝐔𝐀𝐑𝐃𝐈𝐀𝐍 𝐏𝐑𝐎 • ──────╮\n"
        "│      ✨ **ADVANCED GROUP SECURITY** ✨      \n"
        "├──────────────────────────────┤\n"
        "│ 🛡️ **BIO LINK PROTECTION**\n"
        "│  └ Warn + Auto Mute (30ᵐⁱⁿ)\n"
        "│\n"
        "│ 🔗 **ANTI LINK SYSTEM**\n"
        "│  └ Instant Link Removal\n"
        "│\n"
        "│ 🚫 **ANTI ABUSE PROTECTION**\n"
        "│  └ Smart Language Filter\n"
        "│\n"
        "│ 📥 **FORWARD CONTROL**\n"
        "│  └ Auto Forward Delete\n"
        "│\n"
        "│ 📝 **EDIT SECURITY**\n"
        "│  └ Edited Link Detection\n"
        "│\n"
        "│ 🗑️ **MEDIA CLEANUP**\n"
        "│  └ Silent Auto Delete (50s)\n"
        "├──────────────────────────────┤\n"
        "│ ⚡ _Fast • Stable • Professional Grade_      \n"
        "╰──────────────────────────────╯"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✨ Add Me To Your Group ✨", url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true")],
        [
            InlineKeyboardButton("📢 Channel", url=f"https://t.me/{Config.UPDATE_CH}"),
            InlineKeyboardButton("🛠️ Help Menu", callback_data="help_menu")
        ]
    ])
    if message.chat.type.value == "private":
        await message.reply_photo(photo=Config.START_IMG, caption=text, reply_markup=buttons)
    else:
        await message.reply_text("Bot active hai! Mujhe PM me start karke Help Menu check karein.", reply_markup=buttons)

@bot.on_callback_query(filters.regex("^help_menu$|^back_start$"))
async def cb_handler(client, cb: CallbackQuery):
    if cb.data == "help_menu":
        help_text = (
            "🛠️ **GUARDIAN PRO - HELP MENU & GUIDE**\n\n"
            "👮 **Admin Commands (Supports: Reply, Username, ID, Mention):**\n"
            "• `/ban` - User ko group se ban karein\n"
            "• `/unban` - User ko unban karein\n"
            "• `/mute` - User ko mute karein\n"
            "• `/unmute` - User ko unmute karein\n"
            "• `/warn` - User ko warning dein (3 warns = Ban)\n"
            "• `/diswarn` - User ki ek warning kam karein\n"
            "• `/approve` - User ko whitelist karein (Bypass rules)\n"
            "• `/disapprove` - Whitelist se hatayein\n\n"
            "⚙️ **Welcome Customization:**\n"
            "• `/welcomeset [text]` - Photo par reply karke ya seedhe photo ke caption me likhein\n"
            "• `/welcomereset` - Welcome message band karein\n\n"
            "🔍 **Filters System:**\n"
            "• `/filter [keyword] [reply text]` - Naya trigger text set karein\n"
            "• `/stop [keyword]` - Filter delete karein\n"
            "• `/stopallfilter` - Saare filters clear karein"
        )
        await cb.message.edit_caption(caption=help_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back_start")]]))
    elif cb.data == "back_start":
        text = (
            "╭────── • 𝐆𝐔𝐀𝐑𝐃𝐈𝐀𝐍 𝐏𝐑𝐎 • ──────╮\n"
            "│      ✨ **ADVANCED GROUP SECURITY** ✨      \n"
            "╰──────────────────────────────╯"
        )
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ Add Me To Your Group ✨", url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true")],
            [InlineKeyboardButton("📢 Channel", url=f"https://t.me/{Config.UPDATE_CH}"), InlineKeyboardButton("🛠️ Help Menu", callback_data="help_menu")]
        ])
        await cb.message.edit_caption(caption=text, reply_markup=buttons)

# --- ADVANCED WELCOME SET UP ---
@bot.on_message(filters.command("welcomeset") & filters.group)
async def set_welcome_msg(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): 
        return
        
    # Check karega agar photo par reply hai ya khud command ke sath hi photo send ki gayi hai
    photo_msg = None
    if message.photo:
        photo_msg = message
    elif message.reply_to_message and message.reply_to_message.photo:
        photo_msg = message.reply_to_message

    if not photo_msg:
        await message.reply_text("❌ Is command ko use karne ke liye kisi photo par reply karein, ya photo send karte waqt caption me `/welcomeset [text]` likhein!")
        return

    fid = photo_msg.photo.file_id
    full_text = message.text or message.caption or ""
    text_w = full_text.replace("/welcomeset", "").strip()
    
    # Caption aur buttons ko isolate karne ke liye logic
    cap = text_w
    btn_raw = ""
    if "[" in text_w and "]" in text_w:
        start_idx = text_w.find("[")
        cap = text_w[:start_idx].strip()
        btn_raw = text_w[start_idx:].strip()

    await db.set_welcome(message.chat.id, fid, cap, btn_raw if btn_raw else None)
    await message.reply_text("✅ **Custom Welcome Image, Caption aur Buttons successfully save ho gaye hain!**")

@bot.on_message(filters.command("welcomereset") & filters.group)
async def reset_welcome_msg(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): 
        return
    await db.reset_welcome(message.chat.id)
    await message.reply_text("🗑️ Welcome message completely reset aur disable kar diya gaya hai.")

# --- DYNAMIC ACTION CONTROLS (BAN, MUTE, WARN, APPROVE) ---
@bot.on_message(filters.command(["ban", "mute", "warn", "approve", "disapprove", "diswarn"]) & filters.group)
async def admin_actions(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): 
        return
        
    target = await extract_user(client, message)
    if not target:
        await message.reply_text("❌ **Galat Format!** Please user ke message par reply karein, ya command ke aage `@username`, `User ID` ya `mention` likhein.")
        return
        
    cmd = message.command[0]

    if cmd == "ban":
        try:
            await client.ban_chat_member(message.chat.id, target.id)
            await message.reply_text(f"🛑 {target.mention} ko group se block (Ban) kar diya gaya.")
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")
            
    elif cmd == "mute":
        try:
            await client.restrict_chat_member(message.chat.id, target.id, permissions=ChatPermissions(can_send_messages=False))
            await message.reply_text(f"🔇 {target.mention} ko completely mute kar diya gaya hai.")
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")
            
    elif cmd == "warn":
        count = await db.add_warn(message.chat.id, target.id)
        if count >= 3:
            try:
                await client.ban_chat_member(message.chat.id, target.id)
                await message.reply_text(f"🔥 {target.mention} ke 3/3 warnings poore hone par automatic Ban kar diya gaya.")
            except Exception:
                await message.reply_text(f"⚠️ {target.mention} ke 3 warnings ho gaye hain par admin privileges ki wajah se ban nahi ho saka.")
        else:
            await message.reply_text(f"⚠️ {target.mention} ko warning di gayi. (Total Warns: {count}/3)")
            
    elif cmd == "diswarn":
        count = await db.remove_warn(message.chat.id, target.id)
        await message.reply_text(f"✅ {target.mention} ki ek warning kam kar di gayi hai. (Remaining Warns: {count})")
        
    elif cmd == "approve":
        await db.approve_user(message.chat.id, target.id)
        await message.reply_text(f"🟢 {target.mention} whitelist (approve) ho gaya hai. Ab ispar anti-link filters work nahi karenge.")
        
    elif cmd == "disapprove":
        await db.disapprove_user(message.chat.id, target.id)
        await message.reply_text(f"🔴 {target.mention} ko whitelisted status se remove kar diya gaya.")

@bot.on_message(filters.command(["unban", "unmute"]) & filters.group)
async def admin_unactions(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): 
        return
        
    target = await extract_user(client, message)
    if not target:
        await message.reply_text("❌ Please user ke message par reply karein ya command ke aage `@username` / `User ID` dalein.")
        return
        
    cmd = message.command[0]
    
    if cmd == "unban":
        await client.unban_chat_member(message.chat.id, target.id)
        await message.reply_text(f"✅ {target.mention} successfully unban ho gaya hai.")
    elif cmd == "unmute":
        await client.restrict_chat_member(message.chat.id, target.id, permissions=ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
        await message.reply_text(f"🔊 {target.mention} successfully unmute ho gaya hai!")

# --- FILTER SYSTEM ---
@bot.on_message(filters.command("filter") & filters.group)
async def set_filter(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): 
        return
    if len(message.command) < 3:
        await message.reply_text("❌ Format galat hai. Use karein: `/filter [keyword] [reply text]`")
        return
    keyword = message.command[1].lower()
    reply_text = message.text.split(None, 2)[2]
    await db.add_filter(message.chat.id, keyword, reply_text)
    await message.reply_text(f"📥 Filter save ho gaya hai trigger word: `{keyword}` ke liye.")

@bot.on_message(filters.command("stop") & filters.group)
async def stop_one_filter(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): 
        return
    if len(message.command) < 2:
        await message.reply_text("❌ Triger name dalein: `/stop [keyword]`")
        return
    kw = message.command[1].lower()
    deleted = await db.stop_filter(message.chat.id, kw)
    if deleted: 
        await message.reply_text(f"🗑️ `{kw}` filter band kar diya gaya hai.")
    else: 
        await message.reply_text("❌ Aisa koi filter group me active nahi hai.")

@bot.on_message(filters.command("stopallfilter") & filters.group)
async def stop_all_f(client, message: Message):
    if not await is_admin(message.chat, message.from_user.id): 
        return
    await db.stop_all_filters(message.chat.id)
    await message.reply_text("💥 Is group ke saare custom filters delete kar diye gaye hain.")

# --- NEW CHAT MEMBER JOIN ACTION ---
@bot.on_message(filters.new_chat_members & filters.group)
async def welcome_action(client, message: Message):
    w_data = await db.get_welcome(message.chat.id)
    if not w_data: 
        return
    cnt = await client.get_chat_members_count(message.chat.id)
    for m in message.new_chat_members:
        un = f"@{m.username}" if m.username else "No Username"
        
        # Tags formatting fallback engine
        cap = w_data["caption"]
        cap = cap.replace("{mention}", m.mention or m.first_name)
        cap = cap.replace("{name}", m.first_name or "User")
        cap = cap.replace("{fullname}", f"{m.first_name} {m.last_name or ''}".strip())
        cap = cap.replace("{id}", str(m.id))
        cap = cap.replace("{username}", un)
        cap = cap.replace("{title}", message.chat.title)
        cap = cap.replace("{count}", str(cnt))
        
        btns = parse_buttons(w_data.get("buttons"))
        markup = InlineKeyboardMarkup(btns) if btns else None
        try: 
            await client.send_photo(chat_id=message.chat.id, photo=w_data["file_id"], caption=cap, reply_markup=markup)
        except Exception: 
            pass

# --- AUTO WATCHER (FILTERS, SECURITY & PROTECTION) ---
@bot.on_message(filters.group & ~filters.service)
async def watcher(client, message: Message):
    if not message.from_user: 
        return
    if await db.is_approved(message.chat.id, message.from_user.id) or await is_admin(message.chat, message.from_user.id):
        return

    text_content = message.text or message.caption or ""
    
    # Custom Triggers Engine Check
    all_filters = await db.get_filters(message.chat.id)
    for f in all_filters:
        if f["keyword"] in text_content.lower():
            await message.reply_text(f["reply_text"])
            return

    # Basic URL/Link Security
    if re.search(r"t\.me|http|www\.", text_content):
        try: 
            await message.delete()
            return
        except Exception: 
            pass

    # Anti-Forward Control
    if message.forward_date:
        try: 
            await message.delete()
            return
        except Exception: 
            pass

# --- MODERN ASYNC LOOP EXECUTION ENGINE ---
async def main():
    await start_server()
    print("🌐 Web Server active on port configuration!")
    await bot.start()
    print("🤖 Guardian Pro Security Engine Started Successfully!")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot deployment stopped safely.")
