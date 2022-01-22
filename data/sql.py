from environs import Env
import asyncpg
import logging


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
admins = env.list("ADMINS")


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


async def create_pool():
    return await asyncpg.create_pool(user=env.str("PG_USER"),
                                     password=env.str("PG_PASS"),
                                     host=env.str("PG_HOST"),
                                     database=env.str("DB"))
