import pathlib
import os
import shutil

def normalize(filename, suffix):  # filename normalization
    global TRANS
    new_filename = ''
    for i in filename:
        if i.isdigit():
            new_filename += i
        elif i.isalpha():
            i = i.translate(TRANS)
            new_filename += i
        else:
            new_filename += '_'
    return new_filename + suffix


def sort_dir(path,list_dir,path_dict):
    p = pathlib.Path(path)
    for i in p.iterdir():
        if i.is_file():
            try:
                if i.suffix == '.zip' or i.suffix == '.tar' or i.suffix == '.gz':
                    shutil.unpack_archive(i, os.path.join('archives', i.stem))
                    os.remove(i)
                else:
                    shutil.move(i, os.path.join(path_dict[i.suffix.lower()],i.name))
                    os.rename(os.path.join(path_dict[i.suffix.lower()], i.name),
                              os.path.join(path_dict[i.suffix.lower()],normalize(i.stem, i.suffix)))
            except KeyError:
                pass
        else:
            if i.name not in list_dir:
                sort_dir(i,list_dir,path_dict)

                if len(os.listdir(i)) == 0:
                    os.rmdir(i,list_dir,path_dict)
                else:
                    os.rename(i, path + '/' + normalize(i.stem, i.suffix))


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def main(path):
    path_img = os.path.join(path, 'images')
    path_video = os.path.join(path, 'video')
    path_documents = os.path.join(path, 'documents')
    path_archives = os.path.join(path, 'archives')
    path_audio = os.path.join(path, 'audio')
    os.chdir(path)
    if not os.path.exists(path_img):
        os.mkdir(path_img)
    if not os.path.exists(path_video):
        os.mkdir(path_video)
    if not os.path.exists(path_documents):
        os.mkdir(path_documents)
    if not os.path.exists(path_archives):
        os.mkdir(path_archives)
    if not os.path.exists(path_audio):
        os.mkdir(path_audio)
    path_dict = {'.png': path_img,
                 '.jpg': path_img,
                 '.jpeg': path_img,
                 '.svg': path_img,
                 '.avi': path_video,
                 '.mp4': path_video,
                 '.mov': path_video,
                 '.mkv': path_video,
                 '.doc': path_documents,
                 '.docx': path_documents,
                 '.txt': path_documents,
                 '.pdf': path_documents,
                 '.xlsx': path_documents,
                 '.pptx': path_documents,
                 'mp3': path_audio,
                 'ogg': path_audio,
                 'wav': path_audio,
                 'amr': path_audio, }
    list_dir = ['audio', 'video', 'documents', 'archives', 'images']
    sort_dir(path,list_dir,path_dict)