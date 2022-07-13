import os, json, asyncio, sys, logging
from telethon import TelegramClient, events, Button
from telethon.sync import TelegramClient as TMPTelegramClient

logging.basicConfig(level=logging.WARNING)

API_KEY = 9782603

API_HASH = '62bf09866604292ae428ebb67a359858'

SUPERADMIN = 1999796584

bot = TelegramClient("bot2", API_KEY, API_HASH)


# evento triggerato alla ricezione di un messaggio


@bot.on(events.NewMessage(incoming=True))
async def NewMessages(msg):
    # Se il messaggio e' uguale a /start invia il messaggio sottostante
    if msg.text == '/start':
        users = json.load(open('users.json'))
        # Se l'utente non e' registrato:
        if not str(msg.sender.id) in users:
            users[msg.sender.id] = {'open': False, 'admin': False, 'ban': False}
            json.dump(users, open('users.json', 'w'))
            await msg.respond(f'Ciao {msg.sender.username} benvenuto in questo bot!', buttons=[[Button.inline('AVVIA CHAT', 'start_chat')]])
        # Se l'utente e' registrato:
        else:
            # Se il messaggio viene inviato da un utente:
            if msg.sender.id != SUPERADMIN and users[str(msg.sender.id)]['admin'] == False:
                await msg.respond(f'Ciao {msg.sender.username} bentornato in questo bot!', buttons=[[Button.inline('AVVIA CHAT', 'start_chat')]])
            # Se il messaggio viene inviato dall'admin:
            else:
                await msg.respond(f'Ciao {msg.sender.username}, sei un\'admin, tutti i messaggi dagli utenti verranno inviati in questa chat')
    # Se il messaggio non e' uguale a start, l'utente e' registrato, non e' bannato e non e' admin:
    users = json.load(open('users.json'))
    if (
            msg.text != '/start' and msg.sender.id != SUPERADMIN and str(msg.sender.id) in users and
            users[str(msg.sender.id)]['ban'] == False and users[str(msg.sender.id)]['admin'] == False
    ):
            for user in users:
                global admin
                if users[user]['admin'] == True:
                    admin = user
                    await bot.forward_messages(int(user), msg.id, msg.sender.id)
                    await bot.send_message(int(user), 'Messaggio inviato da @' + msg.sender.username + ' (' + str(msg.sender.id) + ') \nRispondi a questo messaggio per rispondere all\'utente')
            await bot.forward_messages(SUPERADMIN, msg.id, msg.sender.id)
            await bot.send_message(SUPERADMIN, 'Messaggio inviato da @' + msg.sender.username + ' (' + str(msg.sender.id) + ') \nRispondi a questo messaggio per rispondere all\'utente', buttons=[[Button.inline('BAN', 'ban'), Button.inline('RENDI ADMIN', 'admin')], [Button.inline('UNBAN', 'unban'), Button.inline('UN ADMIN', 'unadmin')]])
    elif users[str(msg.sender.id)]['ban']:
        await msg.respond('Sei stato bannato dal bot!')

    elif users[str(msg.sender.id)]['admin'] or msg.sender.id == SUPERADMIN:
        if msg.is_reply:
            idd = (await msg.get_reply_message()).text.split(" ")[4].replace('(', '')
            idd = idd.replace(')', '')
            await bot.send_message(int(idd), 'Staff: ' + msg.text)
            for user in users:
                if users[user]['admin'] == True:
                    if user != str(msg.sender.id):
                        await bot.send_message(int(user), 'Messaggio in risposta a @' + (await msg.get_reply_message()).text.split(" ")[3] + 'da @' + msg.sender.username + ': ' + msg.text)
                    if msg.sender.id != SUPERADMIN:
                        await bot.send_message(int(user), 'Messaggio in risposta a @' +(await msg.get_reply_message()).text.split(" ")[3] + 'da @' + msg.sender.username + ': ' + msg.text)


@bot.on(events.CallbackQuery())
async def callbackQuery(cq):
    # Se viene avviata la chat:
    if cq.data == b"start_chat":
        users = json.load(open('users.json'))
        users[str(cq.sender.id)]['open'] = True
        json.dump(users, open('users.json', 'w'))
        await cq.edit('Chat con gli admin avviata correttamente, invia qui i messaggi che vuoi mandargli!', buttons=[[Button.inline('FERMA CHAT', 'stop_chat')]])
    # Se viene fermata la chat:
    elif cq.data == b"stop_chat":
        users = json.load(open('users.json'))
        users[str(cq.sender.id)]['open'] = False
        json.dump(users, open('users.json', 'w'))
        await cq.edit('Chat fermata correttamente!', buttons=[[Button.inline('AVVIA CHAT', 'start_chat')]])
    # Se viene premuto il tasto bannato
    elif cq.data == b"ban":
        users = json.load(open('users.json'))
        if cq.sender.id == SUPERADMIN or users[str(cq.sender.id)]['admin'] == True:
            idd = (await cq.get_message()).text.split(" ")[4].replace('(', '')
            idd = idd.replace(')', '')
            users[str(idd)]['ban'] = True
            json.dump(users, open('users.json', 'w'))
            await cq.answer('Hai correttamente bannato l\'utente', alert=True)
            await bot.send_message(int(idd), 'Sei stato bannato!')
        else:
            await cq.respond('NON SEI UN ADMIN', alert=True)
    # Se viene premiuto il tasto admin
    elif cq.data == b"admin":
        users = json.load(open('users.json'))
        if cq.sender.id == SUPERADMIN or users[str(cq.sender.id)]['admin'] == True:
            idd = (await cq.get_message()).text.split(" ")[4].replace('(', '')
            idd = idd.replace(')', '')
            users[str(idd)]['admin'] = True
            json.dump(users, open('users.json', 'w'))
            await cq.answer('Hai correttamente reso l\'utente admin', alert=True)
            await bot.send_message(int(idd), 'Sei stato reso admin!')
        else:
            await cq.respond('NON SEI UN ADMIN', alert=True)
    # Se viene premiuto il tasto unban
    elif cq.data == b"unban":
        users = json.load(open('users.json'))
        if cq.sender.id == SUPERADMIN or users[str(cq.sender.id)]['admin'] == True:
            idd = (await cq.get_message()).text.split(" ")[4].replace('(', '')
            idd = idd.replace(')', '')
            users[str(idd)]['ban'] = False
            json.dump(users, open('users.json', 'w'))
            await cq.answer('Hai correttamente unbannato l\'utente', alert=True)
            await bot.send_message(int(idd), 'Sei stato unbannato!')
        else:
            await cq.respond('NON SEI UN ADMIN', alert=True)

    # Se viene premiuto il tasto unadmin
    elif cq.data == b"admin":
        users = json.load(open('users.json'))
        if cq.sender.id == SUPERADMIN or users[str(cq.sender.id)]['admin'] == True:
            idd = (await cq.get_message()).text.split(" ")[4].replace('(', '')
            idd = idd.replace(')', '')
            users[str(idd)]['admin'] = False
            json.dump(users, open('users.json', 'w'))
            await cq.answer('Hai correttamente eliminato l\'utente come admin', alert=True)
            await bot.send_message(int(idd), 'Non sei piu\' un admin!')
        else:
            await cq.respond('NON SEI UN ADMIN', alert=True)

bot.start()

bot.run_until_disconnected()
