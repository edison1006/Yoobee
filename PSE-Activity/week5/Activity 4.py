class Color:
    def __init__(self, name):
        self.name = name
    
    def show_info(self):
        return f"Color: {self.name}"


class TransparentColor(Color):
    def __init__(self, name, transparency_level):
        super().__init__(name)   
        self.transparency_level = transparency_level 

    def show_info(self):
        return f"Color: {self.name}, Transparency: {self.transparency_level}%"


class Animal:
    def __init__(self, species, color: Color):
        self.species = species
        self.color = color
    
    def show_info(self):
        return f"Animal: {self.species}, {self.color.show_info()}"


if __name__ == "__main__":

    panda_color = Color("Black & White")
    panda = Animal("Panda", panda_color)
    print(panda.show_info())

    butterfly_color = TransparentColor("Orange", 30)
    butterfly = Animal("Butterfly", butterfly_color)
    print(butterfly.show_info())
