import pickle
from .contact import Email, Birthday, Phone, Record
from .notepad import Note
from . import clean_folder


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as value_error:
            print(value_error)
            return "Помилка вводу данних : "
        return result

    return inner


@input_error
def input_data(necessary_data):
    data = input(f"{necessary_data} ")
    return data.strip()


def exit_boot(
    address_book,
    note_book,
    list_command,
    path_adress_book,
    path_note_book,
):
    with open(path_adress_book, "wb") as fh:
        pickle.dump(address_book, fh)
    with open(path_note_book, "wb") as fh:
        pickle.dump(note_book, fh)

    return "exit"


def help(ddress_book, note_book, list_command, *arg):
    print(f"Перелік наявних команд: \n{list_command}")


def hello(*arg):
    print("How can I help you?")


def add_contact(address_book, *arg):
    while True:
        name = input_data("Введіть ім'я контакту: ")
        contact = address_book.find(name)
        if contact:
            print("Такий контакт вже існує")
        elif name == "":
            return
        elif contact == None:
            user = Record(name)
            break
    while True:
        phone = input_data("Введіть номер телефону (xxxxxxxxxx): ")
        if phone == "":
            return
        phone_value = Phone(phone)
        if phone_value.value == "":
            print("Не вірно вказано номер телефлефону, повторіть ввід або вийти Enter")
        else:
            user.add_phone(phone)
            break
    while True:
        birthday = input_data("Введіть дату дня народження (dd/mm/yyyy): ")
        if birthday == "":
            break
        birthday_value = Birthday(birthday)
        if birthday_value.value == "":
            print(
                "Не вірно вказано дату дня народження, повторіть ввід або вийти Enter"
            )
        else:
            user.add_birthday(birthday)
            break
    while True:
        email = input_data("Введіть e-mail: ")
        if email == "":
            break
        email_value = Email(email)
        if email_value.value == None:
            print("Не вірно вказано e-mail, повторіть ввід або вийти Enter")
        else:
            user.add_email(email)
            break
    address = input_data("Введіть адресу: ")
    user.add_address(address)
    address_book.add_record(user)
    print(f"Додано контакт : {user}")


def change_phone(address_book, *arg):
    name = input_data("Введіть ім'я (Вийти 'Enter') \n")
    contact = address_book.find(name)
    if name == "":
        return None
    elif contact is None:
        print("Немає такого контакту")
        return None
    print(contact)
    phone = input_data(
        "Введіть номер телефону який необхідно замінити (xxxxxxxxxx) (Вийти 'Enter') \n"
    )
    if phone == "":
        return None
    elif Phone(phone).value:
        phone_new = input_data(
            "Введіть новий номер телефону (xxxxxxxxxx) (Вийти 'Enter') \n"
        )
        if phone_new == "":
            return None
        elif Phone(phone_new).value:
            contact = address_book.get(name)
            contact.remove_phone(phone)
            contact.add_phone(phone_new)
            address_book.data[name] = contact
            print(f"Змінено контакт: {contact}, новий номер телефону: {phone_new}")


def add_phone(address_book, *arg):
    name = input_data("Введіть ім'я (Вийти 'Enter') \n")
    contact = address_book.find(name)
    if name == "":
        return None
    elif contact is None:
        print("Немає такого контакту")
        return None
    print(contact)
    phone = input_data(
        "Введіть номер телефону який необхідно внести (xxxxxxxxxx) (Вийти 'Enter') \n"
    )
    if phone == "":
        return None
    elif Phone(phone).value:
        contact.add_phone(phone)
        address_book.data[name] = contact
        print(f"Змінено контакт: {contact}, внесено номер телефону: {phone}")


def change_email(address_book, *arg):
    name = input_data("Введіть ім'я (Вийти 'Enter') \n")
    contact = address_book.find(name)
    if name == "":
        return None
    elif contact is None:
        print("Немає такого контакту")
        return None
    print(contact)
    email = input_data("Введіть e-mail який необхідно замінити (Вийти 'Enter') \n")
    if email == "":
        return None
    elif Email(email).value:
        email_new = input_data("Введіть новий e-mail (Вийти 'Enter')\n")
        if email_new == "":
            return None
        elif Email(email_new).value:
            contact = address_book.get(name)
            contact.add_email(email_new)
            address_book.data[name] = contact
            print(f"Змінено контакт: {contact}, новий e-mail: {email_new}")


def find_contact(address_book, *arg):
    result = input_data("Введіть назву контакту або його частину: ")
    list_contact = address_book.find_contact(result)
    if list_contact == []:
        print("Такого контакту немає")
        return None
    for contact in list_contact:
        print(contact)


def find_all(address_book, *arg):
    result = input_data("Введіть значення пошуку: ")
    list_contact = address_book.find_all(result)
    if list_contact == []:
        print("За даними умовами пошуку нічого не знайдено")
        return None
    for contact in list_contact:
        print(contact)


def show_all(address_book, *arg):
    print("Вивід всіх збеорежених контактів \n")
    for value in address_book.values():
        print(value)


def when_birthday(address_book, *arg):
    result = input_data("Вкажіть ім'я контакту/(Вийти 'Enter')\n")
    if result == "":
        return
    else:
        if result in address_book and address_book[result].days_to_birthday():
            if address_book[result].days_to_birthday():
                print(address_book[result].days_to_birthday())
        else:
            print(f"не має запису в адресній книзі для: {result}")


@input_error
def contacts_birthday(address_book, *arg):
    result = input_data("Вкажіть кількість днів/(Вийти 'Enter')\n")
    if result == "":
        return
    try:
        days = int(result)
    except:
        raise ValueError("Введіть дні числом")
    if address_book.contact_for_birthday(int(result)):
        print(address_book.contact_for_birthday(int(result)))
    else:
        print(f"Через {days} днів ні в кого немає день народження")


def cleans_folder(*arg):
    result = input_data("Вкажіть шлях до папки/(Вийти 'Enter')\n")
    if result == "":
        return
    else:
        try:
            clean_folder.main(result)
        except FileNotFoundError:
            print(f"Невірний шлях до папки")


def good_bye(
    address_book, note_book, list_command, path_adress_book, path_note_book, *arg
):
    exit_boot(
        address_book.data,
        note_book.data,
        list_command,
        path_adress_book,
        path_note_book,
    )
    return "Good bye!"


def add_note(note_book, *arg):
    while True:
        result = input_data("Напишіть ключове слово(#..)/їх може бути декілька/\n")
        if result == "" or result[0] != "#":
            print("Некоректно введено тег")
        else:
            break
    text = []
    print("Напишіть саму нотатку")
    while True:
        result2 = input()
        if result2 == "":
            break
        text.append(result2)
    if text:
        text = "\n".join(text)
        note = Note(text, result)
        note_book.add_note(note)


def find_note(note_book, *arg):
    result = input_data("Напишіть ключове слово(#..)/їх може бути декілька/Вийти no\n")
    if result == "":
        return
    matches = note_book.find_notes(result)
    if matches:
        for i in matches:
            print(i)
    else:
        print("Немає нотатків по такому тегу")
        command = "find_note"


def sort_notes(note_book, *arg):
    note_book.sort_notes()


def show_notes(note_book, *arg):
    if note_book.data:
        for tags in note_book.data:
            print("#" + tags)
            for note in note_book.data[tags]:
                print(f"{note.text}")
