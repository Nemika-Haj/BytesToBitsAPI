from cryptography.fernet import Fernet

from PyJS.modules import fs

security = Fernet(fs.createReadStream("data/key.key").chunk().encode('utf-8'))

def encrypt(token):
    return security.encrypt(token.encode('utf-8'))

def decrypt(token):
    return security.decrypt(token).decode('utf-8')