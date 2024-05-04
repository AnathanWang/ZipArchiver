import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QComboBox
import zipfile
import os
from py7zr import SevenZipFile
from rarfile import RarFile
import tarfile

class ArchiverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Archiver")

        self.file_label = QLabel("Выберите файл для архивации:")
        self.file_entry = QLineEdit()
        self.select_file_button = QPushButton("Выбрать файл")
        self.select_file_button.clicked.connect(self.select_file)

        self.format_label = QLabel("Выберите формат архивации:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["ZIP", "7Z", "TAR"])

        self.archive_button = QPushButton("Архивировать")
        self.archive_button.clicked.connect(self.archive_selected_file)

        self.archive_label = QLabel("Выберите архив для разархивации:")
        self.archive_entry = QLineEdit()
        self.select_archive_button = QPushButton("Выбрать архив")
        self.select_archive_button.clicked.connect(self.select_archive)

        self.unarchive_button = QPushButton("Разархивировать")
        self.unarchive_button.clicked.connect(self.unarchive_selected_file)

        self.edit_label = QLabel("Редактировать архив:")
        self.edit_entry = QLineEdit()
        self.select_edit_button = QPushButton("Выбрать архив для редактирования")
        self.select_edit_button.clicked.connect(self.select_edit_archive)

        self.add_files_button = QPushButton("Добавить файлы")
        self.add_files_button.clicked.connect(self.add_files_to_archive)

        self.remove_files_button = QPushButton("Удалить файлы")
        self.remove_files_button.clicked.connect(self.remove_files_from_archive)

        self.exit_button = QPushButton("Выход")
        self.exit_button.clicked.connect(self.exit_program)

        layout = QVBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_entry)
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.format_label)
        layout.addWidget(self.format_combo)
        layout.addWidget(self.archive_button)
        layout.addWidget(self.archive_label)
        layout.addWidget(self.archive_entry)
        layout.addWidget(self.select_archive_button)
        layout.addWidget(self.unarchive_button)
        layout.addWidget(self.edit_label)
        layout.addWidget(self.edit_entry)
        layout.addWidget(self.select_edit_button)
        layout.addWidget(self.add_files_button)
        layout.addWidget(self.remove_files_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
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

    def archive_file(self, file_path, archive_format):
        if os.path.isfile(file_path):
            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            if archive_format == "ZIP":
                archive_path = os.path.join(directory, f"{filename}.zip")
                with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(file_path, arcname=filename)
            elif archive_format == "7Z":
                archive_path = os.path.join(directory, f"{filename}.7z")
                with SevenZipFile(archive_path, 'w') as szf:
                    szf.write(file_path)
            elif archive_format == "TAR":
                archive_path = os.path.join(directory, f"{filename}.tar")
                with tarfile.open(archive_path, 'w') as tar:
                    tar.add(file_path, arcname=filename)

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

    def edit_archive(self, archive_path, operation, files=[]):
        if os.path.isfile(archive_path):
            if archive_path.endswith(".zip"):
                with zipfile.ZipFile(archive_path, 'a') as zipf:
                    if operation == "add":
                        for file in files:
                            zipf.write(file, arcname=os.path.basename(file))
                    elif operation == "remove":
                        for file in files:
                            zipf.extract(file)

    def archive_selected_file(self):
        source_file = self.file_entry.text()
        if os.path.isfile(source_file):
            archive_format = self.format_combo.currentText()
            self.archive_file(source_file, archive_format)

    def unarchive_selected_file(self):
        archive_path = self.archive_entry.text()
        if os.path.isfile(archive_path):
            self.unarchive_file(archive_path)

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
