class Clothing():
    def __init__(self, name, clothing_type, desc="", colour="#ffffff"):
        self.name = name
        self.desc = desc
        self.clothing_type = clothing_type.lower()
        self.colour = colour
        

    def info(self):
        print(f"[{self.name}]")
        print(f"{self.desc}")


class Top(Clothing):
    def __init__(self, name, desc="", colour="#ffffff", sleeves=True):
        super().__init__(name, "top", desc, colour)
        self.sleeves = sleeves
        


def main():
    # outfit combinations
    outfits = []

    # clean and dirty clothing
    # 
    clean = []
    dirty = []

    shirt = Top("shirt", "balls")
    shirt.info()

if __name__ == "__main__":
    main()