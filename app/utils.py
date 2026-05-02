import hashlib
from config import Config
SECRET = Config.HASH_SECRET

def get_hash(ip, user_agent):
    return hashlib.sha256((ip + user_agent + SECRET).encode()).hexdigest()