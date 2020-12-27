from pyosu import Osu
from telebot import TeleBot, types

import requests
import io
import random

bot = TeleBot("1454185227:AAFCfSgdY4ZWLIiVHIpp117ZFwxkkkSsoYU")
osu = Osu("29bb2198e1a05fe147ad2a81a60bd97e05a32b61")


bot_commands = [
    '/start:Re/Starting bot',
    '/help:All commands',
    '/support:Message to admin',
    '/info <username>:Profile info',
    '/img <username>:Profile image'
]

admin = 842794623

def help_msg(message):
    msg = "😜 My commands:"
    for i in range(len(bot_commands)):
        c = bot_commands[i].split(":")
        msg = msg+f"\n{i+1}. {c[0]} - {c[1]}"

    bot.send_message(message.chat.id, msg)

def error_msg(message, e):
    bot.send_message(message.chat.id, "😕 Hmm.. error\n"+e, parse_mode="HTML")

support_poll = []

@bot.message_handler(commands=['start', 'help', 'info', 'img', 'support', 'exit', 'send'])
def poll_cmd(message):
    if message.text == "/start":
        bot.send_message(message.chat.id, f"😎 Hi, {message.chat.first_name}!")
        bot.send_message(message.chat.id, "Bot created on Python3.9\nAdmin: @rzet8")
        help_msg(message)

    elif message.text == "/help":
        help_msg(message)

    elif "/info" in message.text:
        try:
            username = message.text.split(" ")[1]

            info = osu.player(username)

            if info != None:
                world = '{0:,}'.format(int(info['profile']['top']['world'])).replace(",", " ")
                local = '{0:,}'.format(int(info['profile']['top']['local'])).replace(",", " ")
                msg = f"🤩 Profile {info['profile']['name']}\n - Id: {info['profile']['user_id']}\n - Level: {info['profile']['level']}\n - Join date: {info['misc']['join_date']}\n - Game time: {info['game']['gametime']}hours\n\n🎮 Game\n - PP: {info['game']['pp']}\n - Accuracy: {info['game']['accuracy']}\n - Playcount: {info['game']['playcount']}games\n\nSS: {info['game']['total']['ss']} | S: {info['game']['total']['s']} | A: {info['game']['total']['a']}\n\n🥇 Top\n - Local: {local} ({info['profile']['country']})\n - World: {world}"
                bot.send_message(message.chat.id, msg)
            else:
                error_msg(message, username+" not found!\n\nCheck username and try again")
        except:
            error_msg(message, "Where your username?\n\n<b>Use:</b> /info <username>")
    
    elif "/img" in message.text:
        try:
            username = message.text.split(" ")[1]

            img = osu.player(username)

            if img != None:
                response = requests.get(img['misc']['image_url'])
                image = io.BytesIO(response.content)
                
                bot.send_photo(message.chat.id, photo=image, caption="🥰 "+username)
            else:
                error_msg(message, username+" not found!\n\nCheck username and try again")
        except Exception as e:
            print(e)
            error_msg(message, "Where your username?\n\n<b>Use:</b> /info <username>")
        
    elif message.text == '/support' and message.chat.id not in support_poll:
        bot.send_message(message.chat.id, "😭 Write your problem: @rzet8")
        #support_poll.append(message.chat.id)
        #print(message.chat.id)
    

@bot.message_handler(content_types=['text'])
def poll_msg(message):
    if message.text == "":
        pass
    else:
        bot.reply_to(message, "🤨 Undefined command\nCheck /help")

if __name__ == "__main__":
    bot.polling(True)