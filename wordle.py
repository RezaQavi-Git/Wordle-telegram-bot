# IMPORTS
import logging
import random
import re
from config import TELEGRAM_BOT_TOKEN, WORDS_LIST
from config import (
    startMessage,
    helpMessage,
    wordleMessage,
    guessMessage,
    guessLengthMessage,
    guessValidationMessage,
    winMessage,
    guessResultMessage,
    cancelMessage,
)
from telegram import ForceReply, Update, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("WORDLE")
GUESS, WIN = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(startMessage.format(user=user.mention_html()))


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(helpMessage)


async def wordle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    randomWord = WORDS_LIST[random.randint(0, len(WORDS_LIST) - 1)]
    context.user_data["randomWord"] = randomWord
    logger.info(
        "User: {user} and RandomWord: {rm}".format(
            user=update.effective_user.username, rm=randomWord
        )
    )
    await update.message.reply_html(
        wordleMessage.format(numberOfLetters=len(randomWord)),
        reply_markup=ForceReply(input_field_placeholder="[word]"),
    )
    context.user_data["matched"] = "❔" * len(randomWord)
    return GUESS


def matching(word, guess, context):
    matchPattern = list(context.user_data["matched"])
    hints = list()
    for i in range(len(guess)):
        if guess[i] == word[i]:
            matchPattern[i] = guess[i].upper()
            hints.append("🟢")
        elif guess[i] in word:
            hints.append("🟡")
        else:
            hints.append("🔴")

    context.user_data["matched"] = "".join(matchPattern)
    return "".join(matchPattern), "".join(hints)


async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    randomWord = context.user_data["randomWord"]
    guessWord = update.message.text
    if guessWord == None:
        await update.message.reply_photo(
            photo="images/joke.png",
            caption=guessMessage,
            reply_markup=ForceReply(selective=True, input_field_placeholder="[word]"),
        )

        return GUESS
    if len(guessWord) != len(randomWord):
        await update.message.reply_photo(
            photo="images/joke.png",
            caption=guessLengthMessage,
            reply_markup=ForceReply(input_field_placeholder="[word]"),
        )
        return GUESS

    if (guessWord) != (re.sub(r"[^a-zA-Z]", "", guessWord)):
        await update.message.reply_photo(
            photo="images/joke.png",
            caption=guessValidationMessage,
            reply_markup=ForceReply(input_field_placeholder="[word]"),
        )
        return GUESS

    matchedWord, hints = matching(randomWord.lower(), guessWord.lower(), context)
    if matchedWord.lower() == guessWord.lower():
        await update.message.reply_photo(
            photo="images/win.png",
            caption=winMessage,
            reply_markup=ReplyKeyboardRemove(),
        )
        logger.info("User {user} wins.".format(user=update.effective_user.username))
        return ConversationHandler.END
    else:
        await update.message.reply_html(
            guessResultMessage.format(hints=hints, matchPattern=matchedWord),
            reply_markup=ForceReply(input_field_placeholder="[word]"),
        )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Game Canceled")
    await update.message.reply_photo(
        photo="images/loser.png",
        caption=cancelMessage.format(randomWord=context.user_data["randomWord"].upper()),
        reply_markup=ReplyKeyboardRemove(),
    )
    context.user_data["matched"] = None

    return ConversationHandler.END


def main():
    """Start Wordle Bot"""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("wordle", wordle)],
        states={
            GUESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, guess),
                CommandHandler("cancel", cancel),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == "__main__":
    main()
