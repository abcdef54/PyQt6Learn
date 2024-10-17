from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QPushButton, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
import sys
import os
import math

os.system("cls")

class Calcu(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.set_main_window_settings()
        self.initGUI()
        
    
    
    def set_main_window_settings(self) -> None:
        self.setWindowTitle("Calculator v2.0")
        self.setWindowIcon(QIcon("Items/calculator_2374370.png"))
        self.setGeometry(600, 200, 400, 500)
    
    
    
    def create_variables(self) -> None:
        self.text_box = QLineEdit("0", self)
        self.text_box.setReadOnly(True)
    
    
    
    def initGUI(self) -> None:
        self.create_variables()
        self.create_buttons()
        self.set_style()
        self.set_layout()
    

    
    def set_layout(self) -> None:
        master_layout = QVBoxLayout()
        master_layout.addWidget(self.text_box)
        master_layout.addLayout(self.grid)
        master_layout.setContentsMargins(25,25,25,0)
        self.setLayout(master_layout)
        
        
        
    def set_style(self) -> None:
        self.setStyleSheet("""
                           QWidget{
                               background-color: #212121;
                           }
                           QLineEdit{
                               font-size: 28px;
                               padding: 15px;;
                               border-radius: 10px;
                               background-color: #c9c6c3;
                               color: #2e302e;
                           }
                           QPushButton{
                               padding: 10px;
                               font-size: 18px;
                               font-weight: bold;  
                               background-color: #ccc9c6;
                               color: #2e302e;
                           }
                           QPushButton:hover{
                               background-color: #d9d6d4;  
                           }
                           QPushButton:hover{
                               padding: 10px;
                               font-size: 18px;
                               font-weight: bold;
                               border-radius: 22px;
                           }
                           QPushButton#operator_buttons{
                               color: #d6d2c5;
                               background-color: #c49814;
                           }
                           QPushButton#operator_buttons:hover{
                               color: #d6d2c5;
                               background-color: #d4a313;
                           }
                           QPushButton#clear_button{
                               color: #d6d2c5;
                               background-color: #bd4209;
                           }
                           QPushButton#clear_button:hover{
                               color: #d6d2c5;
                               background-color: #b5350e;
                           }
                           """)
    
    
    
    def create_buttons(self) -> None:
        self.grid = QGridLayout()
        
        button_text = ['π','(',')','%','7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '+/-', '0', '.', '+']
        col = 0
        row = 0
        for text in button_text:
            button = QPushButton(text, self)
            self.grid.addWidget(button, row, col)
            self.grid.setSpacing(1)
            button.clicked.connect(self.button_clicked)
            if button.text() not in '0123456789π().':
                button.setObjectName("operator_buttons")
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        self.expand_button = QPushButton("Exp", self)
        self.clear_button = QPushButton("C", self)
        self.del_button = QPushButton("←", self)
        self.equal_button = QPushButton("=", self)
        
        custom_buttons = [self.expand_button, self.clear_button, self.del_button, self.equal_button]
        
        for button in custom_buttons:
            self.grid.addWidget(button, row, col)
            button.clicked.connect(self.button_clicked)
            if button.text() not in "C←":
                button.setObjectName("operator_buttons")
            if button.text() in "C←":
                button.setObjectName("clear_button")
            
            col += 1
            if col > 3:
                col = 0
                row += 1

    
    
    def button_clicked(self, in_sender_text: str = "") -> None:
        if not in_sender_text:
            sender = self.sender()
            if not sender:
                return
            sender_text = sender.text()
        else:
            sender_text = in_sender_text
        
        self.remove_error_text()
        
        if sender_text in '1234567890π()':
            self.handle_numeric(sender_text)
        
        elif sender_text in '+-*/%':
            self.handle_operators(sender_text)
        
        elif sender_text == '.':
            self.handle_period_symbol()
        
        elif sender_text == 'C':
            self._set_default_textbox()
        
        elif sender_text == '=':
            self.handle_equal_operator()
            
        elif sender_text == '←':
            self.handle_remove_operator()
            
        elif sender_text == '+/-':
            self.turn_first_number_negative()
        
        elif sender_text == 'Exp':
            # secret case:
            if self.text_box.text() == '42069':
                self.text_box.setText("Whatssup")
                return
            self.text_box.setText("Feature Not Implemented")
        
        return

    
    
    def handle_numeric(self, sender_text: str) -> None:
        if sender_text == '0' and self._text_box_is_default():
                return
        else:
            if self._text_box_is_default():
                self.text_box.setText(sender_text)
            else:
                self.text_box.setText(self.text_box.text() + sender_text)
    
    
    
    def handle_operators(self, sender_text: str) -> None:
        if self.text_box_is_empty():
                return
        elif self.text_box.text()[-1] == sender_text:
            return
        elif self.text_box.text()[-1] in '+-*/%':
            self.text_box.setText(self.text_box.text()[:-1] + sender_text)
        else:  
            self.text_box.setText(self.text_box.text() + sender_text)
    
    
    
    def handle_equal_operator(self) -> None:
        if self.text_box_is_empty() or self._text_box_is_default():
                return

        try:
            if self.text_box.text()[-1] in '+-*/%':
                text = self.text_box.text()[:-1]
            else:
                text = self.text_box.text()
            
            if not self._valid_parentheses(text):
                self.text_box.setText("Invalid Parentheses")
                return
            
            text = self.format_to_eval(text)
            result = eval(text)
                
            self.text_box.setText(f"{result:,}")
        
        except ZeroDivisionError:
            self.text_box.setText("ZeroDivisionError")
        except Exception:
            self.text_box.setText("Error")
    
    
    
    def handle_period_symbol(self) -> None:
        if self.text_box_is_empty():
                return
            
        if self.text_box.text()[-1] in '+-*/%.π()':
            return
        
        elif '.' not in self.text_box.text():
            self.text_box.setText(self.text_box.text() + '.')
        
        else:
            text = self.text_box.text()
            length = len(text)
            operator_found = False
            index = length - 1
            while index >= 0 and text[index] != '.':
                if text[index] in '+-*/%)':
                    operator_found = True
                index -= 1
                
            if not operator_found:
                return
            else:
                self.text_box.setText(self.text_box.text() + '.')
    
    
    
    def handle_remove_operator(self) -> None:
        if self._text_box_is_default():
                return
        elif self._text_box_has_one_value():
            self._set_default_textbox()
            return
        else:
            self.text_box.setText(self.text_box.text()[:-1])
            
            
            
    def turn_first_number_negative(self) -> None:
        if self.text_box_is_empty() or self._text_box_is_default():
                return
            
        else:
            if self.text_box.text()[0] != '-':
                self.text_box.setText('-' + self.text_box.text())
            else:
                self.text_box.setText(self.text_box.text()[1:])
    
    
    
    def remove_error_text(self) -> None:
        errors = ["ZeroDivisionError", "Feature Not Implemented", "Error", "Invalid Parentheses"]
        if self.text_box.text() in errors:
            self._set_default_textbox()
    
    
    
    def _valid_parentheses(self, text: str) -> bool:
        length = len(text)
        for index, char in enumerate(text):
            if index + 1 < length and char == '(':
                if text[index + 1] == ')':
                    return False
        
        open_parentheses = 0
        for char in text:
            if char == '(':
                open_parentheses += 1
            elif char == ')':
                open_parentheses -= 1
                if open_parentheses < 0:
                    return False
        
        return open_parentheses == 0
    
    
    
    def format_to_eval(self, text: str) -> str:
        formatted_text = self._format_pi(text)
        formatted_text = self._format_parentheses(formatted_text)
        formatted_text = formatted_text.replace(",","")
        return formatted_text
    
    
    
    def _format_parentheses(self, text: str) -> str:
        """
        Add '*' before '(' and after ')' if there is no operator
        """
        new_text = ""
        for index, char in enumerate(text):
            if char == '(':
                if index > 0 and text[index - 1] not in '+-*/%(':
                    new_text += '*('
                else:
                    new_text += '('
                    
            elif char == ')':
                if index < len(text) - 1 and  text[index + 1] not in '+-*/%)':
                    new_text += ')*'
                else:
                    new_text += ')'
            
            else:
                new_text += char
                
        return new_text
            
    
    
    def _format_pi(self, text: str) -> str:
        """
        Add '*' symbol before and/or after 'π' symbols if missing,
        and replace 'π' with its numerical value.
        """
        if 'π' not in text:
            return text
        
        pi = "3.141592"
        new_text = ""
        
        for index, symbol in enumerate(text):
            if symbol == 'π':
                before_pi_is_valid = (index == 0 or (index - 1 >= 0 and text[index - 1] in '+-*/%()'))
                after_pi_is_valid = (index + 1 >= len(text) or (index + 1 < len(text) and text[index + 1] in '+-*/%()π'))
                
                if before_pi_is_valid and after_pi_is_valid:
                    new_text += 'π'
                elif before_pi_is_valid:
                    new_text += 'π*'
                elif after_pi_is_valid:
                    new_text += '*π'
                else:
                    new_text += '*π*'
                    
            else:
                new_text += symbol
        
        return new_text.replace('π', pi)
    
    
    
    def text_box_is_empty(self) -> bool:
        """
        If there is nothing in the textbox (len() == 0)
        """
        return len(self.text_box.text()) == 0
    
    
    
    def _text_box_is_default(self) -> bool:
        """
        If the only value in textbox is 0 (default)
        """
        return len(self.text_box.text()) == 1 and self.text_box.text() == '0'
    
    
    
    def _text_box_has_one_value(self) -> bool:
        """
        If there is only one value in the textbox (not 0)
        """
        return len(self.text_box.text()) == 1
    
    
    
    def _set_default_textbox(self) -> None:
        """
        Set the textbox string to '0'
        """
        self.text_box.setText('0')
    
    
    
    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()

        elif event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.button_clicked(in_sender_text='=')

        elif event.key() == Qt.Key.Key_Backspace:
            self.button_clicked(in_sender_text='←')

        elif event.key() in (Qt.Key.Key_Plus, Qt.Key.Key_Minus, Qt.Key.Key_Asterisk, Qt.Key.Key_Slash, Qt.Key.Key_Percent):
            self.button_clicked(in_sender_text = chr(event.key()))
        
        elif event.key() in (Qt.Key.Key_0,
                             Qt.Key.Key_1,
                             Qt.Key.Key_2,
                             Qt.Key.Key_3,
                             Qt.Key.Key_4,
                             Qt.Key.Key_5,
                             Qt.Key.Key_6,
                             Qt.Key.Key_7,
                             Qt.Key.Key_8,
                             Qt.Key.Key_9):
            numeric_key_mapping = {
            Qt.Key.Key_0: '0',
            Qt.Key.Key_1: '1',
            Qt.Key.Key_2: '2',
            Qt.Key.Key_3: '3',
            Qt.Key.Key_4: '4',
            Qt.Key.Key_5: '5',
            Qt.Key.Key_6: '6',
            Qt.Key.Key_7: '7',
            Qt.Key.Key_8: '8',
            Qt.Key.Key_9: '9'
            }
            self.button_clicked(in_sender_text = numeric_key_mapping[event.key()])

        elif event.key() == Qt.Key.Key_Period:
            self.button_clicked(in_sender_text= '.')
            
        elif event.key() == Qt.Key.Key_C:
            self.button_clicked(in_sender_text= 'C')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cal = Calcu()
    cal.show()
    sys.exit(app.exec())