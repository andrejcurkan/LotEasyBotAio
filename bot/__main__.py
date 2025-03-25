import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from configs import conf
from configs.logs_config import logs
from handlers import bot_blocked_handlers, admin_handlers, start_rules_handlers, user_handlers
from middlewares.ban_rules_check import BanRulesCallbackMiddleware
from middlewares.bot_blocked_check import BotBlockedCallMiddleware
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage
from checkers import Checkers as ch
from configs.env_reader import env_config
from db_conn_create import db
import logging

logging.basicConfig(
    level=logging.DEBUG,  # INFO или DEBUG для максимальной детализации
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат логов
)
logger = logging.getLogger(__name__)


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    global bot
    try:
        logger.info("Starting bot initialization...")

        # Инициализация подключения к базе данных
        logger.info("Initializing database connection...")
        if db is not None:
            await db.connect()
        logger.info("Database connected successfully.")

        # Инициализация бота
        logger.info("Initializing bot with token...")
        bot = Bot(
            token=env_config.BOT_TOKEN.get_secret_value(),
            default=DefaultBotProperties(parse_mode="HTML")
        )
        logger.info("Bot initialized successfully.")

        # Инициализация диспетчера
        logger.info("Initializing dispatcher with MemoryStorage and FSMStrategy...")
        dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT)
        logger.info("Dispatcher initialized successfully.")

        # Регистрация роутеров
        logger.info("Registering routers...")
        dp.include_routers(
            bot_blocked_handlers.router,
            start_rules_handlers.router,
            user_handlers.router,
            admin_handlers.router
        )
        logger.info("Routers registered successfully.")

        # Регистрация middleware
        logger.info("Registering middleware...")
        dp.callback_query.outer_middleware(BanRulesCallbackMiddleware())
        dp.callback_query.outer_middleware(BotBlockedCallMiddleware())
        logger.info("Middleware registered successfully.")

        # Настройка фильтров
        logger.info("Setting up filters...")
        dp.my_chat_member.filter(F.chat.type == "private")
        dp.message.filter(F.chat.type == "private")
        logger.info("Filters set up successfully.")

        # Запуск дополнительных задач, если они включены в конфигурациях
        if conf.ch_start:
            logger.info("Starting additional tasks...")
            asyncio.create_task(ch().topup_cheker_all(bot))
            asyncio.create_task(ch().winner_warned_checker(bot))
            logger.info("Additional tasks started successfully.")

        # Запуск бота
        logger.info("Starting polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        logger.info("Polling started successfully.")

    except (KeyboardInterrupt, asyncio.CancelledError):
        # Обработка прерывания (например, Ctrl+C)
        logger.warning("Bot stopped by user!")
    except Exception as e:
        # Логирование любых других ошибок
        logger.error(f"An error occurred: {e}", exc_info=True)
    finally:
        # Корректное завершение работы бота
        if 'bot' in globals():
            logger.info("Closing bot session...")
            await bot.session.close()
            logger.info("Bot session closed successfully.")

        # Закрытие соединения с базой данных, если соединение было установлено
        if db is not None:
            logger.info("Closing database connection...")
            await db.close()
            logger.info("Database connection closed successfully.")


if __name__ == "__main__":
    # Логируем запуск программы
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Starting the bot application...")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

    logger.info("StreamHandler добавлен вручную")

    asyncio.run(main())
