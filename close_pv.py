from pyrogram import Client, filters, enums
from pyrogram.enums import ChatType
from setting import *
from local_setting import *
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pysondb import db


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

app = Client("CLOSE_PV_SESSION", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

ConfigAcc = db.getDb('log.json')

# Get account info from config.json
check = ConfigAcc.getByQuery({'admin_id': ADMIN_ID})

# Keep default config
default_config = \
{
    'friend': [6719097274],
    'admin_id': ADMIN_ID
}

# Add account default config to config.json if it not exists
if not check:
    ConfigAcc.add(default_config)

# |========> Setup scheduler <========|
scheduler = AsyncIOScheduler()
scheduler.start()

@app.on_message(filters.command('bot'))
async def new_message_handler(client, message):
    global is_off
    
    if message.from_user is None or message.from_user.id != ADMIN_ID:
        return
    msg = message.text
    msg = msg.split()
    if len(msg) != 2:
         await message.reply("""
                            This wrong!
                            /bot on
                            OR
                            /bot off
                             """)
    msg = msg[1]
    if msg == "on":
        if is_off:
            is_off = False
            txt = "__ربات روشن شد!__"
        else:
            txt = "__ربات روشن بوده است!__"
    elif msg == "off":
        if is_off:
            txt = "__ربات خاموش بوده است!__"
        else:
            is_off = True
            txt = "__ربات خاموش شد!__"
    else:
        return
    await message.reply(txt, quote=True)
    

@app.on_message(filters.command('help'))
async def new_message_handler(client, message):
    global is_off
    
    if is_off or message.from_user is None or message.from_user.id != ADMIN_ID:
        return
    await message.reply(help_text, quote=True)
    
    
@app.on_message(filters.command('add'))
async def new_message_handler(client, message):
    global is_off
    
    if is_off or message.from_user is None or message.from_user.id != ADMIN_ID:
        return

    msg = message.text
    msg = msg.split()

    if len(msg) == 2:
        given_id = msg[1]
        try:
            given_id = int(given_id)
            txt = "__آیدی عددی داده شده با موفقیت به لیست دوستان اضافه شد!__"
        except ValueError:
            given_id = 0
            txt = "__آیدی عددی وارد شده نامعتبر است!__"

    else:
        given_id = 0
        txt = "__دستور افزودن به لیست دوستان به شکل نادرستی وارد شده است!__"

    if given_id != 0:
        # Get account info from config
        datas = ConfigAcc.getByQuery({'admin_id': ADMIN_ID})[0]
        
        if given_id not in datas['friend']:
            datas['friend'].append(given_id)
            ConfigAcc.updateByQuery({'admin_id': ADMIN_ID}, {'friend': datas['friend']})
        else:
            txt = "__کاربر موردنظر در لیست دوستان بوده است!__"

    await message.reply(txt, quote=True)
    

@app.on_message(filters.command('del'))
async def new_message_handler(client, message):
    global is_off
    
    if is_off or message.from_user is None or message.from_user.id != ADMIN_ID:
        return

    msg = message.text
    msg = msg.split()

    if len(msg) == 2:
        given_id = msg[1]
        try:
            given_id = int(given_id)
            txt = "__آیدی عددی داده شده با موفقیت از لیست دوستان حذف شد!__"
        except ValueError:
            given_id = 0
            txt = "__آیدی عددی وارد شده نامعتبر است!__"

    else:
        given_id = 0
        txt = "__دستور حذف از لیست دوستان به شکل نادرستی وارد شده است!__"

    if given_id != 0:
        # Get account info from config
        datas = ConfigAcc.getByQuery({'admin_id': ADMIN_ID})[0]

        if given_id in datas['friend']:
            datas['friend'].remove(given_id)
            # Update config
            ConfigAcc.updateByQuery({'admin_id': ADMIN_ID}, {'friend': datas['friend']})
        else:
            txt = "__کاربر موردنظر در لیست دوستان نبوده است!__"
            
            
@app.on_message(filters.command('id'))
async def new_message_handler(client, message):
    global is_off
    
    if is_off or message.from_user is None or message.from_user.id != ADMIN_ID:
        return
    if message.reply_to_message is not None:
        given_id = message.reply_to_message.from_user.id
        txt = f"__آیدی عددی کاربر ریپلای شده  :  `{given_id}`__"
    else:
        if message.chat.type is ChatType.PRIVATE:
            txt = f"__آیدی عددی این کاربر  :  `{message.chat.id}`__"
        elif message.chat.type is ChatType.SUPERGROUP:
            txt = f"__آیدی عددی این گروه  :  `{message.chat.id}`__"
        else:
            txt = "__لطفا در گروه یا پیوی کاربر ارسال کنید!__"
    await message.reply(txt, quote=True)            
            

@app.on_message()
async def new_message_handler(client, message):
    datas = ConfigAcc.getByQuery({'admin_id': ADMIN_ID})[0]
    global is_off

    if is_off or message.from_user is None:
        return
    
    if message.from_user.id not in datas['friend']:
        try:
            await message.delete()
        except:
            pass

if __name__ == "__main__":
    app.run()