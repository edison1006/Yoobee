class user_details:
    def __init__(self,name,age,address):
        self.name = name
        self.age = age
        self.address = address

    def personal_details(self):
        return f"Name:{self.name},Age:{self.age},Address{self.address}"

if __name__ == "__main__":
    name = input("Please enter your name:")
    age = input("Please enter your age:")
    address = input("Please enter your address:")
    personal_details = []
    personal_details.append(user_details(name, age, address))
    print("\nPersonal Details:")

    for person in personal_details:
        print(person)
    years_to_add = int(input("\nHow many years to add to the current age: "))
    personal_details[0].age += years_to_add
    print(f"\nIn {years_to_add} years, {personal_details[0].user_name} will be {personal_details[0].age} years old and still living at {personal_details[0].address}.")
    print("How many years to add to their current age:")

