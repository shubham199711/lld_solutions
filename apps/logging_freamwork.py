from enum import Enum
from abc import ABC
from datetime import datetime
from threading import Lock
import json
from typing import Optional

class LogLevel(Enum):
  DEBUG = 10
  INFO = 20
  WARNING = 30
  ERROR = 40

class Log:
  def __init__(self, level: LogLevel, message: str):
    self.time = datetime.now()
    self.level = level
    self.message = message

  def __str__(self):
    return f"{self.time:%Y-%m-%d %H:%M:%S} [{self.level.name}]: {self.message}"

class Formatter(ABC):
  def __init__(self):
    pass
  
  def format(self, message: Log) -> str:
    return ""
  

class SimpleFormatter(Formatter):
  def __init__(self):
    pass
  
  def format(self, message: Log):
    return str(message)


class JSONFormatter(Formatter):
  def __init__(self):
    pass

  def format(self, message: Log):
    return json.dumps({"datetime": str(message.time), "level": message.level.name, "message": message.message})
    

class LogHandler(ABC):
  def __init__(self):
    pass

  def emit(self, message: Log):
    pass

class ConsoleHandler(LogHandler):
  def __init__(self, formatter: Optional[Formatter] = None):
    self.formatter = formatter or SimpleFormatter()

  def emit(self, message: Log):
    print(self.formatter.format(message))

class FileHandler(LogHandler):
  def __init__(self, filename: str, formatter: Optional[Formatter] = None):
    self.filename = filename
    self.lock = Lock()
    self.formatter = formatter or SimpleFormatter()

  def emit(self, message: Log):
    with self.lock:
      with open(self.filename, "a") as f:
        f.write(self.formatter.format(message) + "\n")

class Logger:
  def __init__(self, level: LogLevel):
    self.level = level
    self.lock = Lock()
    self.handler = set([])

  def add_handler(self, new_handler: LogHandler):
    self.handler.add(new_handler)

  def log(self, level: LogLevel, message: str):
    if level.value < self.level.value:
      return
    log_message = Log(level, message)
    with self.lock:
      for handler in self.handler:
        handler.emit(log_message)

  def debug(self, message: str): self.log(LogLevel.DEBUG, message)
  def info(self, message: str): self.log(LogLevel.INFO, message)
  def warning(self, message: str): self.log(LogLevel.WARNING, message)
  def error(self, message: str): self.log(LogLevel.ERROR, message)


if __name__ == "__main__":
  logger = Logger(LogLevel.INFO)
  print_handler = ConsoleHandler(formatter=JSONFormatter())
#   print_handler2 = ConsoleHandler()
  print_handler2 = FileHandler(filename="logs.txt", formatter=JSONFormatter())

  logger.add_handler(print_handler)
  logger.add_handler(print_handler2)
  logger.info("This is message")
  logger.error("Something bad happened!")
  logger.log(LogLevel.WARNING, "this is waring message")