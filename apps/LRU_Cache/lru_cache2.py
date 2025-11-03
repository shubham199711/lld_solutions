class Node:
    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value
        self.next = None
        self.prev = None


class LruCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache = {}

        # head and tail fake node
        self.head = Node(None, None)
        self.tail = Node(None, None)

        # attach values
        self.head.next = self.tail
        self.tail.prev = self.head
    

    def delete_node(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def add_at_start(self, node: Node):
        node.next = self.head.next
        node.prev = self.head

        # update previous head
        self.head.next.prev = node
        self.head.next = node
    
    def search(self, key):
        if key not in self.cache:
            return None
        node = self.cache[key]
        self.delete_node(node)
        self.add_at_start(node)
        return node.value
    
    def put(self, key, value):
        if key not in self.cache:
            if self.capacity == len(self.cache):
                # lru
                lru_node = self.tail.prev
                self.delete_node(lru_node)
                del self.cache[lru_node.key]
            node = Node(key, value)
            self.cache[key] = node
            self.add_at_start(node)
        else:
            node = self.cache[key]
            node.value = value
            self.delete_node(node)
            self.add_at_start(node)


if __name__ == "__main__":
    cache = LruCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.search(1))  # 1 (recently used)
    cache.put(3, 3)         # evicts key 2
    print(cache.search(2))  # None (evicted)
    cache.put(4, 4)         # evicts key 1
    print(cache.search(1))  # None (evicted)
    print(cache.search(3))  # 3
    print(cache.search(4))  # 4
