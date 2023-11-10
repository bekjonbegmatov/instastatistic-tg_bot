from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram import types

import db


def chanal_kb():
    chanal_kbl = InlineKeyboardMarkup(row_width=1)
    num = 1
    chan = db.Chanals()
    for i in chan.get_all_chanals():
        chanal_kbl.insert(
            InlineKeyboardButton(text=f"Kanal {num}", url=f"https://t.me/{i[1]}")
        )
        num += 1
    chanal_kbl.insert(
        InlineKeyboardButton(text="Tasdiqlash ✅", callback_data="sub_done")
    )

    return chanal_kbl


def menu_button():
    kb = [
        [types.KeyboardButton(text="Video Yuklash")],
        [types.KeyboardButton(text="Profil Haqida Malumot")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    return keyboard

