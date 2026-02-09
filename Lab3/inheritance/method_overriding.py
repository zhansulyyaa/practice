#1
class Person:
    def printname(self):
        print("First and last name")

class Student(Person):
    def printname(self):
        print("Student name")

#2
class Student(Person):
    def welcome(self):
        print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)
