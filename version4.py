import tkinter as tk
from tkinter import filedialog
import zipfile
import os

def archive_file(file_path):
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    archive_path = os.path.join(directory, f"{filename}.zip")
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, arcname=filename)

def unarchive_file(archive_path):
    directory = os.path.dirname(archive_path)
    with zipfile.ZipFile(archive_path, 'r') as zipf:
        zipf.extractall(directory)

def select_file():
    selected_file = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, selected_file)

def select_archive():
    selected_archive = filedialog.askopenfilename()
    archive_entry.delete(0, tk.END)
    archive_entry.insert(0, selected_archive)

def archive_selected_file():
    source_file = file_entry.get()
    if os.path.isfile(source_file):
        archive_file(source_file)

def unarchive_selected_file():
    archive_path = archive_entry.get()
    if os.path.isfile(archive_path):
        if archive_path.endswith(".zip"):
            unarchive_file(archive_path)
        else:
            print("Неподдерживаемый формат архива. Поддерживается только ZIP.")

def exit_program():
    print("Выход из программы....")
    raise SystemExit

root = tk.Tk()
root.title("Archiver")

file_label = tk.Label(root, text="Выберите файл для архивации:")
file_label.pack()

file_entry = tk.Entry(root, width=50)
file_entry.pack()

select_file_button = tk.Button(root, text="Выбрать файл", command=select_file)
select_file_button.pack()

archive_button = tk.Button(root, text="Архивировать", command=archive_selected_file)
archive_button.pack()

archive_label = tk.Label(root, text="Выберите архив для разархивации:")
archive_label.pack()

archive_entry = tk.Entry(root, width=50)
archive_entry.pack()

select_archive_button = tk.Button(root, text="Выбрать архив", command=select_archive)
select_archive_button.pack()

unarchive_button = tk.Button(root, text="Разархивировать", command=unarchive_selected_file)
unarchive_button.pack()

exit_button = tk.Button(root, text="Выход", command=exit_program)
exit_button.pack()

root.mainloop()
