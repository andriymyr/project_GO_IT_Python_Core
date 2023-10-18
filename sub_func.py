import func

def hello():
    print("How can I help you?")

def add_contact():
    name = func.input_data("Введіть ім'я контакту: ")
    if name == "":
        return
    while True:
        phone = func.input_data("Введіть номер телефону (xxxxxxxxxx): ")
        phone = main.r
        if 
    birthday = func.input_data("Введіть дату деня народження (dd/mm/yyyy): ")
    address = func.input_data("Введіть адресу: ")
    email = func.input_data("Введіть e-mail: ")
    user = Record(name, birthday=birthday)
    user = Record(name)
    user.add_phone(phone)
    user.add_address(address)
    user.add_email(email)
    address_book.add_record(user)
    print(f"Додано контакт : {user}")