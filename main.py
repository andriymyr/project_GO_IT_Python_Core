import inspect
import pickle
import sys
import func
import difflib
from notepad import Note, Note_book


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return f"Name: {self.value}"


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
                raise ValueError("Введено неправильний e-mail")
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
        if re.match(phone_pattern_1, value) == re.match(phone_pattern_2, value):
            return ""
        return value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = self.is_phone(value)


class Record:
    def __init__(self, name, birthday=""):
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

    def add_address(self, address):
        self.address = Address(address)

    def add_email(self, email):
        self.email = Email(email)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p.value) != phone]

    def edit_phone(self, phone_old, phone_new):
        if self.find_phone(phone_old):
            self.remove_phone(phone_old)
            self.add_phone(phone_new)

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
            return (
                birthday_date.replace(year=(current_data.year + 1)) - current_data
            ).days


class AddressBook(UserDict):
    def add_record(self, value):
        self.data[value.name.value] = value

    def find(self, value):
        return self.data.get(value)

    def find_contact(self, value):
        result = [self.data.get(contact) for contact in self.data if value in contact]
        return result

    def find_all(self, value):
        list_contact = [str(self.data.get(contact)) for contact in self.data]
        result = [contact for contact in list_contact if value in str(contact)]
        return result

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
        now = datetime.now().date()
        result = ""

        days_interval = timedelta(days=days)
        for key, value in self.data.items():
            if value.birthday.value:
                date = (
                    datetime(year=now.year, month=now.month, day=now.day)
                    + days_interval
                )
                birthday_date = datetime.strptime(
                    str(value.birthday.value), "%d/%m/%Y"
                ).date()
                birthday_date_new = birthday_date.replace(year=date.year)
                if date.date() == birthday_date_new:
                    result += f"Contact name: {key} phones:" + str(*value.phones) + "\n"
        return result

    def __str__(self):
        print(f"\nAddressBook list name: ")
        for i in self.data.values():
            print(i)
        return "AddressBook"


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
    return OPERATIONS.get(operator, (None, None, None))


def main():
    global address_book
    global note_book
    global list_command

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
        command = func.input_data(f"Чекаю команду\n").lower()
        if command not in list_command:
            suggestion = suggest_command(command)
            print(suggestion)
            continue

        command_function = get_command(command)
        if command_function is not None:
            result = command_function(address_book, note_book, list_command)
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
