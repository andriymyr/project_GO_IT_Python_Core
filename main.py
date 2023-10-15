from collections import UserDict
from datetime import datetime, timedelta
from pathlib import Path
import clean_folder
import inspect
import pickle
import sys
import func
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)
        self.name = name


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = self.is_data(value)

    def is_data(self, value):
        if value is None:
            return None
        value = value.replace(".", "/")
        day_pattern = r"\d{2}/\d{2}/\d{4}"
        if not re.match(day_pattern, value):
            raise ValueError("неправильний формат дати")
        try:
            datetime.strptime(value, "%d/%m/%Y")
            return value
        except ValueError:
            raise ValueError("неправильно вказано дату")
            return None

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
        phone_pattern = r"^[0-9]{10}$"
        if not re.match(phone_pattern, value):
            # print ("неправильний номер телефону ", value)
            return ""
            # raise ValueError
        return value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = self.is_phone(value)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)
        self.address = None
        self.email = None

    def __str__(self):
        if self.birthday.value:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, Birthday: {self.birthday.value}"
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

    def find(self, arg):
        for i in self.phones:
            input(f"<<<<<>>>>>>{i}")
            if str(i) == arg:
                return Phone(arg)        
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


class Address(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f"Address: {self.value}"


class Email(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f"Email: {self.value}"


def main():
    address_book = AddressBook()
    with open("adressbook.bin", "rb") as fh:
        try:
            address_book.data = pickle.load(fh)
        except EOFError:
            pass
    command, name, phone,birthday = "", "", "",""
    while True:
        if not command:
            command = func.input_data("Чекаю команду (hello, add, change, phone, show all,good bay)\n").lower() 
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
                user = Record(name)
                user.add_phone(result)
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
            address_book.show_book(0,list=False)
        elif command == "good bye":
            command = func.exit_boot(address_book.data)
        elif command == "close":
            command = func.exit_boot(address_book.data)
        elif command == "exit":
            # func.exit_boot(address_book, classes_used)
            func.exit_boot(address_book.data)
            break
        else:
            print("Не існує такої команди")
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
