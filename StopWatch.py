from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QTimer, QTime
import sys
import os

os.system("cls")

class StopWatch(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.MainWindowStyle()
        self.initGUI()
    
    
    def MainWindowStyle(self) -> None:
        self.setWindowIcon(QIcon("Items/clock_.png"))
        self.setWindowTitle("Stop Watch")
        self.setGeometry(500, 200, 500, 400)
    
    
    def Variables(self) -> None:
        self.time = QTime(0, 0, 0, 0)
        self.time_label = QLabel("00:00:00.00", self)
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.reset_button = QPushButton("Reset", self)
        self.timer = QTimer(self)
        
    
    
    def initGUI(self) -> None:
        self.Variables()
        self.init_mainlayout()
        self.init_mainstyle()
        
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.reset_button.clicked.connect(self.reset)
        self.timer.timeout.connect(self.update_time)
        
        self.stop_button.setDisabled(True)
        self.reset_button.setDisabled(True)
        
    def init_mainlayout(self) -> None:
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.time_label)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        hbox.addWidget(self.reset_button)
        
        vbox.addLayout(hbox)
        self.setLayout(vbox)
    
    
    def init_mainstyle(self) -> None:
        
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
                           QLabel, QPushButton {
                               font-family = calibri;
                               padding: 10px;
                           }
                           QLabel {
                               font-size: 90px;
                               font-weight: bold;
                               background-color: #4287f5;
                               border-radius: 10px;
                           }
                           QPushButton {
                               font-size: 50px;
                           }
                           """)
    
    
    def start(self) -> None:
        self.timer.start(10)
        self.start_button.setDisabled(True)
        self.stop_button.setDisabled(False)
        self.reset_button.setDisabled(False)
    
    def stop(self) -> None:
        self.timer.stop()
        self.start_button.setDisabled(False)
        self.stop_button.setDisabled(True)
        self.reset_button.setDisabled(False)
    
    
    def reset(self) -> None:
        self.timer.stop()
        self.time = QTime(0, 0, 0, 0)
        self.time_label.setText("00:00:00.00")
        self.start_button.setDisabled(False)
        self.stop_button.setDisabled(True)
        self.reset_button.setDisabled(True)
    
    
    def update_time(self) -> None:
        self.time = self.time.addMSecs(10)
        self.time_label.setText(self.format_time(self.time))
        
    
    def format_time(self, time: QTime) -> str:
        hours = time.hour()
        minutes = time.minute()
        seconds = time.second()
        milsec = time.msec() // 10
        
        return f"{hours:02}:{minutes:02}:{seconds:02}.{milsec:02}"
    
    
    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    stopwatch = StopWatch()
    stopwatch.show()
    sys.exit(app.exec())