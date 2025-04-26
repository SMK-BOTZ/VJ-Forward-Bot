
from os import environ 

class Config:
    API_ID = int(environ.get("API_ID", "28055351"))
    API_HASH = environ.get("API_HASH", "4acf3a28b9745eb39b25a91478f9504b")
    BOT_TOKEN = environ.get("BOT_TOKEN", "7594003962:AAGzId8q2ioq1DfvxVOTq38NWhZXqGw2nsc") 
    BOT_SESSION = environ.get("BOT_SESSION", "siya") 
    DATABASE_URI = environ.get("DATABASE_URI", "mongodb+srv://misssiyaofficial:zzx4322CU68rU8gw@cluster0.frhwbd1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    DATABASE_NAME = environ.get("DATABASE_NAME", "cluster0")
    BOT_OWNER = int(environ.get("BOT_OWNER", "6879821587"))
    #  Single Channel (old way)
    # UPDATES_CHANNEL = "-1001234567890"  
    
    # Multiple Channels (new way)
    UPDATES_CHANNEL = ["-1002549170360", "-1002630469734", "-1002630469734"]

class temp(object): 
    lock = {}
    CANCEL = {}
    forwardings = 0
    BANNED_USERS = []
    IS_FRWD_CHAT = []
