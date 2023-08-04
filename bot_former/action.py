''' reports collection '''
from typing import Dict, Any, Callable
from itertools import count
from os import remove
from matplotlib import figure
from pandas import DataFrame
from bot_former import log

logger = log.get_logger(__name__, console_level=10, file_level=10)

class Action:
    ''' base report class '''
    newid = count()
    def __init__(self, name: str, task: Callable) -> None :
        self.action_id = next(Action.newid)
        self.__name__ = name
        self.task = task
        self.arguments: Dict[str, Any] = {}
        self.result_string = f'Name: {name}'

    @staticmethod
    def before() -> None:
        ''' run befoore call '''
    @staticmethod
    def input() -> None:
        ''' function to get data from user '''
        return input()
    @staticmethod
    def print(text : str) -> None:
        ''' function to write message to user '''
        print(text)
    @staticmethod
    def result(text : str) -> None:
        ''' function to write final message to user '''
        print(text)
    @staticmethod
    def print_img(img : str) -> None:
        ''' function to write img-message to user '''
        print(f'''I don't know how to print {img} (((''')
    @staticmethod
    def print_table(table : DataFrame) -> None:
        ''' function to write table-message to user '''
        print(f'''I don't know how to print {table} (((''')
    @staticmethod
    def after() -> None:
        ''' run after call '''

    def args_needed(self) -> None:
        ''' check if arguments needded for task '''
        if hasattr(self.task, '__code__'):
            for _ in self.task.__code__.co_varnames[:self.task.__code__.co_argcount]:
                self.print(f'Task {self.__name__} needs argument - {_}:')
                arg = self.input()
                try:
                    arg = int(arg)
                except ValueError:
                    try:
                        arg = float(arg)
                    except ValueError:
                        pass
                self.arguments[_] = arg
        self.result_string += ('.' if self.arguments == {} else f' with args: {self.arguments}.')

    def __call__(self):
        ''' run task of report '''
        self.before()
        try:
            self.args_needed()
            result = self.task(**self.arguments)
            if type(result) in [int, float, bool, str, list, tuple, set, frozenset, dict]:
                self.print(f'TASK DONE!\n{self.result_string}\n{str(result)}')
            else:
                if result is None:
                    pass
                elif isinstance(result, figure.Figure):
                    result.savefig('temp.jpg')
                    self.print_img('temp.jpg')
                    remove('temp.jpg')
                elif isinstance(result, DataFrame):
                    self.print_table(result)
                else:
                    self.result_string += '\nUnknown return'
                self.print(f'TASK DONE!\n{self.result_string}')
        except Exception as ex:
            logger.debug('Exception %s', str(ex))
            self.result_string += f'\nException {str(ex)}'
            self.print(f'{self.result_string}')
        self.after()

    def __repr__(self) -> str:
        return self.__name__