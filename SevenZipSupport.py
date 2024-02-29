import py7zr

# Создание архива 7z
def create_7z_archive(source_dir, output_filename):
    with py7zr.SevenZipFile(output_filename, 'w') as archive:
        archive.writeall(source_dir)

# Распаковка архива 7z
def extract_7z_archive(archive_filename, target_dir):
    with py7zr.SevenZipFile(archive_filename, 'r') as archive:
        archive.extractall(target_dir)

# Добавление файлов в архив 7z
def add_files_to_7z_archive(archive_filename, files_to_add):
    with py7zr.SevenZipFile(archive_filename, 'a') as archive:
        for file_path in files_to_add:
            archive.write(file_path)

# Удаление файлов из архива 7z
def remove_files_from_7z_archive(archive_filename, files_to_remove):
    with py7zr.SevenZipFile(archive_filename, 'a') as archive:
        for file_path in files_to_remove:
            archive.remove(file_path)

