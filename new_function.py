# sample.py

import os
import sys
import json  # unused
import re

def calculate(a,b):
 x = a + b
    if x > 10:
       print("greater than 10")
    else:
        print("less or equal to 10")
    return x

def get_userData():
    data = {"name":"John","age":30,"city":"New York"}
    for key in data.keys():
        print(key + "=>" + str(data[key]))
    return data

def multiply(x,y,z): return x*y*z

def unused_function():
    pass

class User:
 def __init__(self,name,age):
    self.n = name
    self.a = age
 def show(self):
     print("User:",self.n)

def main():
    result = calculate(5,7)
    print("Result is",result)
    info = get_userData()
    print(info)
    print(multiply(2,3,4))
    # hardcoded usage:
    user = User("Jane",25)
    user.show()

main()
