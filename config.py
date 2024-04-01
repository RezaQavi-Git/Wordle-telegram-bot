import os
from dotenv import load_dotenv

load_dotenv()

defaultWordsList = open("resources/words_list.txt", "r").read()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WORDS_LIST = os.environ.get("WORDS_LIST", default=defaultWordsList).split()
LOG_CHANNEL_ID = os.environ.get("LOG_CHANNEL_ID", default='')

startMessage = """Hi {user} 😏
I'm a Wordle game
I'll select a word at random and tell you how many letters it has. Your task is to guess the word.
I hope you enjoy :)
To start paly: /wordle
For help: /help"""

helpMessage = """I'm a Wordle game
I'll select a word at random and tell you how many letters it has. Your task is to guess the word.
I hope you enjoy :)
Game Color Meaning:
🟢(Right place)
🟡(Exists, but in the wrong place)
🔴(Not exist) 
To start paly: /wordle"""

wordleMessage = """Game Color Meaning:
🟢(Right place)
🟡(Exists, but in the wrong place)
🔴(Not exist) 
A random word selected, {numberOfLetters} Letters
Start guessing with [word]"""

guessMessage = """Dude, guess a world :(
or /cancel"""

guessLengthMessage = """Dude, at least guess a world with same length :(
or /cancel"""

guessValidationMessage = """Dude, just use letters in your guess [A-Z, a-z] :(
or /cancel"""

winMessage = """You Win 🔥
Go and be happy :)
Come back soon
Play again /wordle"""

guessResultMessage = """Guess Result: {hints}
Letters Matched: {matchPattern}
To continue, reply with [word]. To cancel, use /cancel."""

cancelMessage = """HeHe, you lose
Random word was : {randomWord}"""
