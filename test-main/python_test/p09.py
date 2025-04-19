class fraction(object):
    def __init__(self, top, bottom):
        self.top=top
        self.bottom=bottom   

    def __add__(self, other_fraction):
        new_top=self.top*other_fraction.bottom + self.bottom*other_fraction.top   
        new_bottom=self.bottom*other_fraction.bottom  
        return fraction(new_top, new_bottom)

    def __mul__(self, other_fraction):
        new_top=self.top*other_fraction.top
        new_bottom=self.bottom*other_fraction.bottom
        return fraction(new_top, new_bottom)

    def __str__(self):
        return str(self.top)+"/"+str(self.bottom)

    def __sub__(self, other_fraction):
        top=self.top*other_fraction.bottom - self.bottom*other_fraction.top
        bottom=self.bottom*other_fraction.bottom
        return fraction(top, bottom)

half=fraction(1,2)
half_string=str(half)
quarter=fraction(1,4)
half.__add__(quarter)
fraction.__add__(half, quarter)
print(half+quarter)
print(half)

quarter*half
quarter.__mul__(half)
fraction.__mul__(quarter, half)

print(quarter)
quarter.__str__()
fraction.__str__(quarter)

print(half*half)
(half.__mul__(half)).__str__()
fraction.__str__(fraction.__mul__(half, half))