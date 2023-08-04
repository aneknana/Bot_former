''' new user handler '''
from typing import List, Dict
from bot_former import bot
from bot_former import action
from bot_former import user
from threading import Thread, Lock
from urllib3 import disable_warnings, exceptions

def all_admins_call(admins: List[int], user_info: Dict[str, any])-> None:
    ''' message to every admin '''
    for admin in admins:
        Thread(target = __confirm_msg__, args=(admin,user_info,)).start()
        # __confirm_msg__(admin,user_info)

def confirm(user_info)->None:
    ''' grant all permissions '''
    user_info['user_id'] = user_info.pop('id')
    new_user = user.User(**user_info)
    new_user.no_permissions()
    new_user.grant_permission(0)
    return f'Пользователь {user_info["username"]} добавлен.'

def deny(user_info)->None:
    ''' ignore user '''
    return f'Пользователю {user_info["username"]} отказано в доступе.'

def __actions__(user_info: Dict[str, any] = None):
    ''' inline actions '''
    return [{'text': 'yes',
             'callback_data':0,
             'function': lambda: confirm(user_info)},
            {'text': 'no',
             'callback_data':1,
             'function': lambda: deny(user_info)}]

def __confirm_msg__(admin: int, user_info: Dict[str, any])-> None:
    ''' message to admin '''
    inline_acts = {'newbie': {'inline_keyboard': [[{k: v for k, v in a.items() if k in ['text', 'callback_data']}] for a in __actions__()]}}
    fun_acts = [[v for k, v in a.items() if k == 'function'][0] for a in __actions__(user_info)]


    listener = bot.Bot(inline_acts, callbacks_fun=fun_acts)
    msg_to_answer = listener.__send_message_with_inline__(chat_id= admin,
                                                          reply_to_message_id= None,
                                                          text= f'Добавить нового пользователя {user_info["username"]} ({user_info["first_name"]} {user_info["last_name"]})?',
                                                          markup= inline_acts['newbie'])

    disable_warnings(exceptions.InsecureRequestWarning)
    while True:
        try:
            listener.call_response()
            if listener.last_callbacks_msg == msg_to_answer:
                msg_to_answer = listener.__send_message__(chat_id= user_info['user_id'],
                                                             reply_to_message_id= None,
                                                             text= 'You have permissions')

                break
        except KeyboardInterrupt:
            break