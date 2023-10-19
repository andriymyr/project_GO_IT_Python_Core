from collections import UserDict
from datetime import datetime, timedelta
from pathlib import Path
import clean_folder
import inspect
import pickle
import sys
import func
import re
import difflib
from notepad import Note, Note_book
from contact import Field, Name, Address, Email, Birthday, Phone, Record, AddressBook


address_book = AddressBook()
note_book = Note_book()




OPERATIONS = {
    'hello': func.hello,
    'add': func.add_contact,
    'change_phone': func.change_phone,
    'change_email': func.change_email,
    'find_contact': func.find_contact,
    'find_all': func.find_all,
    'show all': func.show_all,
    'when_birthday': func.when_birthday,
    'contacts_birthday': func.contacts_birthday,
    'clean_folder': func.cleans_folder,
    'good bye': func.good_bye,
    'exit': func.good_bye,
    'close': func.good_bye,
    'add_note': func.add_note,
    'find_note': func.find_note,
    'sort_notes': func.sort_notes,
    'show_notes': func.show_notes
    }


list_command = list()
for command in OPERATIONS:
    list_command.append(command)


def suggest_command(user_input):
    best_match = difflib.get_close_matches(user_input, list_command, n=1, cutoff=0.75)

    if best_match:
        return f"Можливо ви мали на увазі команду '{best_match[0]}'?"
    else:
        return "Не знайдено відповідної команди."


def get_command(operator):
    #command_function, address_book = OPERATIONS.get(operator, (None, None))
    #return command_function, address_book
    return OPERATIONS.get(operator, (None, None))
    #return OPERATIONS.get(operator, None), address_book, note_book




def main():
    global address_book
    global note_book

    try:
        with open("adressbook.bin", "rb") as fh:
            address_book.data = pickle.load(fh)
    except EOFError:
        pass
    except FileNotFoundError:
        pass
    try:
        with open("notebook.bin", "rb") as fh:
            note_book.data = pickle.load(fh)
    except EOFError:
        pass
    except FileNotFoundError:
        pass
    
    while True:
        command = func.input_data(f"Чекаю команду\n{list_command}\n").lower()
        if command not in list_command:
            suggestion = suggest_command(command)
            print(suggestion)
            continue

        #commands = get_command(command)
        command_function = get_command(command)
        #if commands is not None:
        if command_function is not None:
            #result = commands(address_book, note_book)
            result = command_function(address_book, note_book)
            if result == "Good bye!":
                print("Good bye!")
                break
        else:
            print(f"Команда '{command}' не знайдена.")



if __name__ == "__main__":

    classes_used = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            classes_used.append(obj)

    main()




