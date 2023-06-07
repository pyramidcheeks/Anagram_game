import tkinter as tk
import random
import json
import time

root = tk.Tk()


# Personalização do Jogo:
# Cores
background_colour = "6CA0DC"
background_colour_correct = "32CD32"
background_colour_incorrect = "ED2939"

# Número de tentativas
tries = 3
score = 0


# Importar Dicionário JSON 
def import_json(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data

json_file = 'dictionary.json'
words = import_json(json_file)

# Shuffle
chosen_word = random.choice(list(words.keys()))
shuffled_word = "".join(random.sample(chosen_word, len(chosen_word)))


num_tries = tries #usamos esta operação para ter o valor definido para quando o jogo for reiniciado


# Função para encontrar a definição de uma a palavra
def get_word_meaning(word):
    if word in words:
        return words[word]
    else:
        return "Meaning not found."
    
# Função para iniciar o jogo
def start_game():
    global root, entry, start_time
    root = tk.Tk()
    root.title("Guess the Word")
    root.configure(bg=f"#{background_colour}")
    root.bind('<Control-d>', close_window)
    print(chosen_word)
    label = tk.Label(root, text=f"Guess the word: {shuffled_word}", bg=f"#{background_colour}", fg="white", font=("Arial", 20))
    label.pack(padx=20, pady=20)
    hint_label = tk.Label(root, text=f"Hint: The word means '{get_word_meaning(chosen_word)}'", bg=f"#{background_colour}", fg="white", font=("Arial", 12))
    hint_label.pack(padx=20, pady=5)
    entry = tk.Entry(root, font=("Arial", 16))
    entry.pack(padx=20, pady=20)
    entry.bind('<Return>', check_guess)
    submit_button = tk.Button(root, text="Submit", command=check_guess, font=("Arial", 16))
    submit_button.pack(padx=20, pady=20)
    rules_button = tk.Button(root, text="Rules", command=lambda: show_rules2(), font=("Arial", 16))
    rules_button.pack(padx=20, pady=20)
    quit_button = tk.Button(root, text="Quit", command=root.destroy, font=("Arial", 12))
    quit_button.pack(padx=20, pady=10)
    start_time = time.time()  #  Guardar o tempo
    
# Função base para apresentar uma mensagem
def show_message(message, ok_button_enabled):
    window = tk.Toplevel()
    window.title("Guess the Word")
    window.configure(bg=f"#{background_colour_incorrect}")
    label = tk.Label(window, text=message, bg=f"#{background_colour_incorrect}", fg="white", font=("Arial", 16))
    label.pack(padx=20, pady=20)
    if ok_button_enabled:
        ok_button = tk.Button(window, text="OK", command=window.destroy, font=("Arial", 12))
        ok_button.pack(padx=1, pady=10)
    else:
        quit_button = tk.Button(window, text="Quit", command=window.destroy, font=("Arial", 12))
        quit_button.pack(padx=20, pady=10)

# Função para definir se a resposta está correta
def check_guess(event=None):
    global num_tries, score
    guess = entry.get().lower()
    if guess == chosen_word:
        meaning = get_word_meaning(chosen_word)
        score += 1
        elapsed_time = round(time.time() - start_time, 2)
        message = f"Congratulations, you guessed the word '{chosen_word}'!\n\nMeaning: {meaning}\n\nScore: {score}\n\nTime elapsed: {elapsed_time} seconds"
        show_message_correct(message)
    else:
        num_tries -= 1
        if num_tries == 0:
            meaning = get_word_meaning(chosen_word)
            elapsed_time = round(time.time() - start_time, 2)
            message = f"Sorry, you ran out of tries. The word was '{chosen_word}'.\n\nMeaning: {meaning}\n\nScore: {score}\n\nTime elapsed: {elapsed_time} seconds"
            show_message_incorrect(message)
        else:
            hint = get_word_meaning(chosen_word)
            message = f"Sorry, '{guess}' is not the word. You have {num_tries} tries left.\n\nHint: The word means '{hint}'\n\nScore: {score}"
            show_message(message, True)

# Função quando inserida palavra correta
def show_message_correct(message):
    window = tk.Toplevel()
    window.title("Guess the Word")
    window.configure(bg=f"#{background_colour_correct}")
    label = tk.Label(window, text=message, bg=f"#{background_colour_correct}", fg="white", font=("Arial", 12))
    label.pack(padx=20, pady=20)
    play_again_button = tk.Button(window, text="Play Again", command=lambda: [restart_game(), window.destroy()], font=("Arial", 12))
    play_again_button.pack(padx=20, pady=10)
    quit_button = tk.Button(window, text="Quit", command=lambda: [root.destroy(), window.destroy()], font=("Arial", 12))
    quit_button.pack(padx=20, pady=10)
  
# Função quando inserida palavra incorreta (com ou sem tries restantes)
def show_message_incorrect(message):
    global window  
    window = tk.Toplevel()
    window.title("Guess the Word - Incorrect")
    window.configure(bg=f"#{background_colour_incorrect}")
    label = tk.Label(window, text=message, bg=f"#{background_colour_incorrect}", fg="white", font=("Arial", 12))
    label.pack(padx=20, pady=20)
    if num_tries > 0:
        ok_button = tk.Button(window, text="Quit", command=lambda: [root.destroy(), window.destroy()], font=("Arial", 12))
        ok_button.pack(padx=20, pady=10)
    else:
        play_again_button = tk.Button(window, text="Play Again", command=restart_game, font=("Arial", 12))
        play_again_button.pack(padx=20, pady=10)
        quit_button = tk.Button(window, text="Quit", command=lambda: [root.destroy(), window.destroy()], font=("Arial", 12))
        quit_button.pack(padx=20, pady=10)



# Regras (antes do jogo)
def show_rules():
    rules_window = tk.Toplevel()
    rules_window.title("Guess the Word - Rules")
    rules_window.configure(bg=f"#{background_colour}")
    rules_text = f"""
    Rules:
    - You have {num_tries} tries to guess the word.
    - Enter your guess in the text box and press Enter or click Submit.
    - If you guess the word correctly, you win!
    - If you run out of tries, you lose.
    - You will earn 1 point for each correct guess.
    """
    rules_label = tk.Label(rules_window, text=rules_text, bg=f"#{background_colour}", fg="white", font=("Arial", 14))
    rules_label.pack(padx=20, pady=20)
    ready_button = tk.Button(rules_window, text="I'm Ready!", command=lambda: [rules_window.destroy(), start_game()], font=("Arial", 12))
    ready_button.pack(padx=20, pady=10)

# Regras_2 (depois de o jogo começar)
def show_rules2():
    rules_window2 = tk.Toplevel()
    rules_window2.title("Guess the Word - Rules")
    rules_window2.configure(bg=f"#{background_colour}")
    rules_text = f"""
    Rules:
    - You have {num_tries} tries to guess the word.
    - Enter your guess in the text box and press Enter or click Submit.
    - If you guess the word correctly, you win!
    - The time you took to guess a word will be displayed once you do it
    - If you run out of tries, you lose.
    """
    rules_label = tk.Label(rules_window2, text=rules_text, bg=f"#{background_colour}", fg="white", font=("Arial", 14))
    rules_label.pack(padx=20, pady=20)
    return_button = tk.Button(rules_window2, text="Return to Game", command=rules_window2.destroy, font=("Arial", 12))
    return_button.pack(padx=20, pady=10)
    
# Função para reiniciar o jogo
def restart_game():
    global num_tries, chosen_word, shuffled_word, score, start_time
    num_tries = tries
    chosen_word = random.choice(list(words.keys()))
    shuffled_word = "".join(random.sample(chosen_word, len(chosen_word)))
    score = 0
    start_time = time.time()  # Reinicar o tempo
    root.destroy()
    if 'window' in globals():
        window.destroy()
    start_game()

# Função para terminar o programa com ctrl+d
def close_window(event):
    root.destroy()

# Esconde a janela principal até o utilizador premir "I'm Ready!"
root.withdraw()


# Inicio do jogo
show_rules()    

root.mainloop()