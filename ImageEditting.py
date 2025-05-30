from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
                            QListWidget, QComboBox, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QKeyEvent, QPixmap, QPixmapCache
from PIL import Image, ImageFilter, ImageEnhance
from typing import List
import os
import sys

os.system('cls')

work_dir = ""

class ImgEditor(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.editor = Editor(self)
        self.main_window_settings()
        self.initGUI()
    
    
    def main_window_settings(self) -> None:
        self.setWindowTitle("IDApp v2")
        self.setWindowIcon(QIcon("Items\picture_12318467.png"))
        self.setGeometry(400, 150, 800, 600)
    
    
    def initGUI(self) -> None:
        self.create_all_app_variables()
        self.setup_combobox()
        self.set_layout()
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
    
    
    def connect_signals(self) -> None:        
        for item in self.all_variables:
            if item not in (self.img_box, self.filter_list, self.file_list):
                if item != self.select_button:
                    item.setEnabled(False)
                item.clicked.connect(self.buttons_clicked)
                
            elif item == self.file_list:
                item.itemClicked.connect(self.buttons_clicked)
                
            elif item == self.filter_list:
                item.currentIndexChanged.connect(self.buttons_clicked)
    
    
    def filter(self, file_names: List[str], extendtions: List[str]) -> List[str]:
        result = []
        for file_name in file_names:
            for extendtion in extendtions:
                if file_name.endswith(extendtion):
                    result.append(file_name)
        return result
        
    
    def get_work_dir(self) -> None:
        global work_dir
        selected_dir = QFileDialog().getExistingDirectory()
        
        if selected_dir:
            work_dir = selected_dir
            extendtions = ['.jpg', '.ico', '.svg', '.png']
            file_names = os.listdir(work_dir)
            image_files = self.filter(file_names, extendtions)
            
            self.file_list.clear()
            self.file_list.addItems(image_files)
            
    
    def display_image(self) -> None:
        if self.file_list.currentRow() >= 0:
            self.editor.load_image(self.file_list.currentItem().text())
            self.editor.show_image()
            
            for button in self.buttons:
                button.setEnabled(True)
            
    
    def buttons_clicked(self) -> None:
        sender = self.sender()
        if not sender:
            return
        
        if sender == self.select_button:
            self.get_work_dir()
        
        elif sender == self.file_list:
            self.display_image()
        
        elif sender == self.left_button:
            self.editor.transform_image("Left")
        
        elif sender == self.right_button:
            self.editor.transform_image("Right")
            
        elif sender == self.mirror_button:
            self.editor.transform_image("Mirror")
            
        elif sender == self.grey_button:
            self.editor.transform_image("Grey")
            
        elif sender == self.sharp_button:
            self.editor.transform_image("Sharpen")
            
        elif sender == self.blur_button:
            self.editor.transform_image("Blur")
            
        elif sender == self.contrast_button:
            self.editor.transform_image("Contrast")
            
        elif sender == self.filter_list:
            if self.file_list.currentRow() >= 0:
                self.editor.apply_filter(self.filter_list.currentText())
        
        else:
            return

    
    def keyPressEvent(self, key: QKeyEvent | None) -> None:
        if key.key() == Qt.Key.Key_Escape:
            self.close()


class Editor:
    def __init__(self, parent: ImgEditor) -> None:
        self.file_name = None
        self.file_path = None
        self.image = None
        self.original = None
        self.save_folder = "Edited/"
        self.parent = parent
        self.mapping = {
            "Left" : lambda image: image.transpose(Image.ROTATE_90),
            "Right" : lambda image: image.transpose(Image.ROTATE_270),
            "Mirror" : lambda image: image.transpose(Image.FLIP_LEFT_RIGHT),
            "Grey" : lambda image: image.convert("L"),
            "Sharpen" : lambda image: image.filter(ImageFilter.SHARPEN),
            "Blur" : lambda image: image.filter(ImageFilter.BLUR),
            "Contrast" : lambda image: ImageEnhance.Contrast(image).enhance(1.1)
        }
        
    
    def load_image(self, file_name: str) -> None:
        self.file_name = file_name
        self.file_path = os.path.join(work_dir, file_name)
        self.image = Image.open(self.file_path)
        self.image = self.image
        self.original = self.image
        
    
    def load_edited_image(self) -> None:
        self.file_path = os.path.join(work_dir, self.save_folder, self.file_name)
        self.image = Image.open(self.file_path)
        self.image = self.image


    def save_image(self) -> None:
        if not self._image_loaded():
            raise FileNotFoundError("Image Not Loaded")
        
        save_folder = os.path.join(work_dir, self.save_folder)
        
        if not (os.path.exists(save_folder) and os.path.isdir(save_folder)):
            os.mkdir(save_folder)
        
        full_path = os.path.join(save_folder, self.file_name)
        self.image.save(full_path)
        
    
    def show_image(self, path: str = None) -> None:
        if not self._image_loaded():
            raise FileNotFoundError("Image Not Loaded")
        
        if not path:
            path = self.file_path
        
        self.parent.img_box.hide()
        
        QPixmapCache.clear()
        image = QPixmap(path)
        width = self.parent.img_box.width()
        height = self.parent.img_box.height()
        image = image.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
        self.parent.img_box.setPixmap(image)
        self.parent.img_box.show()

    
    def transform_image(self, transfromation: str) -> None:
        transform_fuc = self.mapping.get(transfromation)
        if transform_fuc:
            self.image = transform_fuc(self.image)
            self.change_image_after_edited()
            
    
    def apply_filter(self, filter_name: str) -> None:
        if filter_name == "Original":
            self.image = self.original.copy()
        else:
            filter_func = self.mapping.get(filter_name)
            if filter_func:
                self.image = filter_func(self.original.copy())

        self.save_image()
        self.show_image(os.path.join(work_dir, self.save_folder, self.file_name))
    
    
    def _image_loaded(self) -> bool:
        if not self.image or not self.original or not self.file_path:
            return False
        
        return True
    
    
    def change_image_after_edited(self) -> None:
        self.save_image()
        self.load_edited_image()
        self.show_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    img = ImgEditor()
    img.show()
    sys.exit(app.exec())