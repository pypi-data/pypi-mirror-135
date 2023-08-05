class ListNode:
    def __init__(self, val: int, prev_node=None, next_node=None):
        self.val = val
        self.prev_node = prev_node
        if self.prev_node:
            self.prev_node.next_node = self
        self.next_node = next_node
        if self.next_node:
            self.next_node.prev_node = self

    def __str__(self):
        return str(self.val)

    def __iter__(self):
        node = self
        while node:
            yield node.val
            node = node.next_node

    def pop_prev(self):
        if self.prev_node:
            return self.prev_node.pop()

    def pop_next(self):
        if self.next_node:
            return self.next_node.pop()

    def pop(self):
        if self.prev_node:
            self.prev_node.next_node = self.next_node
        if self.next_node:
            self.next_node.prev_node = self.prev_node
        return self

    def insert_after(self, val: int):
        node = ListNode(val, self, self.next_node)
        if self.next_node:
            self.next_node.prev_node = node
        self.next_node = node
        return node

    def insert_before(self, val: int):
        node = ListNode(val, self.prev_node, self)
        if self.prev_node:
            self.prev_node.next_node = node
        self.prev_node = node
        return node

    @classmethod
    def from_list(cls, elems):
        head = None
        current = None
        for e in elems:
            if not current:
                head = current = ListNode(e)
            else:
                current = current.insert_after(e)
        return head


class SinglyListNode:
    def __init__(self, val=0, next_node=None):
        self.val = val
        self.next_node = next_node

    def has_next(self):
        return self.next_node != None

    def __iter__(self):
        node = self
        while node:
            yield node.val
            node = node.next_node

    def __str__(self):
        return str(self.val) + ("" if self.next_node is None else "->[" + str(self.next_node.val) + "...]")

    def reverse(self, append=None):
        if self.next_node is None:
            self.next_node = append
            return self

        tail = self.next_node
        self.next_node = append
        return tail.reverse(self)

    @classmethod
    def from_list(cls, elems):
        head = None
        tail = None
        for e in elems:
            node = SinglyListNode(e)
            if tail is None:
                head = node
            else:
                tail.next_node = node
            tail = node
        return head
