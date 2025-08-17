import random
random_letter = (random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(1, 5))
letter_display = "_" * len(random_letter)
lives = 5
while True:
    gusee = input("Guess a letter: ").lower()
    if gusee in random_letter:
        for i in range(len(random_letter)):
            if random_letter[i] == gusee:
                letter_display = letter_display[:i] + gusee + letter_display[i+1:]
        print("Correct! Current word: " + letter_display)
    else:
        lives -= 1
        print(f"Wrong! You lose a life. Lives left: {lives}")
    if "_" not in letter_display:
        print("Congratulations! You guessed the word!")
        break
    if lives == 0:
        print("Game Over!")
        break
    print("Current word: " + letter_display)


