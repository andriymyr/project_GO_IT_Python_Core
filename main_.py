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



class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Address(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f"Address: {self.value}"


class Email(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = self.is_data(value)

    def is_data(self, email):
        try:
            email = re.findall(r"[a-zA-Z][a-zA-Z._0-9]+@\w+\.+\w\w+", email)
            if email == []:
                raise ValueError ("Введено неправильний e-mail")
        except:
            return None
        return email

    def __str__(self):
        return f"Email: {self.value}"


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = self.is_data(value)

    def is_data(self, value):
        if value == "":
            return value
        value = value.replace(".", "/")
        day_pattern = r"\d{2}/\d{2}/\d{4}"
        try:
            if not re.match(day_pattern, value):
                raise ValueError("неправильний формат дати")
            datetime.strptime(value, "%d/%m/%Y")
            return value
        except ValueError:
            print("неправильно вказано дату")
            return ""

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = self.is_data(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            self.value = self.is_phone(value)
        except ValueError:
            print("неправильний номер телефону _")
            self.value = ""
    
    def __str__(self):
        return f"Phone: {self.value}"
    
    def is_phone(self, value):
        phone_pattern_1 = r"^[0-9]{10}$"
        phone_pattern_2 = r"^[0-9]{12}$"
        if (re.match(phone_pattern_1, value) == re.match(phone_pattern_2, value)):
            return ""
        return value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = self.is_phone(value)


class Record:
    def __init__(self, name, birthday = ""):   
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)
        self.address = None  
        self.email = None 

    def __str__(self):
        if self.birthday.value:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, Birthday: {self.birthday.value}, address: {self.address.value}, e-mail: {self.email.value}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone):
        for i in self.phones:
            if str(i) == phone:
                return False
        result = Phone(phone)
        if result.value:
            self.phones.append(result)
        #    print(f"телефон {phone} не додано: неправильний номер телефону")

    def add_address(self, address):
        self.address = Address(address)

    def add_email(self, email):
        self.email = Email(email)

    def add_birthday(self, birthday):
        self.email = Birthday(birthday)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p.value) != phone]

    def edit_phone(self, phone_old, phone_new):
        print(self.find_phone(phone_old),"::::", phone_old)
        print()
        if self.find_phone(phone_old):
            self.remove_phone(phone_old)
            self.add_phone(phone_new)
        else:
            raise ValueError
            # (f"Такого номера не існує: {phone}")
        return

    def find_phone(self, phone):
        for i in self.phones:
            if str(i) == phone:
                return Phone(phone)
        return None

    def days_to_birthday(self):
        if not self.birthday:
            return 0
        current_data = datetime.now().date()
        birthday_date = datetime.strptime(str(self.birthday.value), "%d/%m/%Y").date()
        birthday_date_new = birthday_date.replace(year=current_data.year)
        if birthday_date_new >= current_data:
            return (birthday_date_new - current_data).days
        else:
            return (birthday_date.replace(year=(current_data.year + 1)) - current_data).days


class AddressBook(UserDict):

    def __init__(self):
        super().__init__()

    def add_record(self, value):
        self.data[value.name.value] = value

    def find(self, value):
        return self.data.get(value)

    def delete(self, value):
        for key, i in self.data.items():
            if value in str(i):
                return self.data.pop(key, "і не було")

    def show_book(self, count=0, list=False):
        # вивід адресної книги
        # count = 0 - вся книга, або вказана кількість строк
        # list = False - тільки вказана кількості строк, True - вся книга, але з розбиттям по вказаній кількості строк
        count = count if count >= 0 else 0
        stop_check = count
        msg = None
        list = list if list == False else True
        records_iterator = iter(self.data.values())
        for i in range(len(self.data)):
            contact = next(records_iterator, None)
            if contact is None:
                break
            print(contact)
            stop_check -= 1
            if list:
                if not stop_check:
                    msg = input("Для продовження 'Enter', Вихід - любий символ ")
                    stop_check = count
                if msg:
                    return
            else:
                if not stop_check:
                    return

    def contact_for_birthday(self, days):
        now=datetime.now().date()
        result=''
        
        days_interval=timedelta(days=days)
        for key, value in self.data.items():
            if value.birthday.value:
                date = datetime(year=now.year, month=now.month, day=now.day)+days_interval
                birthday_date = datetime.strptime(str(value.birthday.value), "%d/%m/%Y").date()
                birthday_date_new = birthday_date.replace(year=date.year)
                if date.date()==birthday_date_new:
                    result+=f'Contact name: {key} phones:'+str(*value.phones)+'\n'
        return result

    def __str__(self):
        print(f"\nAddressBook list name: ")
        for i in self.data.values():
            print(i)
        return "AddressBook"

    #def __iter__(self):
    #    self.records_iterator = iter(self.data.values())
    #    return self

    #def __next__(self):
    #    data = next(self.records_iterator, "")
    #    if not data:
    #        raise StopIteration
    #    return data

address_book = AddressBook()
note_book = Note_book()


def hello(*arg):
    print("How can I help you?")


def add_contact(*arg):
    name = func.input_data("Введіть ім'я контакту: ")
    if name == "":
        return
    user = Record(name)
    added = False
    while True:
        phone = func.input_data("Введіть номер телефону (xxxxxxxxxx): ")
        if phone == "" :
            break
        phone_value = Phone(phone)
        if phone_value.value =="": 
            print ("Не вірно вказано номер телефлефону, повторіть ввід або вийти Enter")
        else:
            user.add_phone(phone_value.value)
            added = True
            break
    while True:
        birthday = func.input_data("Введіть дату дня народження (dd/mm/yyyy): ")
        if birthday == "" :
            break
        birthday_value = Birthday(birthday)
        if birthday_value.value == "": 
            print ("Не вірно вказано дату дня народження, повторіть ввід або вийти Enter")
        else:
            user.add_birthday(birthday_value.value)
            added = True
            break
    while True:
        email = func.input_data("Введіть e-mail: ")
        if email == "" :
            break
        email_value = Email(email)
        if email_value.value == None: 
            print ("Не вірно вказано e-mail, повторіть ввід або вийти Enter")
        else:
            user.add_email(birthday_value.value)
            added = True
            break
    if added:
        address = func.input_data("Введіть адресу: ")
        user.add_address(address)
        address_book.add_record(user)
        print(f"Додано контакт : {user}")

"""
def add_contact(*arg):
    name = func.input_data("Введіть ім'я контакту: ")
    if name == "":
        return
    added = False
    user = Record(name)  # Create a new Record object
    while True:
        phone = func.input_data("Введіть номер телефону (xxxxxxxxxx): ")
        if phone == "":
            break
        phone_value = Phone(phone)
        if phone_value.value == "":
            print("Не вірно вказано номер телефону, повторіть ввід або вийдіть (Enter)")
        else:
            user.add_phone(phone_value.value)
            added = True

    while True:
        birthday = func.input_data("Введіть дату дня народження (dd/mm/yyyy): ")
        if birthday == "":
            break
        birthday_value = Birthday(birthday)
        if birthday_value.value == "":
            print("Не вірно вказано дату дня народження, повторіть ввід або вийдіть (Enter)")
        else:
            user.add_birthday(birthday_value.value)
            added = True

    while True:
        email = func.input_data("Введіть e-mail: ")
        if email == "":
            break
        email_value = Email(email)
        if email_value.value is None:
            print("Не вірно вказано e-mail, повторіть ввід або вийдіть (Enter)")
        else:
            user.add_email(email_value.value)
            added = True

    if added:
        address = func.input_data("Введіть адресу: ")
        user.add_address(address)
        address_book.add_record(user)  # Add the user object to the address book
        print(f"Додано контакт: {user}")

"""


def change_phone(*arg):
    name = func.input_data("Введіть ім'я (Вийти 'Enter') \n")
    contact = address_book.find(name)
    if name == "":
        return None
    elif contact is None:
        print("Немає такого контакту")
        return None
    print(contact)
    phone = func.input_data("Введіть номер телефону який необхідно замінити (xxxxxxxxxx) (Вийти 'no') \n")
    if phone == 'no':
        return None
    elif Phone(phone).value:
        phone_new = func.input_data("Введіть новий номер телефону (xxxxxxxxxx) (Вийти 'no') \n")
        if phone_new == 'no':
            return None
        elif Phone(phone_new).value:
            contact = address_book.get(name)
            contact.remove_phone(phone)  # Видалити старий номер телефону
            contact.add_phone(phone_new)  # Додати новий номер телефону
            address_book.data[name] = contact  # Оновити контакт у address_book
            print(f"Змінено контакт: {contact}, новий номер телефону: {phone_new}")


def change_email(*arg):
    name = func.input_data("Введіть ім'я (Вийти 'Enter') \n")
    contact = address_book.find(name)
    if name == "":
        return None
    elif contact is None:
        print("Немає такого контакту")
        return None
    print(contact)
    email = func.input_data("Введіть e-mail який необхідно замінити (Вийти 'no') \n")
    if email == 'no':
        return None
    elif Email(email).value:
        email_new = func.input_data("Введіть новий номер телефону (xxxxxxxxxx) (Вийти 'no') \n")
        if email_new == 'no':
            return None
        elif Email(email_new).value:
            contact = address_book.get(name)
            #contact.remove_phone(phone)  # Видалити старий номер телефону
            contact.add_email(email_new)  # Додати новий номер телефону
            address_book.data[name] = contact  # Оновити контакт у address_book
            print(f"Змінено контакт: {contact}, новий e-mail: {email_new}")
 



def find_contact(*arg):
    pass


def show_all(*arg):
    print("Вивід всіх збеорежених контактів \n")
    #address_book.show_book(0, list=False)
    for value in address_book.values():
        print(value)


def when_birthday(*arg):
    result = func.input_data("Вкажіть ім'я контакту/(Вийти 'Enter')\n")
    if result=='':
        return
    else:
        if result in address_book and address_book[result].days_to_birthday():
            if address_book[result].days_to_birthday():
                print(address_book[result].days_to_birthday())
        else:
            print(f"не має запису в адресній книзі для: {result}")

@func.input_error
def contacts_birthday(*arg):
    result = func.input_data("Вкажіть кількість днів/(Вийти 'Enter')\n")
    if result=='':
        return
    try:
        days=int(result)
    except:
        raise ValueError('Введіть дні числом')
    if address_book.contact_for_birthday(int(result)):
        print(address_book.contact_for_birthday(int(result)))
    else:
        print(f'Через {days} днів ні в кого немає день народження')


def cleans_folder(*arg):
    result = func.input_data("Вкажіть шлях до папки/(Вийти 'Enter')\n")
    if result=='':
        return
    else:
        try:
            clean_folder.main(result)
        except:
            print(f'Невірний шлях до папки')


def good_bye(*arg):
    func.exit_boot(address_book.data, note_book.data)
    return "Good bye!"

def add_note(*arg):
    while True:
        result=func.input_data("Напишіть ключове слово(#..)/їх може бути декілька/\n")
        if result=='' or result[0]!='#':
            print('Некоректно введено тег')
        else:
            break
    text=[]
    print('Напишіть саму нотатку')
    while True:
        result2=input()
        if result2=='':
            break
        text.append(result2)
    if text:
        text = '\n'.join(text)
        note=Note(text,result)
        note_book.add_note(note)


def find_note(*arg):
    result = func.input_data("Напишіть ключове слово(#..)/їх може бути декілька/Вийти no\n")
    if result=='':
        return
    matches = note_book.find_notes(result)
    if matches:
        for i in matches:
            print(i)
    else:
        print("Немає нотатків по такому тегу")
        command='find_note'


def sort_notes(*arg):
    note_book.sort_notes()


def show_notes(*arg):
    if note_book.data:
        for tags in note_book.data:
            print('#'+tags)
            for note in note_book.data[tags]:
                print(f"{note.text}")


OPERATIONS = {
    'hello': hello,
    'add': add_contact,
    'change_phone': change_phone,
    'change_email': change_email,
    'phone': find_contact,
    'show all': show_all,
    'when_birthday': when_birthday,
    'contacts_birthday': contacts_birthday,
    'clean_folder': cleans_folder,
    'good bye': good_bye,
    'exit': good_bye,
    'close': good_bye,
    'add_note': add_note,
    'find_note': find_note,
    'sort_notes': sort_notes,
    'show_notes': show_notes
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
    return OPERATIONS.get(operator, None)




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

        commands = get_command(command)
        if commands is not None:
            result = commands(address_book, note_book)
            if result == "Good bye!":
                print("Good bye!")
                break
        else:
            print(f"Команда '{command}' не знайдена.")


"""
    'change': change,
    'phone': find_contact,

"""





if __name__ == "__main__":

    classes_used = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            classes_used.append(obj)

    main()




