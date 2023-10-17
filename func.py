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
def exit_boot(*arg):
    print("Good bye!")
    with open("adressbook.bin", "wb") as fh:
        for i in arg:
            pickle.dump(i,fh)

    return "exit"

def verification_date(value):
    value = value.replace(".", "/")
    day_pattern = r"\d{2}/\d{2}/\d{4}"
    if not re.match(day_pattern, value):
        raise ValueError("неправильний формат дати")
    try:
        datetime.strptime(value, "%d/%m/%Y")
        return value
    except ValueError:
        #raise ValueError("неправильно вказано дату")
        return ""

def verification_emails(text):
    """
    перевірка правильності написання e-mail
    """
    text = re.findall(r"[a-zA-Z][a-zA-Z._0-9]+@\w+\.+\w\w+", text)
    if text == []:
        print ("Введено неправильний e-mail")
    return text
