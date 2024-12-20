"""
    Инициализация администратора. 
    Администратор может быть только один.
"""
import configparser
import base64
from models import Administrator

def init_administrator():
    """
    Инициализация администратора.
    """
    config = configparser.ConfigParser()
    config.read("admin_config.ini")
    administrator = Administrator(
        username = config["ADMINISTRATOR"]["username"],
        password = base64.b64encode(config["ADMINISTRATOR"]["password"].encode('ascii'))
    )
    return administrator
