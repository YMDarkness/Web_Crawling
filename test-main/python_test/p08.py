class queue(object):
    def __init__(self):
        self.queue=[]

    def get_queue_elements(self):
        return self.queue.copy()

    def add_one(self, item):
        self.queue.append(item)

    def add_many(self, item, n):
        for i in range(n):
            self.queue.append(item)

    def remove_one(self):
        self.queue.pop(0)

    def remove_many(self, n):
        for i in range(n):
            self.queue.pop(0)

    def size(self):
        return len(self.queue)
    
    def prettyprint(self):
        for thing in self.queue[::-1]:
            print('|_',thing,'_|')

a=queue()
a.add_one(3)
a.add_one(1)
a.prettyprint()
a.add_many(6,2)
a.prettyprint()
a.remove_one()
a.prettyprint()
b=queue()
b.prettyprint()
print('---------------------')

class stack(object):
    def __init__(self):
        self.stack=[]

    def get_stack_elements(self):
        return self.stack.copy()

    def add_one(self, item):
        self.stack.append(item)

    def add_many(self, item, n):
        for i in range(n):
            self.stack.append(item)

    def remove_one(self):
        self.stack.pop()

    def remove_many(self, n):
        for i in range(n):
            self.stack.pop()

    def size(self):
        return len(self.stack)

    def prettyprint(self):
        for thing in self.stack[::-1]:
            print('|',thing,'|')

s=stack()
s.add_many('Y', 4)
s.add_one('R')
s.add_one('W')
s.prettyprint()

