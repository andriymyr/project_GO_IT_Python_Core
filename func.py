from datetime import datetime, timedelta
import pickle
import re


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return "Помилка вводу данних : "
        return result

    return inner


@input_error
def input_data(necessary_data):
    data = input(f"{necessary_data} ")
    return data


@input_error
def exit_boot(address_book, note_book):
    #print("Good bye!")
    with open("adressbook.bin", "wb") as fh:
        pickle.dump(address_book, fh)
    with open("notebook.bin", "wb") as fh:
        pickle.dump(note_book, fh)

    return "exit"
