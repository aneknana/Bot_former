''' create basic config file '''
from sys import argv
from os import path
from configparser import ConfigParser

def __get_args__() -> dict:
    ''' get arguments '''
    token, chat, *admin = argv[1:]
    return {'token': token, 'chat': chat, 'admin': admin}

def __get_path__() -> str:
    '''return path to settings'''
    return path.dirname(path.abspath(__file__)) + '\\settings.ini'

def __create_settings__(token: str, chat: str, admin: str) -> None:
    '''create a config file'''
    token, chat = str(token), str(chat)
    admin = '['+', '.join(map(str, admin))+']' if isinstance(admin, list) else admin
    data_path = __get_path__()
    config = ConfigParser()
    config.add_section('requestsSettings')
    config.set('requestsSettings',
               'token', token)
    config.set('requestsSettings',
               'chat', chat)
    config.set('requestsSettings',
               'admin', admin)
    with open(data_path, 'w') as config_file:
        config.write(config_file)

def read_settings():
    '''read a config file'''
    data_path = __get_path__()
    if not path.isfile(data_path):
        token = input('Telegram bot token needed')
        chat = input('Telegram chatid needed')
        admin = input('Telegram admin list needed')
        __create_settings__(token, chat, admin)
    config = ConfigParser()
    config.read(data_path)
    return config

if __name__ == '__main__':
    __create_settings__(**__get_args__())