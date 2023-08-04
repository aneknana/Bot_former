''' json handler '''
import json
from bot_former import log

logger = log.get_logger(__name__, console_level=10, file_level=10)

def find_in_storage(directory : str, keys : dict, any_in_iter : dict = None) -> dict:
    ''' get dict of object attributes from json '''
    try:
        with open(directory, 'r', encoding="utf-8") as file:
            for line in file:
                stored = json.loads(json.loads(line))
                if all((k in stored and stored[k] == v for k, v in keys.items())):
                    if any_in_iter is None:
                        return stored
                    if all((k in stored and v in stored[k] for k, v in any_in_iter.items())):
                        return stored
        return None
    except FileNotFoundError:
        return None

def find_last_keys(directory : str, keys : list) -> dict:
    ''' get last key '''
    last_keys = {_: 0 for _ in keys}
    try:
        with open(directory, 'r', encoding="utf-8") as file:
            for line in file:
                stored = json.loads(json.loads(line))
                if any(v < stored[k] for k, v in last_keys.items()):
                    last_keys = dict(filter(lambda _: _[0] in keys, stored.items()))
        return last_keys
    except FileNotFoundError:
        return last_keys

def save_new(directory : str, obj : object) -> None:
    ''' json save if not exist '''
    obj = json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True)
    try:
        with open(directory, 'a', encoding="utf-8") as file:
            json.dump(obj, file)
            file.write('\n')
    except Exception as ex:
        logger.debug('save_new - Exception: %s', str(ex))

def update(directory, obj, stored_object : dict) -> None:
    ''' json save if exist '''
    try:
        with open(directory, 'r+') as file:
            text = file.read()
            text = text.replace(json.dumps(stored_object).replace('"', '\\"'),
                                json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True).replace('"', '\\"'))
            file.seek(0)
            file.write(text)
            file.truncate()
    except Exception as ex:
        logger.debug('update - Exception: %s', str(ex))

def save_as_json(directory : str, obj : object, id_name : str) -> None:
    ''' json save if not exist '''
    stored_object = find_in_storage(directory, {id_name : getattr(obj, id_name)})
    if stored_object is None:
        save_new(directory, obj)
    else:
        update(directory, obj, stored_object)