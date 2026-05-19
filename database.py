import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

# Mongo Client ko global variable banayenge par initialize lazy-loading se karenge
# Taaki jab tak main loop start na ho, tab tak ye loop dhoondhne ke chakkar me crash na kare.
client = None
db = None

def init_db():
    global client, db
    if client is None:
        client = AsyncIOMotorClient(
            Config.MONGO_URL,
            serverSelectionTimeoutMS=5000,
            tlsAllowInvalidCertificates=True
        )
        db = client["Group_Secu_Bot_DB"]
        print("✨ MongoDB Client successfully initialized inside Async Loop!")

# Helper wrapper jo collections ko dynamically point karega safely
def get_collection(name):
    init_db()
    return db[name]

# --- WELCOME MODULE METHODS ---
async def set_welcome(chat_id, file_id, caption, buttons=None):
    col = get_collection("welcome_settings")
    await col.update_one(
        {"chat_id": chat_id},
        {"$set": {"file_id": file_id, "caption": caption, "buttons": buttons}},
        upsert=True
    )

async def get_welcome(chat_id):
    col = get_collection("welcome_settings")
    return await col.find_one({"chat_id": chat_id})

async def reset_welcome(chat_id):
    col = get_collection("welcome_settings")
    await col.delete_one({"chat_id": chat_id})

# --- DYNAMIC FILTERS MODULE METHODS ---
async def add_filter(chat_id, keyword, reply_text):
    col = get_collection("chat_filters")
    await col.update_one(
        {"chat_id": chat_id, "keyword": keyword.lower().strip()},
        {"$set": {"reply_text": reply_text}},
        upsert=True
    )

async def get_filters(chat_id):
    col = get_collection("chat_filters")
    cursor = col.find({"chat_id": chat_id})
    return await cursor.to_list(length=100)

async def stop_filter(chat_id, keyword):
    col = get_collection("chat_filters")
    res = await col.delete_one({"chat_id": chat_id, "keyword": keyword.lower().strip()})
    return res.deleted_count > 0

async def stop_all_filters(chat_id):
    col = get_collection("chat_filters")
    await col.delete_many({"chat_id": chat_id})

# --- WARNING MODULE METHODS ---
async def add_warn(chat_id, user_id):
    col = get_collection("user_warns")
    res = await col.find_one({"chat_id": chat_id, "user_id": user_id})
    count = (res.get("count", 0) + 1) if res else 1
    await col.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"count": count}},
        upsert=True
    )
    return count

async def reset_warns(chat_id, user_id):
    col = get_collection("user_warns")
    await col.delete_one({"chat_id": chat_id, "user_id": user_id})

async def remove_warn(chat_id, user_id):
    col = get_collection("user_warns")
    res = await col.find_one({"chat_id": chat_id, "user_id": user_id})
    if not res or res.get("count", 0) == 0:
        return 0
    new_count = res["count"] - 1
    await col.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"count": new_count}}
    )
    return new_count

# --- APPROVED/WHITELIST MODULE METHODS ---
async def approve_user(chat_id, user_id):
    col = get_collection("approved_users")
    await col.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"approved": True}},
        upsert=True
    )

async def disapprove_user(chat_id, user_id):
    col = get_collection("approved_users")
    await col.delete_one({"chat_id": chat_id, "user_id": user_id})

async def is_approved(chat_id, user_id):
    col = get_collection("approved_users")
    res = await col.find_one({"chat_id": chat_id, "user_id": user_id})
    return bool(res)

# --- BROADCAST & STATS TRACKING METHODS ---
async def add_served_user(user_id):
    col = get_collection("served_users")
    await col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

async def get_served_users():
    col = get_collection("served_users")
    return await col.find().to_list(length=5000)

async def add_served_chat(chat_id):
    col = get_collection("served_chats")
    await col.update_one({"chat_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True)

async def get_served_chats():
    col = get_collection("served_chats")
    return await col.find().to_list(length=5000)

# --- GLOBAL CHAT SETTINGS ---
async def get_settings(chat_id):
    col = get_collection("group_settings")
    settings = await col.find_one({"chat_id": chat_id})
    if not settings:
        settings = {"chat_id": chat_id, "anti_link": True, "anti_abuse": True, "forward_control": True, "edit_security": True}
        await col.insert_one(settings)
    return settings
