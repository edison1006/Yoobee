import random, string

class letter_game:
    def __init__(self, word, lives=5):
        self.word = word.lower()
        self.lives = lives
        self.guessed = set()
        self.revealed = ["_" if ch in string.ascii_lowercase else ch for ch in self.word]

    def guess(self, ch):
        ch = ch.lower()
        if len(ch) != 1 or ch not in string.ascii_lowercase or ch in self.guessed:
            return False
        self.guessed.add(ch)
        if ch in self.word:
            for i, w in enumerate(self.word):
                if w == ch:
                    self.revealed[i] = ch
            return True
        else:
            self.lives -= 1
            return False

    def win(self):
        return "_" not in self.revealed

    def lost(self):
        return self.lives <= 0

    def state(self):
        return f"{' '.join(self.revealed)} | lives: {self.lives} | guessed: {','.join(sorted(self.guessed))}"

def random_word():
    return random.choice(["python", "java", "class", "package", "computer",])

def play():
    game = letter_game(random_word())
    print("Welcome to letter game!")
    print(game.state())
    while not (game.win() or game.lost()):
        raw = input("Guess a letter: ").strip()
        if raw.lower() == "quit": return
        if game.guess(raw):
            print("Correct!")
        else:
            print("Wrong!")
        print(game.state())
    print(f"You {'win' if game.win() else 'lost'}! Word was: {game.word}")

if __name__ == "__main__":
    play()
