# using dict + linked list create an LRU cache
class Node:
    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class LruCache:
    def __init__(self, capacity: int) -> None:
        self.dict = {}
        self.capacity = capacity


        self.head = Node(None, None)
        self.tail = Node(None, None)

        self.head.next = self.tail
        self.tail.prev = self.head


    def move_to_start(self, node):
        # update node
        node.next = self.head.next
        node.prev = self.head
        # update current head's previous to new node
        self.head.next.prev = node
        # current head next to new node
        self.head.next = node
    
    def delete_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def search(self, key):
        if key not in self.dict:
            return None
        node_found = self.dict[key]
        self.delete_node(node_found)
        self.move_to_start(node_found)
        return node_found.value
    
    def insert(self, key, value):
        if key not in self.dict:
            if self.capacity == len(self.dict):
                lru_node = self.tail.prev
                self.delete_node(lru_node)
                del self.dict[lru_node.key]
            node = Node(key, value)
            self.dict[key] = node
            self.move_to_start(node)
        else:
            node_found = self.dict[key]
            node_found.value = value
            self.delete_node(node_found)
            self.move_to_start(node_found)


    
if __name__ == "__main__":
    cache = LruCache(2)
    cache.insert(1, 1111)
    cache.insert(2, 2222)
    print(cache.search(1))  # 1
    cache.insert(3, 3)      # evicts key 2
    print(cache.search(2))  # None
    cache.insert(4, 4)      # evicts key 1
    print(cache.search(1))  # None
    print(cache.search(3))  # 3
    print(cache.search(4))  # 4