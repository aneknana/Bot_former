''' return default logger '''
import logging

def get_logger(logger_name : str,
               console_level: int = None, file_level : int = None,
               file_name: str ='log.log', write_mode: str= 'a'):
    ''' levels to choose: [0 - NOTSET, 10 - DEBUG, 20 - INFO,
                           30 - WARN, 40 - ERROR, 50 - CRITICAL] '''
    if console_level is None and file_level is None:
        empty_fun = lambda self, *args, **kwargs: None
        return type('Blanky', (), {'debug': empty_fun, 'info': empty_fun,
                                   'warning': empty_fun, 'error': empty_fun,
                                   'critical': empty_fun})
    assert console_level in (None, 0, 10, 20, 30, 40, 50), f'Logging level console_level: {console_level} is not exist.'
    assert file_level in (None, 0, 10, 20, 30, 40, 50), f'Logging level file_level: {file_level} is not exist.'

    cst_logger = logging.getLogger(logger_name)
    cst_logger.setLevel(level=logging.DEBUG)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(asctime)s - %(message)s')

    for handler in cst_logger.handlers:
        cst_logger.removeHandler(handler)
        handler.close()

    if console_level is not None:
        c_handler = logging.StreamHandler()
        c_handler.setLevel(level = console_level)
        c_handler.setFormatter(formatter)
        cst_logger.addHandler(c_handler)

    if file_level is not None:
        f_handler = logging.FileHandler(file_name, write_mode, encoding ='utf-8')
        f_handler.setLevel(level = file_level)
        f_handler.setFormatter(formatter)
        cst_logger.addHandler(f_handler)

    return cst_logger
