
from abc import ABC, abstractmethod

class FileSystemItem(ABC):

    @abstractmethod
    def show(self, level=0):
        pass


class File(FileSystemItem):
    def __init__(self, name):
        self.name = name
    
    def show(self):
        print(self.name)

class Folder(FileSystemItem):
    def __init__(self, name):
        self.name = name
        self.child = []
    
    def add_child(self, item: FileSystemItem):
        self.child.append(item)
    
    def show(self):
        print(self.name)
        for item in self.child:
            item.show()


root = Folder("root")
root.add_child(File("a.txt"))

docs = Folder("docs")
docs.add_child(File("resume.pdf"))

root.add_child(docs)

root.show()