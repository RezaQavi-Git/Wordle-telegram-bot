
import os
from dotenv import load_dotenv

load_dotenv()

defaultWordList = open('resources/wordlist.txt', 'r').read()

TOKEN = os.environ.get('TOKEN')
WORDS_LIST = os.environ.get('WORDS_LIST', default=defaultWordList).split()
