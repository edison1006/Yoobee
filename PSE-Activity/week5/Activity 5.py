# person.py
class Person:
    def __init__(self, name, address, age):
        self.name = name
        self.address = address
        self.age = age

    def greet(self):
        print(f"Hello, my name is {self.name}, I live at {self.address}, and I am {self.age} years old.")


# student.py
from person import Person

class Student(Person):
    def __init__(self, name, address, age, student_id):
        # ✅ Subclass initialization calls parent class initializer
        super().__init__(name, address, age)
        self.student_id = student_id

    # ✅ Method overriding (redefine greet from Person)
    def greet(self):
        print(f"Hi, I’m {self.name}, a student with ID {self.student_id}, "
              f"living at {self.address}, and I am {self.age} years old.")


# test.py
from student import Student

# Subclass object initialization
student1 = Student("Alice", "123 Main St", 20, "S12345")

# Method overriding demo
student1.greet