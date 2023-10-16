from collections import UserDict
class Note:
    def __init__(self,text,tag):
        self.text = text
        self.tag = [i.title() for i in tag.split('#')[1:]]
class Note_book(UserDict):
    def add_note(self,note):
        for i in note.tag:
            if i in self.data:
                self.data[i].append(note)
            else:
                self.data[i]=[note]
    def sort_notes(self):
        note_tags=self.data.keys()
        list_keys=list(note_tags)
        list_keys=sorted(list_keys)
        sorted_dict={}
        for i in list_keys:
            sorted_dict[i]=self.data[i]
        self.data=sorted_dict
    def find_notes(self,tag):
        tag=[i.title() for i in tag.split('#')[1:]]
        find_notes=[]
        for k,v in self.data.items():
            for i in v:
                if i.tag==tag and i.text not in find_notes:
                    find_notes.append(i.text)
        return find_notes


if __name__ == "__main__":

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