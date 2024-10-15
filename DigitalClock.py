from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont, QFontDatabase, QIcon
from PyQt6.QtCore import Qt, QTime, QTimer
import sys

class DigitalClock(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        self.MainWindowStyle()
        self.variables()
        self.initGUI()
        
    
    def variables(self) -> None:
        self.time_label = QLabel(self)
        self.timer = QTimer(self)
    
    
    def MainWindowStyle(self) -> None:
        self.setWindowIcon(QIcon("Items/clock_.png"))
        self.setWindowTitle("Digital Clock")
        self.setGeometry(400, 300, 600, 200)
        
    
    def initGUI(self) -> None:
        self.Time_Label()
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.time_label)
        self.setLayout(vbox)
        
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
    
    
    def Time_Label(self) -> None:
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("font-size: 150px; color: green;")
        self.time_label.setFont(DigitalClock_Font(font_size=150).Digital_Font)
    
    
    def update_time(self) -> None:
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.time_label.setText(current_time)
        

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()


class DigitalClock_Font:
    def __init__(self, font_size: int = 10) -> None:
        self._font_id = QFontDatabase.addApplicationFont("Items/digital-7/digital-7.ttf")
        self._font_family = QFontDatabase.applicationFontFamilies(self._font_id)[0]
        
        self.Digital_Font = QFont(self._font_family, font_size)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec())