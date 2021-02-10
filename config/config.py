# path
currentDirPath = __file__.replace("\config\config.py","")
xssPayloadPath = "{}\\scan\\payloads\\{}".format(currentDirPath,'xspayload.txt')
vulResultPath = "{}\\scan\\result".format(currentDirPath)
pocPath = "{}\\scan\\{}\\poc".format(currentDirPath,'universal')

# process
processCount = 5

# coroutines
concurrency = 5
debug = True

# mysql
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'vulhub'
USERNAME = 'root'
PASSWORD = '123456'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOST,PORT,DATABASE)


# AES encrypt
from app.common.encrypt import generateKey,getIv
key = generateKey(16)
iv = getIv(key)



