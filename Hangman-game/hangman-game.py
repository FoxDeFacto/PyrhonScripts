import random

# Slovníky slov pro každý jazyk
czech_words = ["python", "programování", "počítač", "algoritmus", "databáze"]
english_words = ["python", "programming", "computer", "algorithm", "database"]
ukrainian_words = ["пітон", "програмування", "комп'ютер", "алгоритм", "база даних"]

def choose_language():
    while True:
        choice = input("Vyberte jazyk / Choose language / Виберіть мову (cz/en/ua): ").lower()
        if choice in ['cz', 'en', 'ua']:
            return choice
        print("Neplatná volba. Zkuste to znovu. / Invalid choice. Try again. / Неправильний вибір. Спробуйте ще раз.")

def get_word(language):
    if language == 'cz':
        return random.choice(czech_words)
    elif language == 'en':
        return random.choice(english_words)
    else:
        return random.choice(ukrainian_words)

def play_hangman(word):
    word = word.lower()
    word_letters = set(word)
    alphabet = set('abcdefghijklmnopqrstuvwxyzáčďéěíňóřšťúůýž')
    used_letters = set()

    lives = 6

    while len(word_letters) > 0 and lives > 0:
        print("Máte", lives, "životů a použili jste tyto písmena: ", ' '.join(used_letters))
        word_list = [letter if letter in used_letters else "_" for letter in word]
        print("Aktuální slovo: ", ' '.join(word_list))

        user_letter = input("Hádejte písmeno: ").lower()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives = lives - 1
                print("Písmeno není ve slově.")
        elif user_letter in used_letters:
            print("Už jste použili toto písmeno. Zkuste to znovu.")
        else:
            print("Neplatný znak. Prosím, zadejte písmeno.")

    if lives == 0:
        print("Promiňte, zemřeli jste. Slovo bylo", word)
    else:
        print("Jupí! Uhádli jste slovo", word, "!!")

def main():
    language = choose_language()
    word = get_word(language)
    play_hangman(word)
    print("Děkujeme za hru!")

if __name__ == "__main__":
    main()