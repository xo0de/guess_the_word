import requests

# Datamuse API endpoint for searching random words
endpoint = "https://random-word-api.herokuapp.com/word"

params = {
    "number": 1,    # Set number of requested words. If it exceeds the maximum stored amount, it will just return all of them.
    "lang": 'en',   # Set language of requested words. Go to Github to get more info on how to add your own language.
}

response = requests.get(endpoint, params=params)

if response.status_code == 200:
    data = response.json()
    if data:
        random_word = data[0]
        print(random_word)
    else:
        print("Word not found.")
else:
    print("Error executing request:", response.status_code)


# Function to get a random word from a list
def get_word():
    return random_word.upper()


# Function to get the player's state
def display_hangman(tries):
    stages = [  # final state: head, torso, both arms, both legs
        '''
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / \\
           -
        ''',
        # head, torso, both arms, one leg
        '''
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     /
           -
        ''',
        # head, torso, both arms
        '''
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |
           -
        ''',
        # head, torso and one arm
        '''
           --------
           |      |
           |      O
           |     \\|
           |      |
           |
           -
        ''',
        # head and torso
        '''
           --------
           |      |
           |      O
           |      |
           |      |
           |
           -
        ''',
        # head
        '''
           --------
           |      |
           |      O
           |
           |
           |
           -
        ''',
        # initial state
        '''
           --------
           |      |
           |
           |
           |
           |
           -
        '''
    ]
    return stages[tries]


def display_info(word, tries):
    print(f"Your man looks like this:\n{display_hangman(tries)}")
    print(f"You have {tries} attempts left. The word looks like this: {''.join(word)}")


# Main game logic
def play(word):
    word_completion = ["_"] * len(word)
    guessed_letters = []
    guessed_words = []
    tries = 6

    print("Hey, let's play a guessing game!")
    display_info(word_completion, tries)

    while True:
        if tries <= 0:
            print(f"\nI'm sorry, but you lost!\n{display_hangman(tries)}")
            print(f"The word was: {word}")
            break
        if "_" not in word_completion:
            print(f"Congratulations! You guessed the word in {6 - tries} tries!")
            display_info(word_completion, tries)
            break
        s = input("Enter a word or letter: ").upper()

        flag = False
        for i in s:
            flag = False
            if i not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and i in "1234567890 !#$%&*+-=?@^_,.'\"":
                print("\nInvalid input! Try again!")
                flag = True
                break
        if flag:
            continue

        if s in guessed_letters or s in guessed_words:
            print(f"\nYou have already entered '{s}'!")
            continue
        elif len(s) > 1:
            if s == word:
                print(f"Congratulations! You guessed the word in {6 - tries} tries!")
                display_info(word_completion, tries)
                break
            else:
                tries -= 1
                guessed_words.append(s)
                print("\nI'm sorry, but you guessed wrong!")
                display_info(word_completion, tries)
        else:
            if s in word:
                guessed_letters.append(s)
                word_completion = [s if word[i] == s else word_completion[i] for i in range(len(word))]
                print(f"\nCongratulations, you guessed the letter '{s}'")
                display_info(word_completion, tries)

            else:
                tries -= 1
                guessed_letters.append(s)
                print("\nI'm sorry, but you guessed wrong!")
                display_info(word_completion, tries)

    return word


def main():
    while True:
        used_words = []
        word = get_word()

        while word in used_words:
            word = get_word()

        used_words.append(play(word))
        if input("\nDo you want to play again? (yes/no): ").lower() != "yes":
            print("Goodbye! Come play some more!")
            break


if __name__ == '__main__':
    main()
