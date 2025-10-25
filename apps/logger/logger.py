from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod
import json
from threading import Lock

class LOG_LEVEL(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40

class Log:
    def __init__(self, log_level: LOG_LEVEL, message: str) -> None:
        self.time = datetime.now()
        self.message = message
        self.log_level = log_level
    
    def __str__(self) -> str:
        return f"{self.time:%Y-%m-%d %H:%M:%S} [{self.log_level.name}]: {self.message}"


class Formatter(ABC):
    @abstractmethod
    def format(self, message: Log) -> str:
        raise NotImplementedError
    

class SimpleFormatter(Formatter):
    def format(self, message: Log):
        return str(message)

class JsonFomatter(Formatter):
    def format(self, message: Log):
        return json.dumps({
            'time': str(message.time),
            'level': message.log_level.name,
            'message': message.message
        })

class LogHanlder(ABC):
    @abstractmethod
    def write(self, message: Log) -> None:
        raise NotImplementedError 

class ConsoleLogHandler(LogHanlder):
    def __init__(self, formater: Formatter | None) -> None:
        super().__init__()
        self.formater = formater or SimpleFormatter()
    
    def write(self, message: Log) -> None:
        print(self.formater.format(message))
    
class FileLogHandler(LogHanlder):
    def __init__(self, formater: Formatter | None, file_name: str) -> None:
        super().__init__()
        self.formater = formater or SimpleFormatter()
        self.file_name = file_name
        self.lock = Lock()
    
    def write(self, message: Log) -> None:
        with self.lock:
            with open(self.file_name, 'a') as f:
                f.write(self.formater.format(message) + '\n')


class Logger:
    def __init__(self, level: LOG_LEVEL) -> None:
        self.lock = Lock()
        self.handler: set[LogHanlder] = set([])
        self.level = level

    def add_hanlder(self, new_handler: LogHanlder):
        self.handler.add(new_handler)
    
    def log(self, message: Log, level: LOG_LEVEL):
        if level.value < self.level.value:
            return
        log_message = Log(level, message)
        with self.lock:
            for hanlder in self.handler:
                hanlder.write(log_message)
    
    def debug(self, message: str):
        self.log(message=message, level=LOG_LEVEL.DEBUG)
    
    def info(self, message: str):
        self.log(message=message, level=LOG_LEVEL.INFO)

    def warning(self, message: str):
        self.log(messasge=message, level=LOG_LEVEL.WARNING)
    
    def error(self, message: str):
        self.log(message=message, level=LOG_LEVEL.ERROR)
    
if __name__ == "__main__":
    logger = Logger(LOG_LEVEL.INFO)
    print_handler = ConsoleLogHandler(formater=JsonFomatter())
    #   print_handler2 = ConsoleHandler()
    print_handler2 = FileLogHandler(file_name="logs.txt", formater=JsonFomatter())

    logger.add_hanlder(print_handler)
    logger.add_hanlder(print_handler2)
    logger.info("This is message")
    logger.error("Something bad happened!")
    logger.log("this is waring message", LOG_LEVEL.WARNING)


