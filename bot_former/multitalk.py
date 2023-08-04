''' multiple users talk class '''
from typing import Dict, List
from gc import get_objects
from bot_former import json_store

class Multitalk:
    ''' object to collect information about talks where responce from another user needed '''
    save_as_json : bool = True
    save_path : str = 'mtalks_info.json'
    id_attr = 'mtalk_id'
    def __init__(self,
                 chat: int,
                 msg: int,
                 action: str,
                 args: Dict[str, any],
                 mtalk_id: int= None,
                 msg_history: List[List[int]] = None,
                 stat: str = None,
                 closed: bool = None):
        self.mtalk_id: int = mtalk_id if mtalk_id is not None else json_store.find_last_keys(self.save_path, [self.id_attr])[self.id_attr]+1
        self.chat: int = chat
        self.msg: int = msg
        self.action: str = action
        self.args: Dict[str, any] = args
        self.msg_history: List[List[int]] = [[chat, msg]] if msg_history is None else msg_history
        self.stat: str = 'created' if stat is None else stat
        self.closed: bool = False if closed is None else closed

        self.__upd_in_path__()

    def __upd_in_path__(self):
        if self.save_as_json:
            json_store.save_as_json(self.save_path, self, self.id_attr)

    def update(self, new_stat: str = None, new_closed: bool = None, msg_history: list = None)-> None:
        ''' update information about statuse and type closed '''
        if new_stat is not None:
            self.stat = new_stat
        if new_closed is not None:
            self.closed = new_closed
        if msg_history is not None:
            self.msg_history.append(msg_history)
        self.__upd_in_path__()

def find_mtalk(mtalk_id : int) -> Multitalk:
    ''' search for user '''
    if Multitalk.save_as_json:
        return find_mtalk_in_storage(mtalk_id)
    return find_mtalk_in_memory(mtalk_id)

def find_mtalk_in_memory(mtalk_id : int) -> Multitalk:
    ''' search for user in garbage collector '''
    for cur_mtalk in get_objects():
        if isinstance(cur_mtalk, Multitalk):
            if cur_mtalk.mtalk_id == mtalk_id:
                return cur_mtalk
    return None

def find_mtalk_in_storage(mtalk_id: int) -> Multitalk:
    ''' read save '''
    cur_mtalk = json_store.find_in_storage(Multitalk.save_path, {'mtalk_id' : mtalk_id})
    if cur_mtalk is not None:
        return Multitalk(**cur_mtalk)
    return None