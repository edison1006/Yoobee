class wordsnumber:
    def __init__(self, sentence):
        self.sentence = sentence

    def len_words(self):
        words = self.sentence.strip().split()
        return len(words)

def main():
    sentence = input("Enter a sentence: ")
    len = wordsnumber(sentence)
    num = len.len_words()
    print(f"The sentence contains {num} words.")

if __name__ == "__main__":
    main()