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
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, Birthday: {self.birthday.value}\naddress: {self.address.value}, e-mail: {self.email.value}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone):
        for i in self.phones:
            if str(i) == phone:
                return False
        result = Phone(phone)
        if result.value:
            self.phones.append(result)
        else:
            print(f"телефон {phone} не додано: неправильний номер телефону")

    def add_address(self, address):
        self.address = Address(address)

    def add_email(self, email):
        self.email = Email(email)

    def add_birthday(self, birthday):
        self.email = Birthday(birthday)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, phone_old, phone_new):
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
        birthday_date = datetime.strptime(str(self.birthday), "%d/%m/%Y").date()
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
        for i in self.data.values():  # address_book:
            print(i)
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

    def contact_for_birthday(self,days):
        now=datetime.now().date()
        res=''
        days_interval=timedelta(days=days)
        for k,v in self.data.items():
            if v.birthday.value:
                date = datetime(year=now.year, month=now.month, day=now.day)+days_interval
                birthday_date = datetime.strptime(str(v.birthday.value), "%d/%m/%Y").date()
                birthday_date_new = birthday_date.replace(year=date.year)
                if date.date()==birthday_date_new:
                    res+=f'Contact name: {k} phones:'+str(*v.phones)+'\n'
        return res

    def __str__(self):
        print(f"\nAddressBook list name: ")
        for i in self.data.values():
            print(i)
        return "AddressBook"

    def __iter__(self):
        self.records_iterator = iter(self.data.values())
        return self

    def __next__(self):
        data = next(self.records_iterator, "")
        if not data:
            raise StopIteration
        return data


def hello():
    print("How can I help you?")


def add_contact(address_book):
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
            #print(phone_value.value,"phone")
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
            #print(birthday_value.value,"birt")
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
            #print(email_value.value,"email")
            user.add_email(birthday_value.value)
            added = True
            break
    if added:
        address = func.input_data("Введіть адресу: ")
        user.add_address(address)
        address_book.add_record(user)
        print(f"Додано контакт : {user}")


def change():
    pass


def find_contact():
    pass


def show_all():
    print("Вивід всіх збеорежених контактів \n")
    address_book.show_book(0, list=False)
    


def when_birthday(address_book):
    result = func.input_data("Вкажіть ім'я контакту/(Вийти 'Enter')\n")
    if result=='':
        return
    else:
        if result in address_book and address_book[result].days_to_birthday():
            if address_book[result].days_to_birthday():
                print(address_book[result].days_to_birthday())
        else:
            print(f"не має запису в адресній книзі для: {result}")


def contacts_birthday(address_book):
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


def cleans_folder():
    result = func.input_data("Вкажіть шлях до папки/(Вийти 'Enter')\n")
    if result=='':
        return
    else:
        try:
            clean_folder.main(result)
        except:
            print(f'Невірний шлях до папки')


def good_bye():
    pass


def add_note(note_book):
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


def find_note(note_book):
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


def sort_notes(note_book):
    note_book.sort_notes()


def show_notes(note_book):
    if note_book.data:
        for tags in note_book.data:
            print('#'+tags)
            for note in note_book.data[tags]:
                print(f"{note.text}")


OPERATIONS = {
    'hello': hello,
    'add': add_contact,
    'change': change,
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
    return OPERATIONS[operator]


address_book = AddressBook()
note_book = Note_book()

def main():
    
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
        commands=get_command(command)
        if command == 'hello':
            result = commands()
        elif command == 'add':
            add_contact(address_book)  # Передача `address_book` як аргумент
        elif command == 'show all':
            result = commands()
        elif command == 'add_note':
            add_note(note_book)
        elif command == 'find_note':
            find_note(note_book)
        elif command == 'sort_notes':
            sort_notes(note_book)
        elif command == 'show_notes':
            show_notes(note_book)
        elif command == 'when_birthday':
            when_birthday(address_book)
        elif command == 'contacts_birthday':
            when_birthday(address_book)
        elif command == 'scleans_folder':
            result = commands()
        elif command == 'good bye' or command == 'close' or command == 'exit':
            func.exit_boot(address_book, note_book)
            break
        else:
            result = commands()



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




