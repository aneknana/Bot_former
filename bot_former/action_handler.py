''' telegram bot blank '''
from typing import List, Dict, Callable
from functools import partial
from bot_former import bot
from bot_former import thread
from bot_former import talk
from bot_former import multitalk
from bot_former import user
from bot_former import let_me_in
from bot_former import permissions_handler as perms
from bot_former import log

logger = log.get_logger(__name__, console_level=10, file_level=10)

class Handler(bot.Bot):
    ''' bot description '''
    def __init__(self, actions: Dict[str, List[Callable]], owner: List[int], threader : bool = False) -> None:
        self.actions = {action.action_id : action
                        for key_word in actions
                        for action in actions[key_word]}
        super().__init__(perms.actions_to_inline(actions))
        self.thread = thread.ThreadObj(threader)
        self.owner = owner

    def __sub_functions__(self, action : Callable, curr_talk : object) -> None:
        ''' wrap report object with bot functions '''
        bot_funcs = {'print' : partial(self.user_output, this_talk = curr_talk),
                     'input' : partial(self.user_input, this_talk = curr_talk),
                     'after' : partial(self.clean_after, this_talk = curr_talk),
                     'print_img' : partial(self.img_output, this_talk = curr_talk)}
        for function in bot_funcs:
            if hasattr(action, function):
                setattr(action, function, bot_funcs[function])

    def __new_user_confirm__(self, message: Dict[str, any]) -> None:
        ''' ask owner if new user shoud be added '''
        logger.debug('Add user request: %s', message['from'])
        mtalk = multitalk.Multitalk(message['chat']['id'],
                                    message['message_id'],
                                    'join',
                                    message["from"]
            )
        for admin in self.owner:
            msg_to_answer = self.__send_message_with_inline__(chat_id= admin,
                                                              reply_to_message_id= None,
                                                              text= f'Добавить нового пользователя {message["from"]["username"]} ({message["from"]["first_name"]} {message["from"]["last_name"]})?',
                                                              markup= perms.admins_inline(mtalk.mtalk_id)['/join'])
            mtalk.update(msg_history=[admin, msg_to_answer])

    def __manage_message__(self, message: dict) -> None:
        ''' work with <message> responses'''
        this_user = user.find_user_by_id(message['from']['id'])
        if this_user is None and message['text'] == '/join':
            self.__new_user_confirm__(message)
        elif this_user is None:
            pass
        else:
            user_keyboards = perms.get_user_inline(this_user, self.inline_keyboards)
            if message['text'].lower() in user_keyboards:
                cur_talk = talk.Talk(this_user.user_id, message['chat']['id'], message['message_id'])
                cur_talk.new_msg(self.__send_message_with_inline__(
                    **cur_talk.ids(),
                    text = 'Что делать?',
                    markup = user_keyboards[message['text'].lower()]))

    def __manage_callback_query__(self, callback: dict) -> None:
        ''' work with <callback_query> responses'''
        if callback['data'][:2]=='mt':
            self.__manage_mtalk__(callback)
        else:
            self.__manage_talk__(callback)

    def __manage_talk__(self, callback: dict) -> None:
        ''' work with <callback_query> responses'''
        curr_talk = talk.find_talk(callback['message']['chat']['id'],
                                 callback['from']['id'],
                                 callback['message']['reply_to_message']['message_id'])
        if curr_talk is None:
            logger.debug('Talk by parameters not found: chat_id %s, user_id %s, message_id %s',
                         callback['message']['chat']['id'],
                         callback['from']['id'],
                         callback['message']['reply_to_message']['message_id'])
            return

        current_action = self.actions[int(callback['data'])]
        self.__sub_functions__(current_action, curr_talk)
        try:
            self.thread.thread_start(current_action)
            curr_talk.add_task_info(current_action.result_string)
        except Exception as ex:
            self.user_output(f'Exception occured {str(ex)}', curr_talk)

    def __manage_mtalk__(self, callback: dict) -> None:
        ''' work with <callback_query> responses'''
        mark, mtalk_id, task_id = callback['data'].split('_')
        curr_mtalk = multitalk.find_mtalk(int(mtalk_id))
        if curr_mtalk.closed:
            self.__send_message__(text = 'This task closed already with stat: {curr_mtalk.stat}',
                                  chat_id = callback['message']['chat']['id'])
            self.__delete_message__(chat_id= callback['message']['chat']['id'],
                                    message_id= callback['message']['id'])
        else:
            result = perms.admin_actions(int(task_id))(curr_mtalk.args)
            curr_mtalk.update(result, True)
            for chat, msg in curr_mtalk.msg_history:
                self.__send_message__(text = result,
                                      chat_id = chat)
                self.__delete_message__(chat_id = chat,
                                        message_id = msg)

    def user_output(self, text: str, this_talk: object) -> None:
        ''' send message to user '''
        _msg = self.__send_message__(text, **this_talk.ids())
        this_talk.new_msg(_msg)

    def user_input(self, this_talk: object) -> str:
        ''' wait for user answer '''
        self.thread.acquire()
        while True:
            try:
                responses = self.__get_updates__()
                for response in responses:
                    if 'message' in response:
                        self.thread.release()
                        this_talk.new_msg(response['message']['message_id'])
                        return response['message']['text']
                    self.__manage_response__(response)
            except KeyError:# no key ['result'] on empty responce
                pass

    def img_output(self, img_path: str, this_talk: object) -> None:
        ''' send image to user '''
        _msg = self.__send_img__(img_path, **this_talk.ids())
        this_talk.new_msg(_msg)

    def clean_after(self, this_talk : object) -> None:
        ''' clean up task '''
        for _msg in this_talk.msgs[:-1]:
            self.__delete_message__(chat_id = this_talk.chat_id,
                                    message_id = _msg)