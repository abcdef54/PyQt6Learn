from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
                            QListWidget, QComboBox, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QKeyEvent, QPixmap, QPixmapCache, QImage, QResizeEvent
from PIL import Image, ImageFilter, ImageEnhance
from typing import List
import os
import sys

os.system('cls')

work_dir = ""

class ImgEditor(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.main_window_settings()
        self.initGUI()
        self.editor = Editor(self)
    
    
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

        for button in self.buttons:
            if button not in (self.select_button, self.filter_list):
                button.setEnabled(False)
    
    
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
            if item not in (self.img_box, self.file_list, self.filter_list):
                item.clicked.connect(self.buttons_clicked)
            
            elif item == self.file_list:
                item.itemClicked.connect(self.buttons_clicked)
                
            elif item == self.filter_list:
                self.filter_list.currentTextChanged.connect(self.buttons_clicked)
                

    def buttons_clicked(self) -> None:
        sender = self.sender()
        if not sender:
            return
        
        buttons = [self.left_button, self.right_button, self.mirror_button, self.grey_button,
                    self.sharp_button, self.blur_button, self.contrast_button]
        
        if sender in buttons:
            self.editor.transform_image(sender.text())
        
        elif sender == self.select_button:
            self.get_working_directory()
        
        elif sender == self.file_list:
            self.display_image()
            
        elif sender == self.filter_list:
            self.show_filter(self.filter_list.currentText())
    
    
    def get_working_directory(self) -> None:
        global work_dir
        selected_dir = QFileDialog().getExistingDirectory()
        
        if selected_dir:
            extendtions = ['.jpg', '.ico', '.svg', '.png']
            work_dir = selected_dir
            files = os.listdir(work_dir)
            files = self.filter_files_in_work_dir(files, extendtions)
            
            self.file_list.clear()
            for file in files:
                self.file_list.addItem(file)
            
    
    def filter_files_in_work_dir(self, files: List[str], extendtions: List[str]) -> None:
        result = []
        for file in files:
            for extendtion in extendtions:
                if file.endswith(extendtion):
                    result.append(file)
        return result


    def display_image(self) -> None:
        if self.file_list.currentRow() >= 0:
            file_name = self.file_list.currentItem().text()
            self.editor.load_image(file_name)
            self.editor.show_image()
            
            for button in self.buttons:
                if button not in (self.select_button, self.filter_list):
                    button.setEnabled(True)


    def show_filter(self, filter_name: str) -> None:
        if self.file_list.currentRow() >= 0:
            self.editor.preview_filter_change(filter_name)


    def keyPressEvent(self, key: QKeyEvent | None) -> None:
        if key.key() == Qt.Key.Key_Escape:
            self.close()


class Editor:
    def __init__(self, parent: ImgEditor) -> None:
        self.file_name = None
        self.file_path = None
        self.save_folder = "Edited/"
        self.image = None
        self.original = None
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
        self.original = self.image
    
    
    def load_edited_image(self) -> None:
        self.file_path = os.path.join(work_dir, self.save_folder, self.file_name)
        self.image = Image.open(self.file_path)
    
    
    def save_image(self) -> None:
        save_path = os.path.join(work_dir, self.save_folder)
        
        if not (os.path.exists(save_path) and os.path.isdir(save_path)):
            os.mkdir(save_path)
        
        image_full_path = os.path.join(save_path, self.file_name)
        self.image.save(image_full_path)
        
        
    def show_image(self, image_path: str = None) -> None:
        if not image_path:
            image_path = self.file_path
        
        self.parent.img_box.hide()
        QPixmapCache.clear()
        
        image = QPixmap(image_path)
        width = self.parent.img_box.width()
        height = self.parent.img_box.height()
        image = image.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
        
        self.parent.img_box.setPixmap(image)
        self.parent.img_box.show()
        
    
    def transform_image(self, transformation: str) -> None:
        transform_func = self.mapping.get(transformation)
        if transform_func:
            self.image = transform_func(self.image)
            self.show_edited_image()
            
    
    def preview_filter_change(self, filter_name: str) -> None:
        if filter_name == "Original":
            self.image = self.original.copy()
            self.show_image(os.path.join(work_dir, self.file_name))
        else:
            preview_func = self.mapping.get(filter_name) 
            if preview_func:
                self.parent.img_box.hide()
                
                preview_image = preview_func(self.image.copy())
                preview_pixmap = self.pil_to_qpixmap(preview_image)
                
                width = self.parent.img_box.width()
                height = self.parent.img_box.height()
                preview_pixmap = preview_pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
                
                self.parent.img_box.setPixmap(preview_pixmap)
                self.parent.img_box.show()
    
    
    def show_edited_image(self) -> None:
        self.save_image()
        self.load_edited_image()
        self.show_image()
        
        
    def pil_to_qpixmap(self, pil_image: Image) -> QPixmap:
        if pil_image.mode != "RGBA":
         pil_image = pil_image.convert("RGBA")
     
     # Get the raw data from the image and construct QImage from it
        data = pil_image.tobytes("raw", "RGBA")
        qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format.Format_RGBA8888)
        
        return QPixmap.fromImage(qimage)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    img = ImgEditor()
    img.show()
    sys.exit(app.exec())