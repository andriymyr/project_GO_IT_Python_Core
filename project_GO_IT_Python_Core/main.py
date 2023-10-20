import inspect
import pickle
import sys
from pathlib import Path
from . import func
import difflib
from .notepad import Note_book
from .contact import AddressBook


address_book = AddressBook()
note_book = Note_book()


OPERATIONS = {
    "help": func.help,
    "hello": func.hello,
    "add": func.add_contact,
    "add phone": func.add_phone,
    "change phone": func.change_phone,
    "change email": func.change_email,
    "find contact": func.find_contact,
    "find all": func.find_all,
    "show all": func.show_all,
    "when birthday": func.when_birthday,
    "contacts birthday": func.contacts_birthday,
    "clean folder": func.cleans_folder,
    "good bye": func.good_bye,
    "exit": func.good_bye,
    "close": func.good_bye,
    "add note": func.add_note,
    "find note": func.find_note,
    "sort notes": func.sort_notes,
    "show notes": func.show_notes,
    "save": func.exit_boot,
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
    return OPERATIONS.get(operator, (None, None, None, None, None))


def main():
    global address_book
    global note_book
    global list_command
    global path_adress_book
    global path_note_book

    path_adress_book = Path.home() / "Contacts" / "adressbook.bin"
    path_note_book = Path.home() / "Contacts" / "notebook.bin"

    try:
        with open(path_adress_book, "rb") as fh:
            address_book.data = pickle.load(fh)
    except EOFError:
        pass
    except FileNotFoundError:
        pass
    try:
        with open(path_note_book, "rb") as fh:
            note_book.data = pickle.load(fh)
    except EOFError:
        pass
    except FileNotFoundError:
        pass

    while True:
        command = func.input_data(f"Чекаю команду (перелік команд - Help)\n").lower()
        if command not in list_command:
            suggestion = suggest_command(command)
            print(suggestion)
            continue

        command_function = get_command(command)
        if command_function is not None:
            result = command_function(
                address_book, note_book, list_command, path_adress_book, path_note_book
            )
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
