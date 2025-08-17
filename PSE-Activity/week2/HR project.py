employee_info = [
    {"name": "John", "salary": 50000, "position": "Software Engineer"},
    {"name": "Tom",  "salary": 60000, "position": "Data Scientist"},
    {"name": "Bob",  "salary": 55000, "position": "Product Manager"},
]

class Employee:
    def __init__(self, name, salary, position):
        self.name = name
        self.salary = salary
        self.position = position

    def display_info(self):
        print(f"Name: {self.name}\nSalary: {self.salary}\nPosition: {self.position}")

    def give_raise(self, amount):
        self.salary += amount
        print(f"{self.name} got a raise of {amount}. New salary: {self.salary}")

class HRproject:
    def __init__(self):
        self.employees = {} 

    def _key(self, name):
        return name

    def load_from_global(self):
        self.employees
        for i in employee_info:
            key = self._key(i["name"])
            self.employees[key] = Employee(i["name"], i["salary"], i["position"])

    def list_all(self):
        if not self.employees:
            print("No employees.")
            return
        print(f"Total: {len(self.employees)}")
        for emp in self.employees.values():
            emp.display_info()

    def give_raise(self, name, amount):
        key = self._key(name)
        emp = self.employees.get(key)
        if not emp:
            print("Not found.")
            return
        emp.give_raise(amount)
        for emp_dict in employee_info:
            if self._key(emp_dict["name"]) == key:
                emp_dict["salary"] = emp.salary
                break

if __name__ == "__main__":
    hr = HRproject()
    hr.load_from_global()

    while True:
        print("*" * 30)
        print("HR Project Menu:")
        print("1. List All Employees")
        print("2. Give Raise")
        print("0. Exit")
        print("*" * 30)
        choice = input("Choose: ")

        if choice == "1":
            hr.list_all()
        elif choice == "2":
            name = input("Name: ")
            amount = float(input("Raise amount: "))
            hr.give_raise(name, amount)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
