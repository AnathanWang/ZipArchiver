import zipfile
import os

def archive_file(file_path):
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    archive_path = os.path.join(directory, f"{filename}.zip")
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, arcname=filename)
    print(f"Файл заархивирован: {archive_path}")

def unarchive_file(archive_path):
    directory = os.path.dirname(archive_path)
    with zipfile.ZipFile(archive_path, 'r') as zipf:
        zipf.extractall(directory)
    print("Файл успешно разохивирован.")

def exit_program():
    print("Выход из программы....")
    raise SystemExit
while True:
    user_input = input("Введите путь к файлу или ZIP-архиву (или 'exit' для выхода): ")
    if user_input.lower() == "exit":
        exit_program()
    if os.path.isfile(user_input):
        if user_input.endswith(".zip"):
            unarchive_file(user_input)
        else:
            archive_file(user_input)
    else:
        print("Неверный ввод. Введите правильный путь к файлу")