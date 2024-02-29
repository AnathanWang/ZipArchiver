import rarfile

# Распаковка архива RAR
def extract_rar_archive(archive_filename, target_dir):
    with rarfile.RarFile(archive_filename, 'r') as archive:
        archive.extractall(target_dir)

# Создание архива RAR
def create_rar_archive(source_dir, output_filename):
    with rarfile.RarFile(output_filename, 'w') as archive:
        archive.add(source_dir)

# Добавление файлов в архив RAR
def add_files_to_rar_archive(archive_filename, files_to_add):
    with rarfile.RarFile(archive_filename, 'a') as archive:
        for file_path in files_to_add:
            archive.add(file_path)

# Удаление файлов из архива RAR
def remove_files_from_rar_archive(archive_filename, files_to_remove):
    with rarfile.RarFile(archive_filename, 'a') as archive:
        for file_path in files_to_remove:
            archive.remove(file_path)

