import asyncio
import logging
import sys
from os import getenv
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode , ContentType
from aiogram.filters import CommandStart , Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import confog
import time
import functions
import db
import butons

TOKEN = confog.TOCEN
bot = Bot(TOKEN)
dp = Dispatcher()

async def send_new_user_to_admin(user):
    info = f"Yangi foydalanuvchi\nid : {user.from_user.id}\nIsmi : {user.from_user.first_name}\nFamilasi : {user.from_user.last_name}\nUsername : {user.from_user.username}"
    await bot.send_message(chat_id=confog.ADMIN_ID , text=info)
    
async def get_not_sub_chanals(user_id):
    not_sub_ch = []
    chanals = db.Chanals()
    for chanal in chanals.get_all_chanals():
        status = await bot.get_chat_member(f'@{chanal[1]}' , user_id)
        if status.status == 'left' : not_sub_ch.append(chanal[1])
    return not_sub_ch

async def subscribe_button(user_id):
    builder = InlineKeyboardBuilder()
    chalals = db.Chanals()
    not_sub = await get_not_sub_chanals(user_id=user_id)
    i = 1
    for ch in not_sub:
        builder.add(types.InlineKeyboardButton(
        text=f"Kanal {i}",
        url=f'https://t.me/{ch}'))
        i += 1
    builder.add(types.InlineKeyboardButton(
        text=" ✅ Tastoqlash ✅ ",
        callback_data="check_subscribe_to_chanals")
    )
    builder.adjust(1)
    return builder.as_markup()

async def check_subckribe(user_id):
    chanals = db.Chanals()
    not_sub_chan = []
    for chanal in chanals.get_all_chanals():
        status = await bot.get_chat_member(f'@{chanal[1]}' , user_id)
        if status.status == 'left' : not_sub_chan.append(chanal[1])
    if len(not_sub_chan) == 0 : return True
    return False

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = db.User()
    if user.check_user_into_database(chat_id=message.chat.id):
        user.adding_user(
            chat_id=message.chat.id,
            is_admin="False",
            user_name=message.from_user.username,
            first_name=message.from_user.first_name,
        )
        await send_new_user_to_admin(message)
    await bot.send_sticker(
        message.chat.id,
        sticker="CAACAgIAAxkBAAEKPlZk-eLKS3tUCG_aRGY1wZjJY8tnxAACxgEAAhZCawpKI9T0ydt5RzAE",
    )
    info = await bot.get_me()
    name = info.first_name
    await message.answer(
        f"Salom, {hbold(message.from_user.full_name)}! \n{name} botga hush kelibsiz😎\nMen sizga instagramdan video yuklab beraman🤩\nShunchaki video havolasini yuboring💈"
    )

# -----------------    Chanals Manager    --------------#

@dp.message(F.text, Command("chanal_add"))
async def chanal_add(message: Message):
    if message.from_user.id == confog.ADMIN_ID : 
        new_chanal = message.text
        new_chanal.replace('/chanal_add ' , '')
        if len(new_chanal) > 0 :
            chanal = db.Chanals()
            chanal.create_chanal(chanal_name=new_chanal.replace('/chanal_add ' , ''))
            text = f'<b> ✅ SUCCESS ✅ </b>\nKannal {new_chanal} muvofoqiyatli qoshildi 🤩 🤪 😎'
            await bot.send_message(message.chat.id , text=text , parse_mode=ParseMode.HTML )
        else : await bot.send_message(message.chat.id , text=' 😔 Kanal qoshilmadi 😔 ') 

@dp.message(F.text, Command("chanal_delete"))
async def chanal_add(message: Message):
    if message.from_user.id == confog.ADMIN_ID : 
        cahnal_id = message.text[15:]
        status = True
        try :
            chanal = db.Chanals()
            chanal.delete_chanal(int(cahnal_id))
        except :
            status = False
        if status : await bot.send_message(message.chat.id , text=f'Knal id : {cahnal_id} , movofoqiyatli udalit boldi ✅ ' )
        else : await bot.send_message(message.chat.id , text=f' ⛔️ Knal id : {cahnal_id} , udalit bolmadi, kanal idsini qayta tekshiring ⛔️ ' )

@dp.message(F.text , Command('all_chanals'))
async def all_chanals_list(message : Message):
    if message.from_user.id == confog.ADMIN_ID : 
        messag_s = await bot.send_message(chat_id=message.chat.id , text=' ♻️ Yuklanmoqta ♻️ ')
        chan = db.Chanals()
        chanals = chan.get_all_chanals()
        list_chan = 'Hamma Aktiv Kanallar\n'
        for chanal in chanals:
            temp = f"id : {chanal[0]}\n"
            temp += f"Chanal name : {chanal[1]} \n\n"
            list_chan += temp
        await messag_s.edit_text(text=list_chan)

@dp.message(F.text , Command('send'))
async def send_all(message : Message):
    if confog.ADMIN_ID == message.from_user.id :
        text = message.text[6:]
        d = db.User()
        bloked_users = 0
        un_bloked_users = 0
        for users in d.get_all_users():
            try : 
                await bot.send_message(chat_id=users[1] , text=text , parse_mode=ParseMode.HTML)
                un_bloked_users += 1
            except :
                bloked_users += 1
        staistik = f'<b> ✅ Habar Muvofoqiyatli Yuborildi ✅ </b>\nJami foydalanuvchilar 👥 : {bloked_users + un_bloked_users} \nAktivlari 😎 : {un_bloked_users} \nBlokdaygilar 😔 : {bloked_users}'
        await bot.send_message(message.chat.id , text=staistik , parse_mode=ParseMode.HTML)

# -----------------    Chanals Manager End   --------------#

@dp.message(F.text, Command("help"))
async def help_command(message: Message):
    info = await bot.get_me()
    name = info.first_name
    text = f'<b>Men {name} bot man 🤖</b>\nMen sizga Instagramda rivojlanishga yordam beraman ✅ \n\n<b>Video Yuklash🎥\nProfil Haqida Malumotℹ️\nPostlar Usishi📈\nTopdaygi Hashtaglar#️⃣\nVideodaygi Hashtaglar🧾\nPost qo\'oyish uchun obunachilar faol vaqtlari🕰️</b>\nKerakli bolimni tanlang'
    await bot.send_message( message.chat.id , text , parse_mode=ParseMode.HTML , reply_markup=butons.menu_button())
    
@dp.message(F.photo)
async def input_photo(message: types.Message):
    if message.from_user.id == confog.ADMIN_ID :
        photo = message.photo[-1]
        file_id = photo.file_id

        opisaniya = message.caption
        users = db.User()

        bloked_users = 0
        un_bloked_users = 0

        sms = await bot.send_message(confog.ADMIN_ID , text='Junatish boshlandi')

        for user in users.get_all_users():
            try : 
                await bot.send_photo(chat_id=user[1] , photo=file_id , caption=opisaniya , parse_mode=ParseMode.HTML)
                un_bloked_users += 1
            except :
                bloked_users += 1
        staistik = f'<b> ✅ Habar Muvofoqiyatli Yuborildi ✅ </b>\nJami foydalanuvchilar 👥 : {bloked_users + un_bloked_users} \nAktivlari 😎 : {un_bloked_users} \nBlokdaygilar 😔 : {bloked_users}'
        await sms.edit_text(text=staistik , parse_mode=ParseMode.HTML)

@dp.message()
async def echo_handler(message: types.Message) -> None:
    if await check_subckribe(message.from_user.id) :
        if "@" in message.text:
            username = message.text.replace("@", "")
            upload_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Qabul qilindi !",
            )
            animat = [
                '⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️',
                '🟩⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️',
                '🟩🟩⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️',
                '🟩🟩🟩⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️',
                '🟩🟩🟩🟩⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️',
                '🟩🟩🟩🟩🟩⬜️⬜️⬜️⬜️⬜️⬜️⬜️',
                '🟩🟩🟩🟩🟩🟩⬜️⬜️⬜️⬜️⬜️⬜️',
                '🟩🟩🟩🟩🟩🟩🟩⬜️⬜️⬜️⬜️⬜️',
                '🟩🟩🟩🟩🟩🟩🟩🟩⬜️⬜️⬜️⬜️',
                '🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜️⬜️⬜️',
                '🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜️⬜️',
                '🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜️',
                '🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩'
                ]
            n = 0
            is_error = False
            for i in animat:
                if n == 6:
                    try :
                        res = functions.Get_Profile_Info(sesion="behruz.beg", username=username)
                        res.get_posts()
                        response = res.posts_filter()
                    except :
                        is_error = True
                await upload_message.edit_text(text=f"Yuklanmoqta : \n{i}")
                n+=1

            time.sleep(0.2)
            if is_error : await upload_message.edit_text(text=f'<b>❗️ Hatolik {message.text} nomlig profil topilmadi ❗️ </b>\nQayta urunib kuring !' , parse_mode=ParseMode.HTML)
            else :
                text = (
                    "<b>"
                    + username
                    + ", Boyicha malimotlar ✅ </b>\n\nBiografiya 📖 : "
                    + response["profile"]["biografiya"]
                    + "\n\n<b>Obunachilar 👥 : "
                    + str(response["profile"]["followers"])
                    + "</b>"
                    + "\n<b>Obunasi 👤 : "
                    + str(response["profile"]["following"])
                    + "</b>\n\n📈Eng zo'r <a href=\""
                    + str(response["posts"]["max_post"]["link"])
                    + '">post</a> , like ❤️ : '
                    + str(response["posts"]["max_post"]["likes"])
                    + '\n📉Eng yomon <a href="'
                    + response["posts"]["min_post"]["link"]
                    + '">post</a>, like 💔 : '
                    + str(response["posts"]["min_post"]["likes"])
                    + "\n<b>O'rtacha like lar 💟 "
                    + str(response["info"]["midle_likes"])
                    + "</b>\n<b>O'rtacha comentlar lar 💌 "
                    + str(response["info"]["midle_coments"])
                    + "</b>\nPost qoyish uchun optimal vaqtlar 🕰️ : "
                    + str(response["info"]["post_time_day1"])
                    + ":00 , "
                    + str(response["info"]["post_time_day2"])
                    + ":00"
                )
                await upload_message.delete()
                await bot.send_message(
                    chat_id=message.chat.id, text=text, parse_mode=ParseMode.HTML
                )
        elif "https://www.instagram.com" in message.text:
            upload_message = await bot.send_message(
                chat_id=message.chat.id, text="Yuklashni boshladim..."
            )
            fun = functions.Save_and_get_Details(message.text)
            link = ""
            await asyncio.sleep(1)
            for i in range(11):
                await upload_message.edit_text(text=f"{i*10}%")
                if i == 8:
                    link = fun.save_post()
            await upload_message.delete()

            dtals = fun.get_post_detaile()
            hashtags = dtals[3]
            h = hashtags
            text = f'<b>Video Haqida malumot ✅ </b>\nLike lar soni ♥️ : {dtals[1]}\nComentlar soni 💌 : {dtals[2]}\nOpisaniya va Heshteglar #️⃣: {h}\nVideo joylangan sana 🕰️: {dtals[4]}\n<a href="{link}" > Video </a>'
            await bot.send_message(message.chat.id, text=text, parse_mode=ParseMode.HTML)
        elif message.text == 'Video Yuklash':
            # text = "<b>Profil Haqida Malumot</b>\n\nMenga profilingizni otimi yuboring\nMasalan : \n@gtarshy.gp , @uzcodern1\n<b>Eslatma : @ < belgisi bilan yozing !</b>"

            text = '<b>Video Yuklash</b>\n\nMenga video ssilkasini yuboring\nMasalan : \nhttps://www.instagram.com/reel/CzBIWTErGLA/'
            await bot.send_message(message.chat.id , text=text , parse_mode=ParseMode.HTML )
        elif message.text == 'Profil Haqida Malumot':
            text = "<b>Profil Haqida Malumot ✅ </b>\n\n<b>Menga profilingizni otini yuboring 😎 </b>\nMasalan @starshy.gp , @uzcodern1\n\n ❗️ Albatta @ belgisini quying ❗️ "
            await bot.send_message(message.chat.id , text=text, parse_mode=ParseMode.HTML )
        else:
            await message.reply("Notug'ri bolim !")

    else : await bot.send_message(chat_id=message.chat.id , text='Botdan foydalanish uchun hamma kanallarga obuna buling !' , reply_markup=await subscribe_button(user_id=message.from_user.id))

@dp.callback_query(F.data == "check_subscribe_to_chanals")
async def send_random_value(callback: types.CallbackQuery):

    await bot.delete_message(chat_id=callback.message.chat.id , message_id=callback.message.message_id)
    if await check_subckribe(callback.from_user.id) : await bot.send_message(chat_id=callback.from_user.id , text=' ✅ Botdan Foydalanishingiz mumkun ✅ ')
    else : await bot.send_message(chat_id=callback.from_user.id , text=' 🆘 HAMMA KANALLARGA OBUNA BULING 🆘 ' , reply_markup=await subscribe_button(user_id=callback.from_user.id))

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
