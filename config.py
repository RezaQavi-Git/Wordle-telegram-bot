
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TOKEN')
WORLDS_LIST = [os.environ.get('WORDS_LIST').split()]