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

print(one_circle.get_radius())
print(another_circle.get_radius())

class Door(object):
    def __init__(self):
        self.width=1
        self.height=1
        self.open=False
    
    def get_status(self):
        return self.open

    def get_area(self):
        return self.width*self.width

class Trac(object):
    def __init__(self):
        self.width=0
        self.height=0

    def change_width(self, width):
        self.width=width

    def change_height(self, height):
        self.height=height

    def get_width(self):
        return self.width

    def  get_height(self):
        return self.height

one_trac=Trac()
another_trac=Trac()
one_trac.change_width(4)
one_trac.change_height(2)
another_trac.change_height(5)
another_trac.change_width(7)

print(one_trac.get_width())
print(one_trac.get_height())
print(another_trac.get_height())
print(another_trac.get_width())
print(one_trac.get_height()*one_trac.get_width())
print(another_trac.get_width()*another_trac.get_height())
print(one_trac.get_width()*another_trac.get_height())
print(one_trac.get_height()*another_trac.get_width())