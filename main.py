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
from notepad_old import Note, Note_book

class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, name):
        super().__init__(name)
        self.name = name


class Address(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f"Address: {self.value}"


class Email(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = self.is_data(value)

    def is_data(self, value):
        if value != "":
            value = func.verification_emails(value)
        return value

    def __str__(self):
        return f"Email: {self.value}"


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = self.is_data(value)

    def is_data(self, value):
        if value != "":
            value = func.verification_date(value)
        return value

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
    def __init__(self, name, birthday = ""):           #address = "", email = "", birthday = ""):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)
        self.address = ""  #Address(address)
        self.email = "" #Email(email)

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





base_commands = ["hello", "add", "change", "phone", "show all", "when_birthday", "contacts_birthday", "clean_folder", "good bye", "exit", "close", "add_note", "find_note", "sort_notes", "show_notes"]


def suggest_command(user_input):
    best_match = difflib.get_close_matches(user_input, base_commands, n=1, cutoff=0.75)

    if best_match:
        return f"Можливо ви мали на увазі команду '{best_match[0]}'?"
    else:
        return "Не знайдено відповідної команди."


def main():
    note_book=Note_book()
    address_book = AddressBook()
    try:
        with open("adressbook.bin", "rb") as fh:
            address_book.data = pickle.load(fh)
    except EOFError:
        pass
    except FileNotFoundError:
        pass

    command, name, phone, birthday = "", "", "",""
    while True:
        if not command:
            command = func.input_data(f"Чекаю команду\n{base_commands}\n").lower()
            if command not in base_commands:
                suggestion = suggest_command(command)
                print(suggestion)
                continue
        elif command == "hello":
            print("How can I help you?")
            command = ""
        elif command == "add":
            command = ""
            if not name:
                name = func.input_data("Введіть ім'я (Вийти 'Enter') \n")
            if not name:
                name, phone, address, email = "", "", "", ""
                continue
            elif not phone:
                result = func.input_data("Введіть номер телефону (xxxxxxxxxx) (Вийти 'no') \n")
            if result == 'no':
                continue
            if Phone(result).value:
                if not birthday:
                    birthday = func.input_data("Введіть день народження (Необов'язково/Пропустити 'skip') \n")
                    if birthday == 'skip' or birthday=='':
                        birthday = ''
                #if birthday:
                #    user = Record(name, birthday=birthday)
                #    user.add_phone(result)
                #    address_book.add_record(user)
                #else:
                #    user = Record(name)
                #    user.add_phone(result)
                #    address_book.add_record(user)
                address = func.input_data("Введіть адресу (Вийти 'no') \n")
                if address == 'no':
                    continue
                email = func.input_data("Введіть email (Вийти 'no') \n")
                if email == 'no':
                    continue
                if birthday:
                    user = Record(name, birthday=birthday)
                else:
                    user = Record(name)
                user.add_phone(result)
                user.add_address(address)
                user.add_email(email)
                address_book.add_record(user)
                print(f"Додано контакт : {user}")
                name, phone, address, email, command = "", "", "", "", ""
            else:
                birthday=''
                command = "add"
        elif command == "change":
            print("Зміна реквізитів контакту")
            command = ""
            if not name:
                name = func.input_data("Введіть ім'я (Вийти 'Enter') \n")
            if not name:
                name, phone = "", ""
                continue
            elif not phone:
                print(address_book.find(name))
                result = func.input_data("Введіть номер телефону який необхідно замінити (xxxxxxxxxx) (Вийти 'no') \n")
                if Phone(result).value:
                    result_one = func.input_data(
                        "Введіть номер телефону який необхідно замінити (xxxxxxxxxx) (Вийти 'no') \n")
            if result == 'no':
                continue
            if result_one == 'no':
                continue
            if Phone(result).value:
                if Phone(result_one).value:
                    user = Record(name)
                    user.edit_phone(result, result_one)
                    print(f"Змінено контакт : {user}, телефонний номер {result_one}")
                    birthday,name, phone, command = "", "", "",""
            else:
                command = "change"
        elif command == "phone":  # задає пошук по номеру назві їх частинах
            command = ""
            print("Пошук телефонну/контакту")
            result = func.input_data("Введіть ім'я обо номер телефону /можна частково/ через прбіл (Вийти 'Enter') \n")
            if result == "":
                command = "phone"
                continue
            for i in (result.split(" ")):
                for result in address_book:
                    if i in str(result):
                        print("Значення пошуку {:>20}, результат {:>50}.".format(i, str(result)))
                        # print(f"Значення пошуку {i}, результат {result}")
                    else:
                        print(f"не має запису в адресній книзі для: {i}")
        elif command == "show all":
            command = ""
            print("Вивід всіх збеорежених контактів \nІм'я та номер телефону")
            address_book.show_book(0, list=False)
        elif command=="when_birthday":
            command=''
            result = func.input_data("Вкажіть ім'я контакту/(Вийти 'no')/(Вийти 'Enter')\n")
            if result == 'no' or result=='':
                continue
            else:
                if result in address_book and address_book[result].days_to_birthday():
                    if address_book[result].days_to_birthday():
                        print(address_book[result].days_to_birthday())
                else:
                    print(f"не має запису в адресній книзі для: {result}")
        elif command=="contacts_birthday":
            command=''
            result = func.input_data("Вкажіть кількість днів/(Вийти 'no')/(Вийти 'Enter')\n")
            if result=='' or result=='no':
                continue
            try:
                days=int(result)
            except:
                raise ValueError('Введіть дні числом')
            if address_book.contact_for_birthday(int(result)):
                print(address_book.contact_for_birthday(int(result)))
            else:
                print(f'Через {days} днів ні в кого немає день народження')
        elif command=="clean_folder":
            command=''
            result = func.input_data("Вкажіть шлях до папки/(Вийти 'no')/(Вийти 'Enter')\n")
            if result=='no' or result=='':
                continue
            else:
                try:
                    clean_folder.main(result)
                except:
                     print(f'Невірний шлях до папки')
                     command='clean_folder'
        elif command=='add_note':
            command=''
            try:
                result=func.input_data("Напишіть ключове слово(#..)/їх може бути декілька/Вийти no\n")
            except:
                print('Некоректно введено тег')
                command='add_note'
                continue
            if result=='' or result=='no' or result[0]!='#':
                print('Некоректно введено тег')
                continue
            text=[]
            print('Напишіть саму нотатку(Вийти no)')
            while True:
                result2=input()
                if result2=='no' or result2=='':
                    break
                text.append(result2)
            if text:
                text = '\n'.join(text)
                note=Note(text,result)
                note_book.add_note(note)
        elif command == "sort_notes":
            command=''
            note_book.sort_notes()
            print('Нотатки відсортовано')
        elif command == "find_note":
            command=''
            result = func.input_data("Напишіть ключове слово(#..)/їх може бути декілька/Вийти no\n")
            if result=='' or result == 'no':
                continue
            matches = note_book.find_notes(result)
            if matches:
                for i in matches:
                    print(i)
            else:
                print("Немає нотатків по такому тегу")
                command='find_note'
        elif command == "show_notes":
            command = ''
            if note_book.data:
                for tags in note_book.data:
                    print('#'+tags)
                    for note in note_book.data[tags]:
                        print(f"{note.text}")
        elif command == "good bye":
            command = func.exit_boot(address_book.data)
        elif command == "close":
            command = func.exit_boot(address_book.data)
        elif command == "exit":
            # func.exit_boot(address_book, classes_used)
            func.exit_boot(address_book.data)
            break
        else:
            command = ""


if __name__ == "__main__":

    classes_used = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            classes_used.append(obj)

    main()
    # file_name = 'data.bin'

    # with open(file_name, "wb") as fh:
    #    pickle.dump(some_data, fh)






"""

    address_book = AddressBook()
    test = dict()
    for i in range(2):
        test[i] = Record((f"Jan_{i}"),"30/01/1955")
        test[i].add_phone("0987654321")
        test[i].add_phone("0999999999")
        address_book.add_record(test[i])    

    test[0].add_phone("09876543210")



    address_book.show_book(10,True)

    input("------------------")

    address_book.show_book(10)

    input("------------------")

    address_book.show_book()

"""
