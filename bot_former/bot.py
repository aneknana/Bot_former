''' telegram bot blank '''
from typing import List, Dict
from json import dumps
import config_defaults
import requests

class Bot:
    ''' bot description '''
    def __init__(self, inline_keyboards: Dict[str, List[Dict[str, List[Dict[str, str]]]]], callbacks_fun: list = None) -> None:
        self.api_url: str = f'https://api.telegram.org/bot{self.__get_token__()}/'
        self.update_id = None
        self.inline_keyboards: dict = inline_keyboards
        self.callbacks_fun: list = [] if callbacks_fun is None else callbacks_fun

    @staticmethod
    def __get_token__() -> str:
        ''' get requestsSettings '''
        return config_defaults.read_settings()['requestsSettings']['token']

    def __get_updates__(self, timeout: int = 100) -> list:
        ''' get bot response '''
        try:
            responses = requests.get(f'{self.api_url}getUpdates?portal.okmarket.ru'
                            , params = {'offset': self.update_id}
                            , verify = False
                            , timeout = timeout).json()['result']
            if len(responses) > 0:
                self.update_id = responses[-1]['update_id'] + 1
            return responses
        except KeyError:# no key ['result'] on empty responce
            return []

    def __send_message__(self, text: str, chat_id: int, reply_to_message_id: int = None) -> int:
        ''' send message '''
        if reply_to_message_id is None:
            reply_to_message_id = {}
        _msg = requests.post(url = f'{self.api_url}sendMessage?portal.okmarket.ru',
                      data = {'chat_id': chat_id,
                              'text': text.replace(r'\n', '\n'),
                              'parse_mode': 'html',
                              'reply_to_message_id': reply_to_message_id},
                      verify = False)
        return _msg.json()['result']['message_id']

    def __forward_message__(self, text: str, chat_id: int, from_chat_id: int, message_id: int) -> int:
        ''' forward message '''
        _msg = requests.post(url = f'{self.api_url}forwardMessage?portal.okmarket.ru',
                      data = {'chat_id': chat_id,
                              'from_chat_id': from_chat_id,
                              'text': text.replace(r'\n', '\n'),
                              'parse_mode': 'html',
                              'message_id': message_id},
                      verify = False)
        return _msg.json()['result']['message_id']

    def __send_img__(self, photo: str, chat_id: int, reply_to_message_id: int = None) -> int:
        ''' send image '''
        if reply_to_message_id is None:
            reply_to_message_id = {}
        _msg = requests.post(url = f'{self.api_url}sendMessage?portal.okmarket.ru',
                      data = {'chat_id': chat_id,
                              'photo': photo,
                              'parse_mode': 'html',
                              'reply_to_message_id': reply_to_message_id},
                      verify = False)
        return _msg.json()['result']['message_id']

    def __send_message_with_inline__(self, chat_id: int
                                     , text: str
                                     , reply_to_message_id: int
                                     , markup: Dict[str, list]):
        ''' send menu to user '''
        _msg = requests.post(url = f'{self.api_url}sendMessage?portal.okmarket.ru',
                          data = {'chat_id': chat_id,
                                  'text': text,
                                  'reply_to_message_id': reply_to_message_id,
                                  'reply_markup': dumps(markup)},
                          verify = False)
        return _msg.json()['result']['message_id']

    def __delete_message__(self, chat_id : int, message_id : int) -> None:
        ''' delete message by id and chat id '''
        requests.post(url = f'{self.api_url}deleteMessage?portal.okmarket.ru',
                      data = {'chat_id': chat_id,
                              'message_id': message_id},
                      verify = False)

    def __manage_message__(self, message: dict) -> None:
        ''' work with <message> responses'''
        if message['text'].lower() in self.inline_keyboards:
            self.__send_message_with_inline__(
                chat_id = message['chat']['id'],
                reply_to_message_id = message['reply_to_message']['message_id'],
                text = 'Что делать?',
                markup = self.inline_keyboards[message['text'].lower()])

    def __manage_callback_query__(self, callback: dict) -> None:
        ''' work with <callback_query> responses'''
        if int(callback['data']) < len(self.callbacks_fun):
            self.__send_message__(text = self.callbacks_fun[int(callback['data'])](),
                                  chat_id = callback['message']['chat']['id'],
                                  reply_to_message_id = None)

    def __manage_response__(self, response : dict) -> None:
        ''' work with responses '''
        if 'callback_query' in response:
            self.__manage_callback_query__(response['callback_query'])
        if 'message' in response:
            self.__manage_message__(response['message'])

    def call_response(self) -> None:
        ''' get and work with responses '''
        responses = self.__get_updates__()
        for response in responses:
            self.__manage_response__(response)