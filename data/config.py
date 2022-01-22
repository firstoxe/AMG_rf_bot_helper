from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
admins = env.list("ADMINS")


ip = '127.0.0.1'
aiogram_redis = {
    'host': ip,
}

redis = {
    'address': ('127.0.0.1', 6379),
    'encoding': 'utf8'
}
