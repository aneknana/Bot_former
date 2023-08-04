''' users handler '''
from typing import List
from gc import get_objects
from bot_former import json_store

class User:
    ''' user access information object '''
    save_as_json : bool = True
    save_path : str = 'users_info.json'
    id_attr = 'user_id'

    def __init__(self, user_id : int, is_bot: bool, first_name : str, last_name : str, username : str,
                 language_code : str,  permissions : List[int] = None, full_access : bool = None) -> None:
        self.user_id : int = user_id
        self.is_bot : bool = is_bot
        self.first_name : str = first_name
        self.last_name : str = last_name
        self.username : str = username
        self.language_code : str = language_code
        self.permissions : list = [] if permissions is None else permissions
        self.full_access : bool = full_access
        self.__upd_in_path__()

    def __upd_in_path__(self):
        ''' save and update in .json '''
        if self.save_as_json:
            json_store.save_as_json(self.save_path, self, self.id_attr)

    def grant_permission(self, action_id : int) -> None:
        ''' add rights to action '''
        self.permissions.append(action_id)
        self.__upd_in_path__()

    def take_away_permission(self, action_id : int) -> None:
        ''' remove rights to action '''
        for i, acc in enumerate(self.permissions):
            if acc == action_id:
                del acc[i]
        self.__upd_in_path__()

    def iter_grant_permission(self, actions : List[int]) -> None:
        ''' add rights to list of actions '''
        any(self.grant_permission(a) for a in actions)

    def iter_take_away_permission(self, actions : List[int]) -> None:
        ''' remove rights to list of actions '''
        any(self.take_away_permission(a) for a in actions)

    def full_permissions(self) -> None:
        ''' add all rights '''
        self.full_access = True
        self.__upd_in_path__()

    def no_permissions(self) -> None:
        ''' remove all rights '''
        self.full_access = False
        self.permissions = []
        self.__upd_in_path__()

def find_user_by_id(user_id : int) -> User:
    ''' search for user '''
    if User.save_as_json:
        return find_user_in_storage(user_id)
    return find_user_in_memory(user_id)

def find_user_in_memory(user_id : int) -> User:
    ''' search for user in garbage collector '''
    for cur_user in get_objects():
        if isinstance(cur_user, User):
            if cur_user.user_id == user_id:
                return cur_user
    return None

def find_user_in_storage(user_id : int) -> User:
    ''' read save '''
    cur_user = json_store.find_in_storage(User.save_path, {User.id_attr : user_id})
    if cur_user is not None:
        return User(**cur_user)
    return None