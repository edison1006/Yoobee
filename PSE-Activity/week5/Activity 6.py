class Student:
    def __init__(self, name, age):
        self.name = name        # Public attribute
        self._age = age         # Protected attribute
        self.__grade = 'A'      # Private attribute

    def get_grade(self):
        return self.__grade

    def has_passed(self):
        return self.__grade in ['A', 'B', 'C']

class Teacher:
    def __init__(self, name, subject):
        self.name = name          # Public attribute
        self._subject = subject   # Protected attribute

    def show_info(self):
        return f"Teacher: {self.name}, Subject: {self._subject}"


if __name__ == "__main__":
    s = Student("Ali", 20)
    print(s.name)          
    print(s._age)          
    print(s.get_grade())   
    print(s.has_passed())  

    t = Teacher("Mr. Smith", "Math")
    print(t.show_info())   

