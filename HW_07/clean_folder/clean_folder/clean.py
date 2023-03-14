from pathlib import Path
import re
import shutil
import sys
import os

# створюємо шлях до папки, який буде прийматися через командний рядок
p = Path(sys.argv[1])

# створюємо папки у які будемо складати файли за типом
folder1 = p / 'images'    
folder1.mkdir(parents = True, exist_ok = True)
folder2 = p / 'documents'
folder2.mkdir(parents = True, exist_ok = True)
folder3 = p / 'audio'
folder3.mkdir(parents = True, exist_ok = True)
folder4 = p / 'video'
folder4.mkdir(parents = True, exist_ok = True)
folder5 = p / 'archives'
folder5.mkdir(parents = True, exist_ok = True)
folder6 = p / 'unknown'
folder6.mkdir(parents = True, exist_ok = True)

# створюємо пусті списки для файлів
files_in_images = []
files_in_documents = []
files_in_audio = []
files_in_video = []
files_in_archives = []
files_in_unknown = []

# функція для нормалізації назви файлів (транслітерація, заміна символів)
def normalize(name_for_norm):
    # створюємо словник відповідностей для транслітерації букв
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie',
        'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l',
        'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ю': 'iu',
        'я': 'ia', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E',
        'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y',
        'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S',
        'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh',
        'Щ': 'Shch', 'Ю': 'Yu', 'Я': 'Ya'
    }
    # виконується транслітерація кириличних символи на латиницю
    for cyr, lat in translit_dict.items():
        name, extension = os.path.splitext(name_for_norm)
        new_name = name.replace(cyr, lat)
        new_name = re.sub(r'[^a-zA-Z0-9]', '_', new_name)
    return new_name + extension

# проходимося по кожному елементу в папці
for element in p.glob("**/*"):
    # ігноруємо папки у які будемо сортувати
    if element.name in ('images', 'documents', 'audio', 'video', 'archives', 'unknown'):
        continue
    # сортування в залежності від розширення файлу
    if element.is_file():
        normalized_file_name = normalize(element.name)
        if element.suffix.lower() in ('.jpeg', '.png', '.jpg', '.svg'):
            shutil.move(str(element), str(folder1 / normalized_file_name))
            files_in_images.append(normalized_file_name)
        elif element.suffix.lower() in ('.avi', '.mp4', '.mov', '.mkv'):
            shutil.move(str(element), str(folder4 / normalized_file_name))
            files_in_video.append(normalized_file_name)
        elif element.suffix.lower() in ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'):
            shutil.move(str(element), str(folder2 / normalized_file_name))
            files_in_documents.append(normalized_file_name)
        elif element.suffix.lower() in ('.mp3', '.ogg', '.wav', '.amr'):
            shutil.move(str(element), str(folder3 / normalized_file_name))
            files_in_audio.append(normalized_file_name)
        elif element.suffix.lower() in ('.zip', '.gz', '.tar', '.rar'):
            dir_archive = folder5 / element.stem
            dir_archive.mkdir(parents = True, exist_ok = True)
            # розпаковуємо знайдений архів у папку архів, stem обрізає розширення
            shutil.unpack_archive(str(element), str(dir_archive))
            files_in_archives.append(normalized_file_name)
        else:
            # всі інші файли кладемо у папку unknown
            shutil.move(str(element), str(folder6 / normalized_file_name))
            files_in_unknown.append(normalized_file_name)
    elif element.is_dir():
        if not list(element.iterdir()):
        # якщо папка пуста - видаляється
            element.rmdir()

# видаляємо папки, які не потрібні
for item in p.glob("*"):
    if item.is_dir() and item.name not in ['archives', 'images', 'documents', 'video', 'audio', 'unknown']:
        shutil.rmtree(item)

# видаляємо файли, які не потрбіні
for item in p.iterdir():
    if item.is_file():
        item.unlink()

print({'images': files_in_images, 'documents': files_in_documents, 'audio': files_in_audio, 'video': files_in_video, 'archives': files_in_archives, 'unknown': files_in_unknown})

if __name__ == '__main__':
    print('Images:', files_in_images)
    print('Documents:', files_in_documents)
    print('Audio:', files_in_audio)
    print('Video:', files_in_video)
    print('Archives:', files_in_archives)
    print('Unknown:', files_in_unknown)