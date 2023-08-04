''' starts telegram bot with actions keyboard '''
from typing import List, Dict
from urllib3 import disable_warnings, exceptions
from bot_former import log
from bot_former import action_handler

def infinite_loop(actions : Dict[str, List[object]], owner_name: str, threadder : bool = False) -> None:
    ''' run infinite loop '''
    logger = log.get_logger(__name__, console_level=10, file_level=10)
    listener = action_handler.Handler(actions, owner_name, threadder)
    disable_warnings(exceptions.InsecureRequestWarning)
    while True:
        try:
            listener.call_response()
        except KeyboardInterrupt:
            logger.debug('Interrupted by the user')
            break