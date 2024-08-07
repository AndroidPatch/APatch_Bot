#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Don't forget to enable inline mode with @BotFather

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import os
from html import escape
from uuid import uuid4
import hashlib

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler
from telegram.ext import ChatJoinRequestHandler
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
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


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query

    if not query:  # empty query should not be handled
        return

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Bold",
            input_message_content=InputTextMessageContent(
                f"<b>{escape(query)}</b>", parse_mode=ParseMode.HTML
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Italic",
            input_message_content=InputTextMessageContent(
                f"<i>{escape(query)}</i>", parse_mode=ParseMode.HTML
            ),
        ),
    ]

    await update.inline_query.answer(results)
async def join_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    #chat_id=update.chat_join_request.chat.id
    chat_id = update.effective_chat.id
    chat_id = update.chat_join_request.from_user.id
    username=update.chat_join_request.from_user.full_name
    #chat_id = -1007069301752
    
    bot=context.bot
    await bot.send_message(chat_id=chat_id, text="题目：手机已解锁，已进入bootloader状态,请用kptools刷入手机\n https://exame.apatch.dev/?id="+str(chat_id) +"  完成后，你将得到一个密码，可以查阅文档寻求帮助 https://apatch.dev ,对机器人发送 /join [你得到的密码] (例如 /join 123456)"
                            
    )

    
    #await update.message.reply_text("Help!")
    #print(context)
    
    #return

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    token=os.getenv('TOKEN','None')
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("join", help_command))

    # on inline queries - show corresponding inline results
    application.add_handler(InlineQueryHandler(inline_query))
    
    application.add_handler(ChatJoinRequestHandler(join_group))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
