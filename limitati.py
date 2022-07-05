# Source creata da @godxk per @sourceskiddate
from telethon import TelegramClient, events
from telethon import events, errors, Button
import os
api_id = 17222139
api_hash= "ffd330fed81cf05cc639f6b8ff71389b"
mybot = TelegramClient("bot_limitati", api_id, api_hash)
status = "null"
admin_id = 1999796584
client = mybot
client.start()

@client.on(events.NewMessage)
async def my_event_handler(event):
    
    client.parse_mode = 'html'
    text = event.text.split(' ')
    filer = open("chat.txt", "r")
    data = filer.read()
    
    
    if(event.sender_id == admin_id):
        if(text[0] == "/mex"):
            idutente = int(text[1])
            
            messaggio1 = event.text.replace(text[0], "")
            messaggio = messaggio1.replace(text[1], "")
            await client.send_message(int(idutente), "👮 Admin: " + str(messaggio.lstrip()))
            await event.respond("Messaggio inviato con successo!")
    else:
        if(data.__contains__(str(event.sender_id))):
            await client.send_message(int(admin_id), "MESSAGGIO DA: <pre>" + str(event.sender_id) + "</pre>" + " " + event.text)


@mybot.on(events.NewMessage(outgoing=False,pattern="/start"))
async def startBot(event):
    await event.respond(f"👋Ciao [{event.sender.first_name}], benvenuto nel Limitati Bot di @ScognaSeLLer 🤖",
    buttons=[
        [
                Button.inline("💬 Avvia Chat", data="chat")
        ],
        [
                 Button.url("👮 Developer", url="t.me/ScognaSeLLer")
        ],
    ])   
    
@mybot.on(events.callbackquery.CallbackQuery(data="home"))
async def homeshopbot(event):
    await event.edit(f"👋Ciao [{event.sender.first_name}], benvenuto nel Limitati Bot di @ScognaSeLLer 🤖",
    buttons=[
        [
                Button.inline("💬 Avvia Chat", data="chat")
        ],
        [
                 Button.url("👮 Developer", url="t.me/ScognaSeLLer")
        ],
    ]) 

@mybot.on(events.callbackquery.CallbackQuery(data="chat"))
async def chatoff(event):
    filew = open("chat.txt", "w")
    filer = open("chat.txt", "r")
    
    data = filer.read()
    
    filew.write(data + "\n" + str(event.sender_id))
    
    filew.close()
    filer.close()
    
    await event.edit("ℹ️ Per terminare la chat live premi sul pulsante sotto-stante",
    buttons=[
        [
            Button.inline("❌ Chiudi", data="chiudi")
        ]
    ])
    
    

@mybot.on(events.callbackquery.CallbackQuery(data="chiudi"))
async def closechat(event):
    filew = open("chat.txt", "w")
    filer = open("chat.txt", "r")
    data = filer.read()
    filew.write(data.replace(str(event.sender_id), "".lstrip()))
    filew.close()
    filer.close()
    
    await event.respond("✔️ Chat terminata",
    buttons=[
        [
            Button.inline("🔙 Torna alla Home", data="home")
        ]
    ])

#riavvio bot in beta#
@mybot.on(events.NewMessage(func=lambda e: e.is_private,pattern="/riavviabot"))
async def riavvio(event):
    await event.delete()
    await event.respond("Premi il pulsante sottostante per riavviare il bot.",
    buttons=[
        [
            Button.inline("Riavvia il Bot", data="riavvio"),
            Button.inline("Chiudi", data="chiudi")
        ]
    ])

@mybot.on(events.callbackquery.CallbackQuery(data="riavvio"))
async def ex(event):
    import os, sys, threading
    os.system("clear")
    os.execl(sys.executable, sys.executable, *sys.argv)
    thereading.Thread(target=_restart, args=(bot, msg)).start()

@mybot.on(events.callbackquery.CallbackQuery(data="chiudi"))
async def chiuditastiera(event):
    await event.delete()

print("BOT AVVIATO")

mybot.start()
mybot.run_until_disconnected()
