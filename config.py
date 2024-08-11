with open('.token', 'r') as file:
    env_token = file.readline()

with open('.chat', 'r') as file:
    chat = file.readline()

    
class Settings():
    BOT_TOKEN: str = env_token
    CHAT: str = chat
    # 24 hours in seconds
    INTERVAL_24 = 24*60*60


SETTINGS = Settings()