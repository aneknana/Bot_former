''' single talk controller '''
from gc import get_objects
from bot_former import json_store

class Talk:
    ''' one conversation '''
    save_as_json : bool = True
    save_path : str = 'talks_info.json'
    id_attr = 'talk_id'
    def __init__(self, user_id : int, chat_id : int, talk_id : int,
                 last_msg : int = None, msgs : list = None,
                 task_info : list = None) -> None:
        self.user_id = user_id
        self.chat_id = chat_id
        self.talk_id = talk_id

        self.last_msg = talk_id if last_msg is None else last_msg
        self.msgs = [talk_id] if msgs is None else msgs
        self.task_info = [''] if task_info is None else task_info

        self.__upd_in_path__()

    def __upd_in_path__(self):
        ''' save and update in .json '''
        if self.save_as_json:
            json_store.save_as_json(self.save_path, self, self.id_attr)

    def new_msg(self, msg : int) -> None:
        ''' upd messages history '''
        self.last_msg = msg
        self.msgs.append(msg)
        self.__upd_in_path__()

    def add_task_info(self, info : str) -> None:
        ''' add information about task '''
        self.task_info.append(info)
        self.__upd_in_path__()

    def ids(self) -> dict:
        ''' return data to send new message '''
        return {'chat_id' : self.chat_id,
                'reply_to_message_id' : self.last_msg}

    def verify(self, username : str, chat_id : int, message_id : int) -> bool:
        ''' check if belong to the talk '''
        if (chat_id == self.chat_id
            and message_id in self.msgs
            and username == self.username):
            return True
        return False

def find_talk(chat_id : int, user_id : int, reply_to_message : int) -> Talk:
    ''' search for user '''
    if Talk.save_as_json:
        return find_talk_in_storage(chat_id, user_id, reply_to_message)
    return find_talk_in_memory(chat_id, user_id, reply_to_message)

def find_talk_in_memory(chat_id : int, user_id : int, reply_to_message : int) -> Talk:
    ''' search for user in garbage collector '''
    for cur_talk in get_objects():
        if isinstance(cur_talk, Talk):
            if cur_talk.chat_id == chat_id and cur_talk.user_id == user_id and reply_to_message in cur_talk.msgs:
                return cur_talk
    return None

def find_talk_in_storage(chat_id : int, user_id : int, reply_to_message : int) -> Talk:
    ''' read save '''
    cur_talk = json_store.find_in_storage(Talk.save_path, {'chat_id' : chat_id, 'user_id' : user_id}, {'msgs' : reply_to_message})
    if cur_talk is not None:
        return Talk(**cur_talk)
    return None