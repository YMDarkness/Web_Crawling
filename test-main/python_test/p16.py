import unittest

class TestMyCode(unittest.TestCase):
    def test_addition_2_2(self):
        self.assertEqual(2+2,4)

    def test_subtraction_2_2(self):
        self.assertNotEqual(2-2,4)

    def test_addition_5_5(self):
        self.assertEqual(5+5,10)

    def test_remainder_6_2(self):
        self.assertEqual(6%2,0)

unittest.main()

############################################################

def is_prime(n):
    prime=True
    for i in range(1,n): # for i in range(1,2) -> for i in range (2,n)
        if n%i==0:
            prime=False
            return prime
        
def absolute_value(n):
    if n < 0:
        return -n
    elif n > 0: #elif n > 0 -> elif n >= 0
        return n

################################################

import unittest
import test

class TestPrime(unittest.TestCase):
    def test_prime_5(self):
        isprime = test.is_prime(5)
        self.assertEqual(isprime, True)
    
    def Test_prime_4(self):
        isprime = test.is_prime(4)
        self.assertEqual(isprime, False)

    def Test_prime_10000(self):
        isprime = test.is_prime(10000)
        self.assertEqual(isprime, False)

class TestAbs(unittest.TestCase):
    def test_abs_5(self):
        absolute = test.absolute_value(5)
        self.assertEqual(absolute, 5)

    def test_abs_neg5(self):
        absolute = test.absolute_value(-5)
        self.assertEqual(absolute, 5)

    def test_abs_0(self):
        absolute = test.absolute_value(0)
        self.assertEqual(absolute, 0)

unittest.main()