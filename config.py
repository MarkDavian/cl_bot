with open('.env', 'r') as file:
    env_token = file.readline()
    
class Settings():
    bot_token: str = env_token

settings = Settings()