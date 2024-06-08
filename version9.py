import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QComboBox, QHBoxLayout
from PyQt5.QtGui import QFont
import zipfile
import os
from py7zr import SevenZipFile
from rarfile import RarFile
import tarfile
from tempfile import NamedTemporaryFile
import shutil


class ArchiverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Архиватор")

        self.file_label = QLabel("Выберите файл для архивации:")
        self.file_label.setFont(QFont("Arial", 10, QFont.Bold))  # установим жирный шрифт
        self.file_entry = QLineEdit()

        self.select_file_button = QPushButton("Выбрать файл")
        self.select_file_button.clicked.connect(self.select_file)

        self.select_destination_archive_button = QPushButton("Выбрать место для архивации")
        self.select_destination_archive_button.clicked.connect(self.select_destination_archive)

        self.file_buttons_layout = QHBoxLayout()
        self.file_buttons_layout.addWidget(self.select_file_button)
        self.file_buttons_layout.addWidget(self.select_destination_archive_button)

        self.format_label = QLabel("Выберите формат архивации:")
        self.format_label.setFont(QFont("Arial", 10, QFont.Bold))  # установим жирный шрифт
        self.format_combo = QComboBox()
        self.format_combo.addItems(["ZIP", "7Z", "TAR"])

        self.archive_button = QPushButton("Архивировать")
        self.archive_button.clicked.connect(self.archive_selected_file)

        self.archive_label = QLabel("Выберите архив для разархивации:")
        self.archive_label.setFont(QFont("Arial", 10, QFont.Bold))  # установим жирный шрифт
        self.archive_entry = QLineEdit()

        self.select_archive_button = QPushButton("Выбрать архив")
        self.select_archive_button.clicked.connect(self.select_archive)

        self.select_destination_unarchive_button = QPushButton("Выбрать место для разархивации")
        self.select_destination_unarchive_button.clicked.connect(self.select_destination_unarchive)

        self.archive_buttons_layout = QHBoxLayout()
        self.archive_buttons_layout.addWidget(self.select_archive_button)
        self.archive_buttons_layout.addWidget(self.select_destination_unarchive_button)

        self.unarchive_button = QPushButton("Разархивировать")
        self.unarchive_button.clicked.connect(self.unarchive_selected_file)

        self.edit_label = QLabel("Редактировать архив:")
        self.edit_label.setFont(QFont("Arial", 10, QFont.Bold))  # установим жирный шрифт
        self.edit_entry = QLineEdit()
        self.select_edit_button = QPushButton("Выбрать архив для редактирования")
        self.select_edit_button.clicked.connect(self.select_edit_archive)

        self.add_files_button = QPushButton("Добавить файлы")
        self.add_files_button.clicked.connect(self.add_files_to_archive)

        self.remove_files_button = QPushButton("Удалить файлы")
        self.remove_files_button.clicked.connect(self.remove_files_from_archive)

        self.edit_buttons_layout = QHBoxLayout()
        self.edit_buttons_layout.addWidget(self.add_files_button)
        self.edit_buttons_layout.addWidget(self.remove_files_button)

        self.exit_button = QPushButton("Выход")
        self.exit_button.clicked.connect(self.exit_program)

        layout = QVBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_entry)
        layout.addLayout(self.file_buttons_layout)
        layout.addWidget(self.format_label)
        layout.addWidget(self.format_combo)
        layout.addWidget(self.archive_button)
        layout.addWidget(self.archive_label)
        layout.addWidget(self.archive_entry)
        layout.addLayout(self.archive_buttons_layout)
        layout.addWidget(self.unarchive_button)
        layout.addWidget(self.edit_label)
        layout.addWidget(self.edit_entry)
        layout.addWidget(self.select_edit_button)
        layout.addLayout(self.edit_buttons_layout)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл или папку", options=options)

        if not file_path:
            file_path = QFileDialog.getExistingDirectory(self, "Выберите папку", options=options)

        if file_path:
            self.file_entry.setText(file_path)

    def select_archive(self):
        archive_path, _ = QFileDialog.getOpenFileName(self, "Выберите архив")
        if archive_path:
            self.archive_entry.setText(archive_path)

    def select_edit_archive(self):
        archive_path, _ = QFileDialog.getOpenFileName(self, "Выберите архив для редактирования")
        if archive_path:
            self.edit_entry.setText(archive_path)

    def select_destination_archive(self):
        self.archive_destination_path = QFileDialog.getExistingDirectory(self, "Выберите место для сохранения архива")
        if self.archive_destination_path:
            QMessageBox.information(self, "Выбрано место для архивации", f"Выбранная директория для архивации: {self.archive_destination_path}")

    def select_destination_unarchive(self):
        self.archive_destination_path = QFileDialog.getExistingDirectory(self, "Выберите папку для разархивации")
        if self.archive_destination_path:
            QMessageBox.information(self, "Выбрано место для разархивации", f"Выбранная директория для разархивации: {self.archive_destination_path}")

    def archive_file(self, path, archive_format):
        if os.path.isfile(path):
            directory = os.path.dirname(path)
            filename = os.path.basename(path)
            if archive_format == "ZIP":
                archive_path = os.path.join(directory, f"{filename}.zip")
                with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(path, arcname=filename)
                self.show_success_message("архивации")
            elif archive_format == "7Z":
                archive_path = os.path.join(directory, f"{filename}.7z")
                with SevenZipFile(archive_path, 'w') as szf:
                    szf.write(path)
                self.show_success_message("архивации")
            elif archive_format == "TAR":
                archive_path = os.path.join(directory, f"{filename}.tar")
                with tarfile.open(archive_path, 'w') as tar:
                    tar.add(path, arcname=filename)
                self.show_success_message("архивации")
        elif os.path.isdir(path):
            directory = os.path.dirname(path)
            foldername = os.path.basename(path)
            if archive_format == "ZIP":
                archive_path = os.path.join(directory, f"{foldername}.zip")
                with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, start=path)
                            zipf.write(file_path, arcname=arcname)
                self.show_success_message("архивации")
            elif archive_format == "7Z":
                archive_path = os.path.join(directory, f"{foldername}.7z")
                with SevenZipFile(archive_path, 'w') as szf:
                    szf.writeall(path, foldername)
                self.show_success_message("архивации")
            elif archive_format == "TAR":
                archive_path = os.path.join(directory, f"{foldername}.tar")
                with tarfile.open(archive_path, 'w') as tar:
                    tar.add(path, arcname=foldername)
                self.show_success_message("архивации")

    def unarchive_file(self, archive_path):
        if os.path.isfile(archive_path):
            directory = os.path.dirname(archive_path)
            if archive_path.endswith(".zip"):
                with zipfile.ZipFile(archive_path, 'r') as zipf:
                    zipf.extractall(directory)
            elif archive_path.endswith(".7z"):
                with SevenZipFile(archive_path, 'r') as szf:
                    szf.extractall(directory)
            elif archive_path.endswith(".rar"):
                with RarFile(archive_path, 'r') as rar:
                    rar.extractall(directory)
            elif archive_path.endswith(".tar"):
                with tarfile.open(archive_path, 'r') as tar:
                    tar.extractall(directory)
            self.show_success_message("разархивации")

    def edit_archive(self, archive_path, operation, files=[],):
        if os.path.isfile(archive_path):
            try:
                if archive_path.endswith(".zip"):
                    if operation == "add":
                        with zipfile.ZipFile(archive_path, 'a') as zipf:
                            for file in files:
                                zipf.write(file, arcname=os.path.basename(file))
                    elif operation == "remove":
                        with zipfile.ZipFile(archive_path, 'r') as zipf:
                            file_list = zipf.namelist()
                            with NamedTemporaryFile(mode='w+b', delete=False) as temp_zip:
                                with zipfile.ZipFile(temp_zip, 'w') as temp_zipf:
                                    for item in file_list:
                                        if item not in files:
                                            temp_zipf.writestr(item, zipf.read(item))
                        shutil.move(temp_zip.name, archive_path)
                elif archive_path.endswith(".7z"):
                    if operation == "add":
                        with SevenZipFile(archive_path, 'a') as szf:
                            for file in files:
                                szf.write(file)
                    elif operation == "remove":
                        with SevenZipFile(archive_path, 'r') as szf:
                            file_list = szf.getnames()
                            with NamedTemporaryFile(mode='w+b', delete=False) as temp_7z:
                                with SevenZipFile(temp_7z, 'w') as temp_szf:
                                    for item in file_list:
                                        if item not in files:
                                            temp_szf.write(item, szf.read(item))
                        shutil.move(temp_7z.name, archive_path)
                elif archive_path.endswith(".tar"):
                    if operation == "add":
                        with tarfile.open(archive_path, 'a') as tar:
                            for file in files:
                                tar.add(file, arcname=os.path.basename(file))
                    elif operation == "remove":
                        with tarfile.open(archive_path, 'r') as tar:
                            file_list = tar.getnames()
                            with NamedTemporaryFile(delete=False) as temp_tar:
                                with tarfile.open(temp_tar.name, 'w') as temp_tarfile:
                                    for item in file_list:
                                        if item not in files:
                                            temp_tarfile.addfile(tar.getmember(item), tar.extractfile(item))
                        shutil.move(temp_tar.name, archive_path)
                self.show_success_message("редактирования")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при редактировании архива: {e}")

    def show_success_message(self, operation):
        QMessageBox.information(self, "Успешно", f"Операция {operation} выполнена успешно!")

    def archive_selected_file(self):
        source_path = self.file_entry.text()
        if os.path.exists(source_path) and self.archive_destination_path:
            archive_format = self.format_combo.currentText()
            self.archive_file(source_path,archive_format, self.archive_destination_path)

    def unarchive_selected_file(self):
        archive_path = self.archive_entry.text()
        if os.path.exists(archive_path) and self.archive_destination_path:
            self.unarchive_file(archive_path, self.archive_destination_path)

    def add_files_to_archive(self):
        archive_path = self.edit_entry.text()
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы для добавления в архив")
        if archive_path and files:
            self.edit_archive(archive_path, "add", files)

    def remove_files_from_archive(self):
        archive_path = self.edit_entry.text()
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы для удаления из архива")
        if archive_path and files:
            self.edit_archive(archive_path, "remove", files)

    def exit_program(self):
        print("Выход из программы....")
        sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    archiver_app = ArchiverApp()
    archiver_app.show()
    sys.exit(app.exec_())
