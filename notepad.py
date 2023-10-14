
from main import Field, Record
class Notes(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            self.value = self.is_note(value)
        except ValueError:
            print ("Формат нотатків: не меньше 3 символів")
            self.value = ""

    def is_note(self, value):
        if not value or len(value)<3:
            print ("Формат нотатків: не меньше 3 символів")
            return ""
            #raise ValueError
        return value


class RecordExtension(Record):
    def __init__(self):
        super().__init__()
        self.notes = []

    def add_note(self, note):
        for i in self.notes:
            if str(i) == note:
                return False
        result = Notes(note)
        if result.value:
            self.notes.append(result)
            print(f"нотаток: {note}  - додано")
        else:
            print (f"нотаток: {note}  - не додано")

    def remove_note(self, note):
        self.notes = [p for p in self.notes if str(p) != note]

    def find_note(self, note):
        for i in self.notes:
            if str(i) == note:
                return Notes(note)
        return None

    def edit_note(self, note_old, note_new):
        if self.find_note(note_old):
            self.remove_note(note_old)
            self.add_note(note_new)
        else:
            raise ValueError
        return


"""
  'Змінній  command  додати нову команду  'note'
   command = func.input_data("Чекаю команду (hello, add, change, phone, show all,good bay, note)\n").lower() 



  'У циклі while True додати нову умову'

   elif command == "note":
            name = func.input_data("Введіть ім'я для нотатків (Вийти 'Enter') \n")
            if not name:
                print('ім'я не введено')
                name, note = "", ""
                continue
                
            note = func.input_data("Введіть свої нотатки (Вийти 'exit') \n")
            if note == 'exit':
                print('нотатки не введено')
                continue  
            
            if Notes(result).value:
                user = RecordExtension(name)
                
                if note not in Notes(result).value:
                    user.add_note(result)
                    # address_book.add_record(user) 
                    print(f"Додано нотатки для : {user}")
                else:
                    user.edit_note(Notes(result).value, note)             
             
                name, note, command = "", "", ""
            else:
                print(f"Нотатки для : {user}  не додано")
   

"""