# IMPORTS
import logging
import random

from config import TOKEN, WORDS_LIST
from telegram import ForceReply, Update, ReplyKeyboardRemove
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          ConversationHandler, MessageHandler, filters)

# LOGGING
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger('WORDLE')

# STAGES
GUESS, WIN = range(2)

# HANDLERS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!" +
        "\nI'm a Wordle game" +
        "\nI choose a random word and say number of letters of this word, you should guess it." + 
        "\nI hope you enjoy :)" +
        "\nTo start paly: /wordle" +
        "\nFor help: /help"

    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        "\nI'm a Wordle game" +
        "\nI choose a random word and say number of letters of this word, you should guess it." + 
        "\nI hope you enjoy :)" +
        "\nGame color meaning:\n🟢(right place)\n🟡(exist but in wrong place)\n🔴(not exist)\n" + 
        "\nTo start paly: /wordle"

    )

async def wordle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    randomWord = WORDS_LIST[random.randint(0, len(WORDS_LIST)-1)]
    context.user_data['randomWord'] = randomWord
    logger.info('User: {user} and RandomWord: {rm}'.format(
        user=update.effective_user.username, rm=randomWord))
    await update.message.reply_html(
        'Game color meaning:\n🟢(right place)\n🟡(exist but in wrong place)\n🔴(not exist)\n' + 
        'A random word selected, {numberOfLetters} Letters \n'.format(numberOfLetters=len(randomWord)) +
        'Start guessing with [word]',
        reply_markup=ForceReply(input_field_placeholder='[word]')
    )
    context.user_data['matched'] = '-'*len(randomWord)
    return GUESS


def matching(word, guess, context):
    matchPattern = list(context.user_data['matched'])
    hints = list()
    for i in range(len(guess)-1):
        if guess[i] == word[i]:
            matchPattern[i] = guess[i]
            hints.append('🟢')
        elif guess[i] in word:
            hints.append('🟡')
        else:
            hints.append('🔴')
    
    logger.info('Matching : {word}'.format(word=''.join(matchPattern)))
    context.user_data['matched'] = ''.join(matchPattern)
    return ''.join(matchPattern), ''.join(hints)


async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    randomWord = context.user_data['randomWord']
    guessWord = update.message.text
    if guessWord == None:
        await update.message.reply_photo(
            'images/joke.png'
            'Dude, guess a world :(\nor /cancel',
            reply_markup=ForceReply(
                selective=True, input_field_placeholder='[word]')
        )

        return GUESS
    if len(guessWord) != len(randomWord):
        await update.message.reply_photo(
            'images/joke.png',
            'Dude, at least guess a world with same length :(\nor /cancel ',
            reply_markup=ForceReply(input_field_placeholder='[word]')
        )
        return GUESS
    
    matchedWord, hints = matching(randomWord.lower(), guessWord.lower(), context)
    if  matchedWord.lower() == guessWord.lower():
        await update.message.reply_photo(
            'images/win.png',
            'You win, I do nothing for you, go and be happy\n' +
            'Come back soon Dude'
        )
        logger.info('User {user} wins.'.format(user=update.effective_user.username))
        return ConversationHandler.END
    else:
        await update.message.reply_html(
            'Guess result : {hints}\n'.format(hints=hints) +
            'letters matched : {matchPattern}\n'.format(matchPattern=matchedWord) +
            'To continue reply [word] otherwise /cancel',
            reply_markup=ForceReply(input_field_placeholder='[word]')
        )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info('Game Canceled')
    await update.message.reply_photo(
        'images/loser.png',
        '\n\nHehe, you lose.\n' +
        'Random word was : {randomWord}'.format(
            randomWord=context.user_data['randomWord']),
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data['matched'] = None

    return ConversationHandler.END


def main():
    """Start Wordle Bot"""
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("wordle", wordle)],
        states={
            GUESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, guess), CommandHandler("cancel", cancel)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == '__main__':
    main()
