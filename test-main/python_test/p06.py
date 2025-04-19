class Circle(object):
    def __init__(self):
        self.radius=0

    def change_radius(self, radius):
        self.radius=radius

    def get_radius(self):
        return self.radius

    def get_area(self):
        return 3.14*self.radius*self.radius

one_circle=Circle()
another_circle=Circle()

one_circle.change_radius(4)
another_circle.change_radius(0)

print(one_circle.get_radius())
print(another_circle.get_radius())

a=Circle()
print(a.get_area())
a.change_radius(3)
print(a.get_area())

class Rectangle(object):
    def __init__(self, length, widht):
        self.length=length
        self.width=widht

    def set_length(self, length):
        self.length=length

    def set_width(self, width):
        self.width=width

    def get_area(self):
        return self.length*self.width

    def get_perimeter(self):
        return 2*(self.length+self.width)

a_rectangle=Rectangle(2,4)