import requests
import sqlite3
import schedule
import time
import datetime
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path = env_path)
token = os.getenv("TOKEN")
api = 'https://api.telegram.org/bot' + token + '/'

delt = 3 # hwclock in UTC, chat in MSK timezone

con = sqlite3.connect('peezdos.db')
c = con.cursor()
c.execute('select * from STICKERS')
res = c.fetchall()
stickers_id = {r[0] : r[1] for r in res}

def peezdos():
  now = datetime.datetime.now()
  chat_id = -1001399625236
  url = api + 'sendSticker?chat_id=' + str(chat_id) + '&sticker=' + stickers_id[(now.hour+delt)%24]
  r = requests.get(url)

schedule.every().hour.at(":00").do(peezdos)

while True:
    schedule.run_pending()
    time.sleep(1)
