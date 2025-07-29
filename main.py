#!/usr/bin/env python3

import logging
import os
from html import escape
from uuid import uuid4
import hashlib

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler, ChatJoinRequestHandler
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user_id=update.effective_chat.id
    text=update.effective_message.text
    print(text)
    pwd=text[6:]
    print(pwd)
    m = hashlib.md5()
    m.update(("{}".format(user_id)+'apatch').encode('utf-8'))
    sign=m.hexdigest()
    print(sign)
    if pwd==sign:
        await context.bot.approveChatJoinRequest(user_id=user_id,chat_id=-1002058433411)
        await update.message.reply_text("密码正确")
    else:
        await update.message.reply_text("密码错误")

    
    
    #await update.message.reply_text("Help!")


async def join_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    #chat_id=update.chat_join_request.chat.id
    chat_id = update.effective_chat.id
    chat_id = update.chat_join_request.from_user.id
    username=update.chat_join_request.from_user.full_name
    #chat_id = -1007069301752
    
    bot=context.bot
    await bot.send_message(chat_id=chat_id, text="题目：手机已解锁，已进入bootloader状态,请用kptools刷入手机\n https://exame.apatch.dev/?id="+str(chat_id) +"  完成后，你将得到一个密码，可以查阅文档寻求帮助 https://apatch.dev ,对机器人发送 /join [你得到的密码] (例如 /join 123456)"
                            
    )

def main() -> None:
    token=os.getenv('TOKEN','None')
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("join", help_command))
    application.add_handler(ChatJoinRequestHandler(join_group))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
