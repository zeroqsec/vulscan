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
MHOST = '127.0.0.1'
MPORT = '3306'
MDATABASE = 'vulhub'
MUSERNAME = 'root'
MPASSWORD = '123456'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(MUSERNAME,MPASSWORD,MHOST,MPORT,MDATABASE)

# redis
RHOST = '127.0.0.1'
RPORT = '6379'
RPASSWORD = '123456'


# AES encrypt
from app.common.encrypt import generateKey,getIv
key = generateKey(16)
iv = getIv(key)



