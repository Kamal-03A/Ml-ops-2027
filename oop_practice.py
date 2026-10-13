
# Exercise 1: Student Class

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}")


s1 = Student("Kamal", 22)
s1.display_info()


# Exercise 2: University Class and Class Methods

class University:
    university_name = "BAU"

    @classmethod
    def display_university(cls):
        print(cls.university_name)

    @classmethod
    def change_university(cls, new_name):
        cls.university_name = new_name


University.display_university()
University.change_university("University of Jordan")
University.display_university()


# Exercise 3: Employee Class

class Employee:
    company = "TechCorp"

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def display_info(self):
        print(self.name, self.salary, Employee.company)

    @classmethod
    def change_company(cls, new_company):
        cls.company = new_company


e1 = Employee("Kamal", 800)
e2 = Employee("Ahmad", 1000)

e1.display_info()
e2.display_info()

Employee.change_company("AI Solutions")

e1.display_info()
e2.display_info()
# Exercise 4: Inheritance
import datetime

import pandas as pd

class LoggedDF (pd.DataFrame):
    def __init__ (self,*args,**kwargs):
         pd.DataFrame. __init__(self,*args,**kwargs)
         self.created_at = datetime.today()
         
    
ldf = LoggedDF({"col1": [1,2], "col2": [3,4]})
print(ldf.values)
print(ldf.created_at)
