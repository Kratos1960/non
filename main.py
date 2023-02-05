import telebot
from telebot import async_telebot
from redis import Redis
db = Redis(host="localhost",port=6379)
bot = async_telebot.AsyncTeleBot(input("Enter token of bot : "))
@bot.message_handler(func=lambda m : True)
def GetBlackList(message):
    if "منع" in message.text and bot.get_chat_member(message.from_user.id).status == "creator":
        message_id = message.text.replace("منع ","")
        db.set(f"{message_id}","BlackList")
        bot.reply_to(message,f"• تم وضع {message_id} في القائمة السوداء ..")
@bot.chat_join_request_handler()
def ApprovRequest(message: telebot.types.ChatJoinRequest):
    status = db.get(f"{message.from_user.id}")
    if status != "BlackList":
        bot.approve_chat_join_request(message.chat.id, message.from_user.id)
        bot.send_message(message.chat.id,f"• لقد قبلت انضمام هذا الشخص {message.from_user.id} .")
    else:
        bot.send_message(message.chat.id,f"• هذا الشخص {message.from_user.id} ضمن القائمة السوداء ، لقد ارسل طلب انضمام لكن لم اوافق .")
bot.infinity_polling()