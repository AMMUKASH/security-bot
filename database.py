import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

# Render aur VPS par DNS timeouts se bachne ke liye SSL parameters add kiye hain
try:
    client = AsyncIOMotorClient(Config.MONGO_URL, serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True)
    db = client["Group_Secu_Bot_DB"]
except Exception as e:
    print(f"❌ DATABASE CRITICAL ERROR: {e}")

# Collections
settings_col = db["group_settings"]
welcome_col = db["welcome_settings"]
filters_col = db["chat_filters"]
warns_col = db["user_warns"]
approved_col = db["approved_users"]
served_users_col = db["served_users"]
served_chats_col = db["served_chats"]

# Welcome Database
async def set_welcome(chat_id, file_id, caption, buttons=None):
    await welcome_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"file_id": file_id, "caption": caption, "buttons": buttons}},
        upsert=True
    )

async def get_welcome(chat_id):
    return await welcome_col.find_one({"chat_id": chat_id})

async def reset_welcome(chat_id):
    await welcome_col.delete_one({"chat_id": chat_id})

# Filters Database
async def add_filter(chat_id, keyword, reply_text):
    await filters_col.update_one(
        {"chat_id": chat_id, "keyword": keyword.lower().strip()},
        {"$set": {"reply_text": reply_text}},
        upsert=True
    )

async def get_filters(chat_id):
    cursor = filters_col.find({"chat_id": chat_id})
    return await cursor.to_list(length=100)

async def stop_filter(chat_id, keyword):
    res = await filters_col.delete_one({"chat_id": chat_id, "keyword": keyword.lower().strip()})
    return res.deleted_count > 0

async def stop_all_filters(chat_id):
    await filters_col.delete_many({"chat_id": chat_id})

# Warns Database
async def add_warn(chat_id, user_id):
    res = await warns_col.find_one({"chat_id": chat_id, "user_id": user_id})
    count = (res.get("count", 0) + 1) if res else 1
    await warns_col.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"count": count}},
        upsert=True
    )
    return count

# Main.py ke sync ke liye reset_warns name fix kiya gaya
async def reset_warns(chat_id, user_id):
    await warns_col.delete_one({"chat_id": chat_id, "user_id": user_id})

async def remove_warn(chat_id, user_id):
    res = await warns_col.find_one({"chat_id": chat_id, "user_id": user_id})
    if not res or res.get("count", 0) == 0:
        return 0
    new_count = res["count"] - 1
    await warns_col.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"count": new_count}}
    )
    return new_count

# Approved Users Database
async def approve_user(chat_id, user_id):
    await approved_col.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"approved": True}},
        upsert=True
    )

async def disapprove_user(chat_id, user_id):
    await approved_col.delete_one({"chat_id": chat_id, "user_id": user_id})

async def is_approved(chat_id, user_id):
    res = await approved_col.find_one({"chat_id": chat_id, "user_id": user_id})
    return bool(res)

# Broadcast System Stats tracking data methods
async def add_served_user(user_id):
    await served_users_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

async def get_served_users():
    return await served_users_col.find().to_list(length=5000)

async def add_served_chat(chat_id):
    await served_chats_col.update_one({"chat_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True)

async def get_served_chats():
    return await served_chats_col.find().to_list(length=5000)

# Default Settings
async def get_settings(chat_id):
    settings = await settings_col.find_one({"chat_id": chat_id})
    if not settings:
        settings = {"chat_id": chat_id, "anti_link": True, "anti_abuse": True, "forward_control": True, "edit_security": True}
        await settings_col.insert_one(settings)
    return settings
