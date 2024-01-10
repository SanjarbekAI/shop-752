from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

channels = [
    # (-1001961644956, 'Test kanal', 'https://t.me/MyBotTestChannelLink'),
    (-1002035223730, 'Kanallarni dodasi', 'https://t.me/MarsTestCanal'),
    (-1002073427408, 'Begzod silla', 'https://t.me/+TYJp20ZuSwQ1ZGYy'),
]
