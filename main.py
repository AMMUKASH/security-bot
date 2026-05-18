import asyncio
from fastapi import FastAPI
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
import uvicorn

# --- CONFIGURATION (YOUR DATA INTEGRATED) ---
API_ID = 38138069        
API_HASH = "2ed313ebcc45cbcf65d1fc736ec71681"  
BOT_TOKEN = "8469456367:AAHnPUxDa1246b3O4p0yHkM4CKkIfSsToW0" 
START_IMG = "https://files.catbox.moe/ko5i86.jpg"

# All your channels with stylish names and usernames extracted from links
CHANNELS = [
    {"name": "ɪɴᴅɪᴀɴ ᴍᴍꜱ💋", "username": "About_Genious"},
    {"name": "ʀᴇᴀʟ ʜɪɴᴅɪ ᴍᴍꜱ💋", "username": "Tele_links_update"},
    {"name": "ꜰᴏʀᴄᴇ ꜰᴜᴄᴋ💋", "username": "Seling_Proff"},
    {"name": "ᴍᴏᴍ & ꜱᴏɴ💋💋", "username": "Genu_Bot_Support"},
    {"name": "ᴄʜɪʟᴅ ꜱᴇx💋💋", "username": "Friend_Forevr"},
    {"name": "ꜱᴛᴇᴩ ᴍᴏᴍ ꜱᴏɴ💋💋", "username": "SticrAura"},
    {"name": "ꜱᴄʜᴏᴏʟ ɪɴᴅɪᴀɴ ɢɪʀʟ💋💋", "username": "Villain_Loves"},
    {"name": "ɪɴᴅɪᴀɴ ᴅᴇꜱɪ ᴀᴜɴᴛʏ💋💋", "username": "Sexi_Aura"},
    {"name": "ʙʜᴀʙʜɪ ʟᴏᴠᴇ💋💋", "username": "Usertag_update"},
    {"name": "ᴊᴀᴩᴀɴᴇᴇꜱ ɢɪʀʟ💋💋💋", "username": "MoviesHub_Verse"},
    {"name": "ʀᴇᴀʟ ᴍᴍꜱ ᴠɪʀᴀʟ💋💋", "username": "K8vin_Hub"},
    {"name": "ᴠɪʀᴀʟ ᴠɪᴅᴇᴏꜱ💋💋💋", "username": "Animyedit"},
    {"name": "ꜱᴜɴɴʏ ʟᴇᴏɴᴇ💋💋", "username": "ll_CEO_OF_YOO_ll"}
]
# --------------------------------------------

# FastAPI App Initialize
app = FastAPI()

# Pyrogram Bot Initialize
bot = Client("insta_mms_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.get("/")
def hello_world():
    return {"status": "Bot is running 24/7", "username": "@Insta_mmmmmsss_bot"}

# --- BOT LOGIC ---
async def check_user_joined(client, user_id):
    not_joined = []
    for channel in CHANNELS:
        try:
            await client.get_chat_member(channel["username"], user_id)
        except UserNotParticipant:
            not_joined.append(channel)
        except Exception:
            # Agar bot kisi channel me admin nahi hoga, toh check skip ho jayega
            continue
    return not_joined

@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    user_id = message.from_user.id
    not_joined_channels = await check_user_joined(client, user_id)
    
    if not_joined_channels:
        buttons = []
        # Har 2 channels ko ek line (row) me dikhane ke liye logic
        row = []
        for channel in not_joined_channels:
            row.append(InlineKeyboardButton(text=channel['name'], url=f"https://t.me/{channel['username']}"))
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
            
        # Try Again button sabse last me single line me
        buttons.append([InlineKeyboardButton(text="🔄 Checked / Try Again", callback_data="check_again")])
        
        await message.reply_photo(
            photo=START_IMG,
            caption=(
                "👋 **Welcome!**\n\n"
                "Bot ko use karne ke liye aapko hamare sabhi channels ko join karna padega.\n"
                "Neeche diye gaye sabhi buttons par click karke join karein 👇"
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await message.reply_photo(
            photo=START_IMG,
            caption=f"✨ **Welcome back!**\n\nAapne saare channels join kar liye hain. Ab aap bot use kar sakte hain!"
        )

@bot.on_callback_query(filters.regex("check_again"))
async def check_again_callback(client, callback_query):
    user_id = callback_query.from_user.id
    not_joined_channels = await check_user_joined(client, user_id)
    
    if not_joined_channels:
        await callback_query.answer(text="❌ Aapne abhi bhi saare channels join nahi kiye hain! Kripya sabhi ko join karein.", show_alert=True)
    else:
        await callback_query.answer("✅ Thank you! Verification successful.", show_alert=False)
        await callback_query.edit_message_caption(
            caption="✨ **Aapka swagat hai!**\n\nVerification safal rha. Ab aap bot ke saare features use kar sakte hain!"
        )

# --- SERVER & BOT LIFECYCLE ---
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.start())
    print("🤖 @Insta_mmmmmsss_bot started in background...")

@app.on_event("shutdown")
async def shutdown_event():
    await bot.stop()
    print("🤖 Bot stopped.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
