import tkinter as tk
from tkinter import filedialog
import zipfile

def select_file():
    selected_file = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, selected_file)

def create_zip_archive():
    source_file = file_entry.get()
    if source_file:
        with zipfile.ZipFile("archive.zip", "w") as archive:
            archive.write(source_file, source_file.split("/")[-1])

# Создание графического интерфейса
root = tk.Tk()
root.title("ZZZArhiver")

file_label = tk.Label(root, text="Выберите файл для архивации:")
file_label.pack()

file_entry = tk.Entry(root, width=50)
file_entry.pack()

select_button = tk.Button(root, text="Архивация", command=select_file)
select_button.pack()

create_button = tk.Button(root, text="Разорхивация", command=create_zip_archive)
create_button.pack()

create_button = tk.Button(root, text="Создать архив", command=create_zip_archive)
create_button.pack()


root.mainloop()
