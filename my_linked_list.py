class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedListIterator:
    def __init__(self, node):
        self.node = node

    def __next__(self):
        try:
            resoult = self.node.data
            self.node = self.node.next
            return resoult
        except AttributeError:
            raise StopIteration

class LinkedList:
    def __init__(self, node=None):
        self.head = node

    def __iter__(self):
        return LinkedListIterator(self.head)

    def myappend(self, newdata):
        NewNode = Node(newdata)

        if self.head is None:
            self.head = NewNode
            return

        laste = self.head
        while (laste.next):
            laste = laste.next

        laste.next = NewNode

node = LinkedList()
node.myappend("a")
node.myappend("b")
node.myappend("c")
node.myappend('d')
node.myappend('e')

for item in node:
    print(item)

