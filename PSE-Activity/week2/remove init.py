class StringManipulator:
    """The __init__ method is a constructor that runs automatically
    when an object is created. It allows us to set initial values
    for the object's attributes, making the object ready to use
    without extra setup steps after creation."""
    
    def find_character(self, char):
        return self.text.find(char)
    
    def get_length(self):
        return len(self.text)

    def toupper(self):
        return self.text.upper()

def main():
    # Without __init__, we need to set attributes manually
    name = StringManipulator()
    name.text = "example"

    result = name.find_character("x")
    print(result)

    length = name.get_length()
    print("Length is:", length)

    upper_text = name.toupper()
    print("Upper text:", upper_text)

if __name__ == "__main__":
    main()
