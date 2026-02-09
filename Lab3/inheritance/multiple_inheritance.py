#1
class Athlete:
    def train(self):
        print("Training")

class Student:
    def study(self):
        print("Studying")

class StudentAthlete(Athlete, Student):
    pass
