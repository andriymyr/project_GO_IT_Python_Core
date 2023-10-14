import pickle


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



