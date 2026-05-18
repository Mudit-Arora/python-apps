from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QGridLayout, QWidget
import sys
from datetime import datetime

class AgeCalculator(QWidget): # parent method
    def __init__(self): # child method
        # in order to run both parent and child methods, we need to use super
        super().__init__() # function that return the parent of the class that has been called (QWidget)
        self.setWindowTitle("Age Calculator")
        grid = QGridLayout()
        
        # Create widgets
        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()

        date_birth_label = QLabel("Date of Birth MM/DD/YYYY:")
        self.name_birth_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate Age")
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel("")

        # Add widgets to the grid
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(date_birth_label, 1, 0)
        grid.addWidget(self.name_birth_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0, 1, 2) # 1 row, 2 columns
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        # Set the layout of the widget
        self.setLayout(grid)

    def calculate_age(self):
        current_year = datetime.now().year
        birth_year = datetime.strptime(self.name_birth_line_edit.text(), "%m/%d/%Y").date().year
        age = current_year - birth_year
        self.output_label.setText(f"{self.name_line_edit.text()} is {age} years old")


# Initialize the application
app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())