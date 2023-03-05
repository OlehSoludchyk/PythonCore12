from pathlib import Path
import re
import shutil
import sys

# створюємо шлях до папки, якe буде приймати функція
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

# функція для нормалізації назви файлів (транслітерація, заміна символів)
def normalize(file_name_for_norm):
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
    for cyrylic, latun in translit_dict.items():
        file_name_for_norm = file_name_for_norm.replace(cyrylic, latun)

    # застосовуємо регулярний вираз, щоб замінити всі інші символи на символ '_'
    file_name_for_norm = re.sub(r'[^a-zA-Z0-9]', '_', file_name_for_norm)

    return file_name_for_norm


def sorted_files(p):
    
    # створюємо пусті списки для файлів
    files_in_images = []
    files_in_documents = []
    files_in_audio = []
    files_in_video = []
    files_in_archives = []
    files_in_unknown = []

    # проходимося по кожному елементу в папці
    for element in p.iterdir():
        # ігноруємо папки у які будемо сортувати
        if element.name in ('images', 'documents', 'audio', 'video', 'archives', 'unknown'):
            continue
        if element.is_file():
            if element.suffix.lower() in ('.jpeg', '.png', '.jpg', '.svg'):
                shutil.move(str(element), str(folder1 / element.name))
                files_in_images.append(element.name)
            elif element.suffix.lower() in ('.avi', '.mp4', '.mov', '.mkv'):
                shutil.move(str(element), str(folder4 / element.name))
                files_in_video.append(element.name)
            elif element.suffix.lower() in ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'):
                shutil.move(str(element), str(folder2 / element.name))
                files_in_documents.append(element.name)
            elif element.suffix.lower() in ('.mp3', '.ogg', '.wav', '.amr'):
                shutil.move(str(element), str(folder3 / element.name))
                files_in_audio.append(element.name)
            elif element.suffix.lower() in ('.zip', '.gz', '.tar'):
                # розпаковуємо знайдений архів у папку архів, stem обрізає розширення
                shutil.unpack_archive(str(element), str(folder5 / element.stem))
                files_in_archives.append(element.name)
            else:
                # всі інші файли кладемо у папку unknown
                shutil.move(str(element), str(folder6 / element.name))
                files_in_unknown.append(element.name)
	        # якщо елемент у папці є папкою викликаємо знову функцію для перегляду файлів у цій папці
        elif element.is_dir():
            sorted_files(element)
            # якщо немає елементів у папці, то вона видаляється
            if not list(element.iterdir()):
                element.rmdir()
    print({'images': files_in_images, 'documents': files_in_documents, 'audio': files_in_audio, 'video': files_in_video, 'archives': files_in_archives, 'unknown': files_in_unknown})
    return {'images': files_in_images, 'documents': files_in_documents, 'audio': files_in_audio, 'video': files_in_video, 'archives': files_in_archives, 'unknown': files_in_unknown}