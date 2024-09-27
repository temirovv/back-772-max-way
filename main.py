import asyncio
import logging
import sys

from loader import dp, bot, db
import handlers.admin.admin_handler 
from handlers.users import start_handler
from handlers.users import menu_handler
from handlers.users import filial_handlers

from handlers.users import back_button_handler


async def main() -> None:  
    db.create_category_table()
    db.create_products_table()
    db.create_users_table()
    db.create_vacancy_table()
    db.create_cart_table()
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
