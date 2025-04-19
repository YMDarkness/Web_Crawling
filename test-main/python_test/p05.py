class Rectangle(object):
    """length,width"""
    def __init__(self, length, width):
        self.length=length
        self.width=width

    def self_length(self, length):
        self.length=length

    def self_width(self, width):
        self.width=width

a_rectangle=Rectangle(2,4)
print(a_rectangle)

class Circle(object):
    def __init__(self):
        self.radius=0

    def change_radius(self, radius):
        self.radius=radius

    def get_radius(self):
        return self.radius

one_circle=Circle()
another_circle=Circle()

one_circle.change_radius(4)
another_circle.change_radius(2)

print(one_circle.get_radius())
print(another_circle.get_radius())

c=Circle()
c.change_radius(2)
r=c.get_radius()
print(r)

Circle.change_radius(c, 5)
r=Circle.get_radius(c)
print(r)

class rect(object):
    def __init__(self,len,hie):
        self.len=len
        self.hie=hie

    def set_len(self,len):
        self.len=len

    def set_wid(self, wid):
        self.wid=wid

a=rect(1,1)
b=rect(1,1)
rect.set_len(a, 4)
rect.set_wid(b, 4)