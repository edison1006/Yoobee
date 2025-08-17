class StringManipulator:
    def __init__(self,text):
        self.text = text
    
    def find_character(self,char):
        return self.text.find(char)
    
    def get_length(self):
        return len(self.text)

    def toupper(self):
        return self.text.upper()

def main():
    name = StringManipulator("example")
    result = name.find_character("x")
    print(result)
    length = name.get_length()
    print("Length is:",length)
    upper_text = name.toupper()
    print("Upper text:",upper_text)

    if __name__=="__main__":
        main()
