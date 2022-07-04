import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 17222139
API_HASH = "ffd330fed81cf05cc639f6b8ff71389b"
BOT_TOKEN = "5412156710:AAHuunbRDAyFs5TPfseSLhLQnNF1WHjXJPo" #INSERISCI BOT TOKEN
ADMIN = [1999796584] #INSERISCI UNO O PIU' FOUNDER ID SEPARATI DA VIRGOLE               

inChat = []

bot = Client("session", API_ID, API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.private)
async def commandsManager(client, message):
    global ADMIN, inChat
    if message.text != None and message.text == "/start":
        if message.chat.username == None:
            if message.chat.last_name == None:
                mention = f"[{message.chat.first_name}](tg://user?id={message.chat.id})"
            else:
                mention = f"[{message.chat.first_name} {message.chat.last_name}](tg://user?id={message.chat.id})"
        else:
            mention = "@" + message.chat.username
        await message.reply_text(f"Benvenuto {mention}, spero che ti piaccia il mio limitati bot\nSarò lieto di accoglierti!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 Chat Diretta 💬", "chat"), InlineKeyboardButton("✏️ FeedBack ✏️", url="https://t.me/ArdaHubFeed")], [InlineKeyboardButton("🌍 Gruppo 🌍", url="https://t.me/CompravenditaByArdaHub")]]))
    elif message.from_user.id in ADMIN:
        if message.reply_to_message != None and message.reply_to_message.entities != None:
            check = False
            for ent in message.reply_to_message.entities:
                if ent.type == "text_mention":
                    check, user = True, ent.user
                    break
            if check:
                await message.forward(user.id)
                msg = await message.reply_text("__Risposta Inviata!__", quote=True)
                await asyncio.sleep(1)
                await msg.delete()

        else:
            await message.reply_text("__Rispondi al messaggio contenente il permalink dell' utente per inviare una risposta!__", quote=False)
    elif message.from_user.id in inChat:
        if message.chat.last_name == None:
            mention = f"[{message.chat.first_name}](tg://user?id={message.chat.id})"
        else:
            mention = f"[{message.chat.first_name} {message.chat.last_name}](tg://user?id={message.chat.id})"
        if message.media:
            for admin in ADMIN:
                try:
                    msg = await message.forward(admin)
                    await msg.reply_text(f"__Messaggio inviato da__ {mention}__!__", quote=True)
                except:
                    pass
        else:
            for admin in ADMIN:
                try:
                    await client.send_message(admin, f"{mention}: {message.text}")
                except:
                    pass
        check = await message.reply_text("__Messaggio Inviato!__", quote=True)
        await asyncio.sleep(1)
        await check.delete()
    else:
        if message.media:
            await message.reply_text("__Hai provato ad inviare un media ma non hai aperto la chat!__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 Avvia Chat 💬", "chat")]]))
        else:
            await message.reply_text(f"__Hai provato ad inviare__ `{message.text}` __ma non hai aperto la chat!__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 Avvia Chat 💬", "chat")]]))
        
    

@bot.on_callback_query()
async def callbackQueryManager(client, query):
    global ADMIN, inChat
    if query.data == "back":
        if query.message.chat.username == None:
            if query.message.chat.last_name == None:
                mention = f"[{query.message.chat.first_name}](tg://user?id={query.message.chat.id})"
            else:
                mention = f"[{query.message.chat.first_name} {query.message.chat.last_name}](tg://user?id={query.message.chat.id})"
        else:
            mention = "@" + query.message.chat.username
        await query.message.edit(f"Benvenuto {mention}, spero che ti piaccia il mio limitati bot\nSarò lieto di accoglierti!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 Chat Diretta 💬", "chat"), InlineKeyboardButton("✏️ FeedBack ✏️", url="https://t.me/ArdaHubFeed")], [InlineKeyboardButton("🌍 Gruppo 🌍", url="https://t.me/CompravenditaByArdaHub")]]))
    elif query.data == "chat":
        if not query.from_user.id in ADMIN:
            if not query.from_user.id in inChat:
                inChat.append(query.from_user.id)
                await query.message.edit("**[✅] Chat Avviata! [✅]**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Chiudi ❌", "close")], [InlineKeyboardButton("🔙 Indietro", "back")]]))
            else:
                await query.message.edit("**❌ Sei già in chat! ❌**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Chiudi ❌", "close")], [InlineKeyboardButton("🔙 Indietro", "back")]]))
        else:
            await query.answer("❌ Sei admin disabile non puoi avviare la chat!", show_alert=True)
    elif query.data == "close":
        if not query.from_user.id in ADMIN:
            if query.from_user.id in inChat:
                inChat.remove(query.from_user.id)
                await query.message.edit("**[❌] Chat Chiusa!** [❌]", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Avvia ✅", "chat")], [InlineKeyboardButton("🔙 Indietro", "back")]]))
            else:
                await query.message.edit("**❌ Non sei in chat! ❌**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Avvia ✅", "chat")], [InlineKeyboardButton("🔙 Indietro", "back")]]))
   


print("Bot Avviato Correttamente!")

bot.run()