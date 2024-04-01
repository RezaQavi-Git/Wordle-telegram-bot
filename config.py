import os
from dotenv import load_dotenv

load_dotenv()

defaultWordsList = open("resources/words_list.txt", "r").read()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WORDS_LIST = os.environ.get("WORDS_LIST", default=defaultWordsList).split()

startMessage = """Hi {user}
I'm a Wordle game
I choose a random word and say number of letters of this word, you should guess it.
I hope you enjoy :)
To start paly: /wordle
For help: /help"""

helpMessage = """"I'm a Wordle game
I choose a random word and say number of letters of this word, you should guess it.
I hope you enjoy :)
Game color meaning:
🟢(Right place)
🟡(Exists, but in the wrong place)
🔴(Not exist) 
To start paly: /wordle"""

wordleMessage = """Game color meaning:
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

winMessage = """You Win 🚀
I\'ll do nothing for you, go and be happy :)
Come back soon Dude
Play again /wordle"""

guessResultMessage = """Guess result : {hints}
Letters matched : {matchPattern}
To continue reply [word] otherwise /cancel"""


cancelMessage = """Hehe, you lose
Random word was : {randomWord}"""
