from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generator():
    haslo_input.delete(0, 'end')
    pass_letters = [choice(letters) for _ in range(randint(8, 10))]
    pass_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    pass_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = pass_letters + pass_symbols + pass_numbers
    shuffle(password_list)

    password = ''.join(password_list)
    haslo_input.insert(0, password)
    pyperclip.copy(password)


def search():
    strona_data = strona_input.get().title()
    if len(strona_data) == 0:
        messagebox.showerror(title='Błąd', message='Nie będę szukać niczego, wpisz nazwę strony.')
    else:
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
                dane = data[strona_data]

        except json.decoder.JSONDecodeError:
            messagebox.showerror(title='Błąd', message='Plik z hasłami jest pusty!')
        except FileNotFoundError:
            messagebox.showerror(title='Błąd', message='Plik z hasłami nie istnieje!')
        except KeyError:
            messagebox.showerror(title='Błąd', message=f'Nie znam hasła do {strona_data}.')
        else:
            messagebox.showinfo(title=strona_data, message=f"Login: {dane['login']}\nHasło: {dane['haslo']}\n"
                                                           f"Hasło wrzuciłem Ci do schowka")
            pyperclip.copy(dane['haslo'])
        finally:
            strona_input.delete(0, 'end')
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    strona_data = strona_input.get().title()
    login_data = login_input.get()
    haslo_data = haslo_input.get()
    new_data = {
        strona_data: {
            'login':login_data,
            'haslo':haslo_data
        }
    }
    if len(strona_data) == 0 or len(login_data) == 0 or len(haslo_data) == 0:
        messagebox.showinfo(title='ej ej kolego', message='nie zostawiaj pustych pól!')
    else:
        is_ok = messagebox.askokcancel(title=strona_data, message=f'Twoje dane logowania:\nLogin: {login_data}\n'
                                                                 f'Hasło: {haslo_data}\nCzy chcesz zapisać?')
        if is_ok:
            try:
                with open('data.json', 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open('data.json', 'w') as file:
                    json.dump(new_data, file, indent=4)
            except json.decoder.JSONDecodeError:
                with open('data.json', 'w') as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
            finally:
                strona_input.delete(0, 'end')
                haslo_input.delete(0, 'end')

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Menedżer haseł")
window.config(padx=40, pady=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

strona = Label(text='Strona:')
strona.grid(row=1, column=0)
strona_input = Entry(width=33)
strona_input.focus()
strona_input.grid(row=1, column=1, sticky='w')

login = Label(text="Login:")
login.grid(row=2, column=0)
login_input = Entry(width=43)
login_input.insert(0, 'your@email.com')
login_input.grid(row=2, column=1, columnspan=2, sticky='w')

haslo = Label(text='Hasło:')
haslo.grid(row=3,column=0)
haslo_input = Entry(width=33)
haslo_input.grid(row=3, column=1, sticky='w')

gen_pass = Button(text='Wymyśl', command=generator)
gen_pass.grid(row=3, column=2, sticky='e')

dodaj = Button(text='Dodaj', width=36, command=save)
dodaj.grid(row=4, column=1, columnspan=2, sticky='w')

szukaj = Button(text='Szukaj',width=6, command=search)
szukaj.grid(row=1, column=2)

window.mainloop()
