class Complex:
    def __init__(self, real=0, imaginary=0):
        self.real = real
        self.imaginary = imaginary

    def __str__(self):
        return '{} + i*{}'.format(self.real, self.imaginary)

    def __add__(self, obj):
        res = Complex()
        if type(obj) == type(self):
            res.real = obj.real + self.real
            res.imaginary = obj.imaginary + self.imaginary
        else:
            res.real = self.real + obj
            res.imaginary = self.imaginary
        return res

    def __sub__(self, obj):
        res = Complex()
        if type(obj) == type(self):
            res.real = obj.real - self.real
            res.imaginary = obj.imaginary + self.imaginary
        else:
            res.real = self.real - obj
            res.imaginary = self.imaginary
        return res

    def __mul__(self, obj):
        res = Complex()
        if type(obj) == type(self):
            res.real = self.real * obj.real - obj.imaginary * self.imaginary
            res.imaginary = self.real * obj.imaginary + obj.real * self.imaginary
        else:
            res.real = self.real * obj
            res.imaginary = self.imaginary * obj
        return res

    def __truediv__(self, obj):
        res = Complex()
        if type(obj) == type(self):
            obj1 = Complex(obj.real, - obj.imaginary)
            obj1.real /= obj.real ** 2 + obj.imaginary ** 2
            obj1.imaginary /= obj.real ** 2 + obj.imaginary ** 2
            res = obj1
        else:
            res.real = self.real / obj
            res.imaginary = self.imaginary / obj
        return res

    def __pow__(self, power, modulo=None):
        if type(power) == int:
            if power == 0:
                return 1
            else:
                return self * self.__pow__(power - 1)

    def conjugate(self):
        return Complex(self.real, -self.imaginary)
