class Stack(object):
    def __init__(self):
        self.stack=[]

    def get_stack_elements(self):
        return self.stack.copy()

    def add_one(self, item):
        self.stack.append(item)

    def add_many(self, item, n):
        for i in range(n):
            self.stack.append(item)
    
    def add_list(self, L):
        for e in L:
            self.stack.append(e)

    def remove_one(self):
        self.stack.pop()

    def remove_many(self, n):
        for i in range(n):
            self.stack.pop()

    def size(self):
        return len(self.stack)

    def prettyprint(self):
        for thing in self.stack[::-1]:
            print('|_',thing,'_|')

buchim=Stack()
buchim.add_one("seafood")
buchim.add_many("photato",4)
print(buchim.size())
buchim.remove_one()
print(buchim.size())
buchim.prettyprint()

print('------------------------')
freud=Stack()
freud.add_one("        Semper te recordor       ")
freud.add_one("       Vires acquirit eundo      ")
freud.add_one("  Magna vis est, Magnum Officium ")
freud.add_one("      Dum vita est, spes est     ")
freud.add_one("         Nil desperandum         ")
freud.add_one(" Faber est suae quisque fortunae ")
print(freud.size())
freud.prettyprint()
print('------------------------')

class Circle(object):
    def __init__(self):
        self.radius=0

    def change_raidu(self, radius):
        self.radius=radius

    def get_radius(self):
        return self.radius

a=Circle()
a.change_raidu(5)
print(a.get_radius())
b=Circle()
b.change_raidu(3)
r=b.get_radius()
print(r)
print('------------------------')

circles=Stack()
one_circle=Circle()
one_circle.change_raidu(2)
circles.add_one(one_circle)

for i in range(5):
    one_circle=Circle()
    one_circle.change_raidu(1)
    circles.add_one(one_circle)

print(circles.size())
circles.prettyprint()
print('-------------------------')

circles=Stack()
one_circle=Circle()
one_circle.change_raidu(2)
circles.add_one(one_circle)

one_circle=Circle()
one_circle.change_raidu(1)
circles.add_many(one_circle, 5)

print(circles.size())
circles.prettyprint()
print('-------------------------')

circles=Stack()
for i in range(3):
    one_circle=Circle()
    one_circle.change_raidu(3)
    circles.add_one(one_circle)
print('-------------------------')

class Rectangle(object):
    def __init__(self,length,width):
        self.length=length
        self.width=width

    def set_length(self,length):
        self.length=length

    def set_width(self, width):
        self.width=width

rect=Stack()
one_rect=Rectangle(1,1)
rect.add_many(one_rect, 5)
print('--------------------------')

