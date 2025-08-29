
# Define a base class 'person' with attributes name, address, age, and ID.
class person:
    def __init__(self,name, address, age, ID):
        self.name = name
        self.address = address
        self.age = age
        self.ID = ID  

    def display(self):
        print("Name:", self.name)
        print("Address:", self.address)
        print("Age:", self.age)
        print("ID:", self.ID)

# Define subclasses 'student', 'academic_staff', and 'general_staff' that inherit from 'person'.
class student(person):
    def __init__(self, name, address, age, ID, GPA):
        super().__init__(name, address, age, ID)
        self.GPA = GPA

    def display(self):
        super().display()
        print("GPA:", self.GPA) 

class academic_staff(person):
    def __init__(self, name, address, age, ID, tax_code, salary):
        super().__init__(name, address, age, ID)
        self.tax_code = tax_code
        self.salary = salary

    def display(self):
        super().display()
        print("Tax Code:", self.tax_code)
        print("Salary:", self.salary)

class general_staff(person):
    def __init__(self, name, address, age, ID, tax_code, payrate):
        super().__init__(name, address, age, ID)
        self.tax_code = tax_code
        self.payrate = payrate

    def display(self):
        super().display()
        print("Tax Code:", self.tax_code)
        print("Payrate:", self.payrate)

