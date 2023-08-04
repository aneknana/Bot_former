''' controm inline menu in terms of permissions '''
from typing import List, Dict, Callable
from bot_former import action
from bot_former import user

def actions_to_inline(actions : Dict[str, List[action.Action]]) -> List[Dict[str, Dict[str, list]]] :
    ''' put all actions intoto inline keyboards '''
    inline_keyboards = {}
    for key_word in actions:
        inline_keyboard = []
        for cur_action in actions[key_word]:
            assert hasattr(cur_action, '__name__'), 'Action object should have __name__ attribute.'
            inline_keyboard.append([{'text': cur_action.__name__,
                                     'callback_data': cur_action.action_id
                                     }])
        inline_keyboards[key_word.lower()] = {'inline_keyboard' : inline_keyboard}
    return inline_keyboards

def inline_keyboards_filter(inline_keyboards : Dict[str, Dict[str, list]], filt : List[int]) -> Dict[str, Dict[str, list]]:
    ''' filter existing keyboards '''
    new_kb = {}
    for key_word in inline_keyboards:
        filtered = [_ for _ in inline_keyboards[key_word]['inline_keyboard'] if _[0]['callback_data'] in filt]
        if filtered != []:
            new_kb[key_word] = {'inline_keyboard' : filtered}
    return new_kb

def add_user(user_info: Dict[str, any])->str:
    ''' grant all permissions '''
    user_info['user_id'] = user_info.pop('id')
    new_user = user.User(**user_info)
    new_user.full_permissions()
    return f'Пользователь {user_info["username"]} добавлен.'

def reject_user(user_info: Dict[str, any])->str:
    ''' ignore user '''
    return f'Пользователю {user_info["username"]} отказано в доступе.'

def admin_actions(task_id: int)-> Callable:
    ''' actions available from admin inline '''
    all_act = {0: add_user,
               1: reject_user}
    return all_act[task_id]

def admins_inline(mtalk_id):
    ''' return inline_keyboard for admin '''
    inline_keyboards = {'/join': {'inline_keyboard':
                                  [[{'text': 'yes',
                                     'callback_data':f'mt_{mtalk_id}_0'}],
                                  [{'text': 'no',
                                     'callback_data':f'mt,{mtalk_id}_1'}]]
                                  }}
    return inline_keyboards

def get_user_inline(user : object, inline_keyboards : Dict[str, Dict[str, list]]) -> Dict[str, Dict[str, list]]:
    ''' return inline_keyboard for users permissions '''
    if user.full_access:
        return inline_keyboards
    return inline_keyboards_filter(inline_keyboards, user.permissions)