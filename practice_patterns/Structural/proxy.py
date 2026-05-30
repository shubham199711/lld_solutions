class Document:
    def read_file(self):
        print("read a file")


class DocumentProxy:
    def __init__(self, role):
        self.role = role
        self.doc = Document()
    
    def read_file(self):
        if self.role != "admin":
            raise PermissionError()
        return self.doc.read_file()



d1 = DocumentProxy("admin")
d1.read_file()
        



