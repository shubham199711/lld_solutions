from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class TextEditor:
    def __init__(self):
        self.content = ""

    def insert(self, text):
        self.content += text

    def delete(self, count):
        deleted = self.content[-count:]
        self.content = self.content[:-count]
        return deleted


class InsertTextCommand(Command):
    def __init__(self, editor, text):
        self.editor = editor
        self.text = text

    def execute(self):
        self.editor.insert(self.text)

    def undo(self):
        self.editor.delete(len(self.text))


class DeleteTextCommand(Command):
    def __init__(self, editor, count):
        self.editor = editor
        self.count = count
        self.deleted_text = ""

    def execute(self):
        self.deleted_text = self.editor.delete(self.count)

    def undo(self):
        self.editor.insert(self.deleted_text)


class CommandManager:
    def __init__(self):
        self.history = []

    def execute(self, command):
        command.execute()
        self.history.append(command)

    def undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()


editor = TextEditor()
manager = CommandManager()

manager.execute(InsertTextCommand(editor, "Hello "))
manager.execute(InsertTextCommand(editor, "World"))

print(editor.content)  # Hello World

manager.undo()
print(editor.content)  # Hello

manager.undo()
print(editor.content)  #