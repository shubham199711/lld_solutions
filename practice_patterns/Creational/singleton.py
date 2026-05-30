from threading import Lock

class Singleton:
    _ins = None
    _lock = Lock()

    def __new__(cls):
        if cls._ins is None:
            with cls._lock:
                if cls._ins is None:
                    cls._ins = super().__new__(cls)
        
        return cls._ins
    
    def __init__(self):
        self.data = []
    
    def add_val(self, val):
        self.data.append(val)

    
    def print_val(self):
        print(self.data)



if __name__ == "__main__":
    s1 = Singleton()
    s2 = Singleton()
    s1.add_val(1)

    s2.print_val()