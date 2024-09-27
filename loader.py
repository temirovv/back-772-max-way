from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database.db_sqlite import Database


TOKEN = '6696952903:AAG0cKfbu_U9QfWMVCJobd09MPhnQHqHQp8'
ADMIN = 1058730773

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
db = Database(path_to_db='database/main.db')
