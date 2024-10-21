from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
                            QListWidget, QComboBox, QFileDialog)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PIL import Image, ImageFilter, ImageEnhance
from typing import List
import os
import sys

os.system('cls')

work_dir = ""

class ImgEditor(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.editor = Editor()
        self.main_window_settings()
        self.initGUI()
    
    
    def main_window_settings(self) -> None:
        self.setWindowTitle("IDApp-v2")
        self.setWindowIcon(QIcon("Items\picture_12318467.png"))
        self.setGeometry(400, 150, 800, 600)
    
    
    def initGUI(self) -> None:
        self.create_all_app_variables()
        self.setup_combobox()
        self.set_layout()
        self.set_style()
        self.connect_signals()
    
    
    def create_all_app_variables(self) -> None:
        self.img_box = QLabel("Image Appear Here")
        self.img_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.select_button = QPushButton("Select Folder")
        self.file_list = QListWidget()
        
        self.filter_list = QComboBox()
        self.left_button = QPushButton("Left")
        self.right_button = QPushButton("Right")
        self.mirror_button = QPushButton("Mirror")
        self.grey_button = QPushButton("Grey")
        self.sharp_button = QPushButton("Sharpen")
        self.blur_button = QPushButton("Blur")
        self.contrast_button = QPushButton("Contrast")
        
        
        self.all_variables = [self.img_box, self.select_button, self.file_list, self.filter_list, self.left_button, self.right_button, self.mirror_button,
                              self.grey_button, self.sharp_button, self.blur_button, self.contrast_button]
        
        self.buttons = [self.select_button, self.filter_list, self.left_button, self.right_button, self.mirror_button,
                        self.grey_button, self.sharp_button, self.blur_button, self.contrast_button]
    
    
    def setup_combobox(self) -> None:
        self.filter_list.addItem("Original")
        for button in self.buttons:
            if button not in (self.select_button, self.filter_list):
                self.filter_list.addItem(button.text())
                

    def set_layout(self) -> None:
        master_layout = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()
        
        for item in self.all_variables:
            if item == self.img_box:
                col2.addWidget(item)
            else:
                col1.addWidget(item)
        
        master_layout.addLayout(col1, 20)
        master_layout.addLayout(col2, 80)
        
        self.setLayout(master_layout)


    def set_style(self) -> None:
        pass


    def connect_signals(self) -> None:
        self.select_button.clicked.connect(self.get_word_dir)
        self.file_list.itemClicked.connect(self.display_image)
    
    
    def display_image(self) -> None:
        if self.file_list.currentRow() >= 0:
            filename = self.file_list.currentItem().text()
            self.editor.load_image(filename)
            self.editor.show_image(os.path.join(work_dir, filename), self)
            
    
    def filter(self, files: List[str], extentions: List[str]):
        result = []
        for file in files:
            for extention in extentions:
                if file.endswith(extention):
                    result.append(file)
        return result
    
    
    def get_word_dir(self) -> None:
        global work_dir
        selected_dir = QFileDialog.getExistingDirectory()
        if selected_dir:
            work_dir = selected_dir
            extentions = ['.png', '.ico', '.jpg', '.svg']
            filenames = self.filter(os.listdir(work_dir), extentions)
            self.file_list.clear()
            for filename in filenames:
                self.file_list.addItem(filename)

class Editor:
    def __init__(self) -> None:
        self.image = None
        self.original = None
        self.file_name = None
        self.save_folder = "Edited/"
        
    
    def load_image(self, filename: str) -> None:
        self.file_name = filename
        full_name = os.path.join(work_dir, self.file_name)
        self.image = Image.open(full_name)
        self.original = self.image
    
    
    def save_image(self) -> None:
        path = os.path.join(work_dir, self.save_folder)
        if not (os.path.isdir(path) or os.path.exists(path)):
            os.mkdir(path)
            
        full_name = os.path.join(path, self.file_name)
        self.image.save(full_name)
    
    
    def show_image(self, path: str, parent: ImgEditor) -> None:
        parent.img_box.hide()
        image = QPixmap(path)
        width = parent.img_box.width()
        height = parent.img_box.height()
        image = image.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
        parent.img_box.setPixmap(image)
        parent.img_box.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    img = ImgEditor()
    img.show()
    sys.exit(app.exec())