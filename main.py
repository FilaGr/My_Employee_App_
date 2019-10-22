from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
import sys
import sqlite3
from PIL import Image
import os

con = sqlite3.connect('employees.db')
cursor = con.cursor()
default_img = "person.png"
employee_id = None


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My employees")
        self.setGeometry(450, 150, 750, 600)
        self.ui()
        self.show()

    def ui(self):
        self.main_design()
        self.layouts()
        self.get_employees()
        self.display_first_record()

    def main_design(self):
        self.setStyleSheet("font-size: 14pt; font-family: Arial Bold;")
        self.employee_list = QListWidget()
        self.employee_list.itemClicked.connect(self.single_click)
        self.btn_new = QPushButton("New")
        self.btn_new.clicked.connect(self.add_employee)
        self.btn_update = QPushButton("Update")
        self.btn_update.clicked.connect(self.update_record)
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.clicked.connect(self.delete_employee)

    def layouts(self):
        # Layouts
        self.main_layout = QHBoxLayout()
        self.left_layout = QFormLayout()
        self.left_layout.setVerticalSpacing(20)
        self.right_main_layout = QVBoxLayout()
        self.right_top_layout = QVBoxLayout()
        self.right_bottom_layout = QHBoxLayout()

        # Adding child layouts to main layout
        self.right_main_layout.addLayout(self.right_top_layout)
        self.right_main_layout.addLayout(self.right_bottom_layout)
        self.main_layout.addLayout(self.left_layout, 40)
        self.main_layout.addLayout(self.right_main_layout, 60)

        # adding widgets to layouts
        self.right_top_layout.addWidget(self.employee_list)
        self.right_bottom_layout.addWidget(self.btn_new)
        self.right_bottom_layout.addWidget(self.btn_update)
        self.right_bottom_layout.addWidget(self.btn_delete)

        # setting main window layout
        self.setLayout(self.main_layout)

    def add_employee(self):
        self.new_employee = AddEmployee()
        self.close()

    def get_employees(self):
        query = "SELECT id, name, surname FROM employees"
        employees = cursor.execute(query).fetchall()
        for employee in employees:
            self.employee_list.addItem(str(employee[0]) + " - " + employee[1] + " " + employee[2])

    def display_record(self):
        pass

    def display_first_record(self):
        query = "SELECT * FROM employees ORDER BY ROWid ASC LIMIT 1"

        employee = cursor.execute(query).fetchone()
        # checks if there is any records in the query.
        if employee:
            img = QLabel()
            img.setPixmap(QPixmap("images/" + employee[5]))

            name = QLabel(employee[1])
            surname = QLabel(employee[2])
            phone = QLabel(employee[3])
            email = QLabel(employee[2])
            address = QLabel(employee[6])
            self.left_layout.addRow("", img)
            self.left_layout.addRow("Name: ", name)
            self.left_layout.addRow("Surname: ", surname)
            self.left_layout.addRow("Phone: ", phone)
            self.left_layout.addRow("Email: ", email)
            self.left_layout.addRow("Address: ", address)

    def single_click(self):
        for i in reversed(range(self.left_layout.count())):
            widget = self.left_layout.takeAt(i).widget()

            if widget is not None:
                widget.deleteLater()

        employee = self.employee_list.currentItem().text()
        id = employee.split("-")[0]
        query = "SELECT * FROM employees WHERE id=?"
        person = cursor.execute(query, (id, )).fetchone()
        img = QLabel()
        img.setPixmap(QPixmap("images/" + person[5]))

        name = QLabel(person[1])
        surname = QLabel(person[2])
        phone = QLabel(person[3])
        email = QLabel(person[2])
        address = QLabel(person[6])
        self.left_layout.addRow("", img)
        self.left_layout.addRow("Name: ", name)
        self.left_layout.addRow("Surname: ", surname)
        self.left_layout.addRow("Phone: ", phone)
        self.left_layout.addRow("Email: ", email)
        self.left_layout.addRow("Address: ", address)

    def refresh(self):
        self.close()
        self.main = Main()

    def delete_employee(self):
        if self.employee_list.selectedItems():

            employee = self.employee_list.currentItem().text()
            id = employee.split("-")[0]
            mbox = QMessageBox.question(self, "Warning", "Are you sure you want to delete this employee?",
                                        QMessageBox.Yes |
                                        QMessageBox.No, QMessageBox.No)
            if mbox == QMessageBox.Yes:
                try:
                    query = "DELETE FROM employees WHERE id=?"
                    cursor.execute(query, (id, ))
                    con.commit()
                    QMessageBox.information(self, "Information", "Employee was deleted")
                    self.refresh()
                except:
                    QMessageBox.information(self, "Warning", "Employee was not deleted")

    def update_record(self):
        global employee_id
        if self.employee_list.selectedItems():
            employee = self.employee_list.currentItem().text()
            employee_id = employee.split("-")[0]
            self.update_window = UpdateEmployee()
            self.close()
        else:
            QMessageBox.information(self, "Information", "please select an employee to update")


class UpdateEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Employee")
        self.setGeometry(450, 150, 450, 600)
        self.ui()
        self.show()

    def ui(self):
        self.get_employee_info()
        self.main_design()
        self.layouts()

    def closeEvent(self, event):
        self.main = Main()

    def get_employee_info(self):
        global employee_id
        query = "SELECT * FROM employees WHERE id=?"
        employee = cursor.execute(query, (employee_id, )).fetchone()
        self.name = employee[1]
        self.surname = employee[2]
        self.phone = employee[3]
        self.email = employee[4]
        self.image = employee[5]
        self.address = employee[6]

    def main_design(self):
        # top layout widgets
        self.setStyleSheet("background-color: white; font-size: 14pt; font-family: Times")
        self.title = QLabel("Employee")
        # line 72 if we wanted to add background color. use ; to separate properties
        # self.title.setStyleSheet('font-size: 24pt;font-family:Arial Bold; background-color: red')
        self.title.setStyleSheet('font-size: 24pt;font-family:Arial Bold')
        self.img_add = QLabel()
        self.img_add.setPixmap(QPixmap("images/{}".format(self.image)))

        # bottom layout widgets

        self.name_label = QLabel("Name : ")
        self.name_entry = QLineEdit()
        self.name_entry.setStyleSheet('font-size: 10pt')
        self.name_entry.setText(self.name)
        self.surname_label = QLabel("Surname : ")
        self.surname_entry = QLineEdit()
        self.surname_entry.setText(self.surname)
        self.surname_entry.setStyleSheet('font-size: 10pt')
        self.phone_label = QLabel("Phone : ")
        self.phone_entry = QLineEdit()
        self.phone_entry.setText(self.phone)
        self.phone_entry.setStyleSheet('font-size: 10pt')
        self.email_label = QLabel("Email : ")
        self.email_entry = QLineEdit()
        self.email_entry.setText(self.email)
        self.email_entry.setStyleSheet('font-size: 10pt')
        self.img_label = QLabel("Picture : ")
        self.img_btn = QPushButton("Browse")
        self.img_btn.setStyleSheet("background-color: orange; font-size: 10pt")
        self.img_btn.clicked.connect(self.upload_image)
        self.address_label = QLabel("Address : ")
        self.address_entry = QTextEdit()
        self.address_entry.setText(self.address)
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_employee)
        self.update_button.setStyleSheet("background-color: orange; font-size: 10pt")

    def layouts(self):
        # layouts
        self.main_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        self.bottom_layout = QFormLayout()

        # adding child layouts to main layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)

        # adding widgets to layouts

        # Top Layout
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.title)
        self.top_layout.addWidget(self.img_add)
        self.top_layout.addStretch()
        self.top_layout.setContentsMargins(110, 20, 10, 30)  # left, top, right, bottom

        # Bottom Layout
        self.bottom_layout.addRow(self.name_label, self.name_entry)
        self.bottom_layout.addRow(self.surname_label, self.surname_entry)
        self.bottom_layout.addRow(self.phone_label, self.phone_entry)
        self.bottom_layout.addRow(self.email_label, self.email_entry)
        self.bottom_layout.addRow(self.img_label, self.img_btn)
        self.bottom_layout.addRow(self.address_label, self.address_entry)
        self.bottom_layout.addRow('', self.update_button)

        # setting main layout for window
        self.setLayout(self.main_layout)

    def upload_image(self):
        global default_img
        self.size = (128, 128)
        self.file_name, ok = QFileDialog.getOpenFileName(self, 'Upload Image', '', 'Image Files (*.jpeg *.png)')

        if ok:

            default_img = os.path.basename(self.file_name)
            img = Image.open(self.file_name)
            img = img.resize(self.size)
            img.save("images/{}".format(default_img))

    def update_employee(self):
        global default_img
        global employee_id
        must_have_fields = ["Name", "Surname", "Phone"]
        name = self.name_entry.text()
        surname = self.surname_entry.text()
        phone = self.phone_entry.text()
        email = self.email_entry.text()
        img = default_img
        address = self.address_entry.toPlainText()
        if name and surname and phone != "":
            try:
                query = "UPDATE employees set name=?, surname=?, phone=?, email=?, image=?, address=? WHERE id=?"
                cursor.execute(query, (name, surname, phone, email, img, address, employee_id))
                con.commit()
                QMessageBox.information(self, "Success", "Employee has been updated")
                self.close()
                self.main = Main()

            except:
                QMessageBox.information(self, "Warning", "Employee hasn't been updated. "
                                                         "Please check the fields and try again")
        else:
            if name != "":
                must_have_fields.pop(0)
            if surname != "":
                must_have_fields.pop(1)
            if phone != "":
                must_have_fields.pop(2)
            QMessageBox.information(self, "Warnings", "{} fields cannot be empty".format(must_have_fields))


class AddEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Employee")
        self.setGeometry(450, 150, 450, 600)
        self.ui()
        self.show()

    def ui(self):
        self.main_design()
        self.layouts()

    def closeEvent(self, event):
        self.main = Main()

    def main_design(self):
        # top layout widgets
        self.setStyleSheet("background-color: white; font-size: 14pt; font-family: Times")
        self.title = QLabel("Add Person")
        # line 72 if we wanted to add background color. use ; to separate properties
        # self.title.setStyleSheet('font-size: 24pt;font-family:Arial Bold; background-color: red')
        self.title.setStyleSheet('font-size: 24pt;font-family:Arial Bold')
        self.img_add = QLabel()
        self.img_add.setPixmap(QPixmap("icons/person.png"))

        # bottom layout widgets

        self.name_label = QLabel("Name : ")
        self.name_entry = QLineEdit()
        self.name_entry.setStyleSheet('font-size: 10pt')
        self.name_entry.setPlaceholderText("Enter Employee Name")
        self.surname_label = QLabel("Surname : ")
        self.surname_entry = QLineEdit()
        self.surname_entry.setStyleSheet('font-size: 10pt')
        self.surname_entry.setPlaceholderText("Enter Employee Surname")
        self.phone_label = QLabel("Phone : ")
        self.phone_entry = QLineEdit()
        self.phone_entry.setStyleSheet('font-size: 10pt')
        self.phone_entry.setPlaceholderText("Enter Employee Phone Number")
        self.email_label = QLabel("Email : ")
        self.email_entry = QLineEdit()
        self.email_entry.setStyleSheet('font-size: 10pt')
        self.email_entry.setPlaceholderText("Enter Employee Email")
        self.img_label = QLabel("Picture : ")
        self.img_btn = QPushButton("Browse")
        self.img_btn.setStyleSheet("background-color: orange; font-size: 10pt")
        self.img_btn.clicked.connect(self.upload_image)
        self.address_label = QLabel("Address : ")
        self.address_entry = QTextEdit()
        self.add_button = QPushButton("Add")
        self.add_button.setStyleSheet("background-color: orange; font-size: 10pt")
        self.add_button.clicked.connect(self.add_employee)

    def layouts(self):
        # layouts
        self.main_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        self.bottom_layout = QFormLayout()

        # adding child layouts to main layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)

        # adding widgets to layouts

        # Top Layout
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.title)
        self.top_layout.addWidget(self.img_add)
        self.top_layout.addStretch()
        self.top_layout.setContentsMargins(110, 20, 10, 30)  # left, top, right, bottom

        # Bottom Layout
        self.bottom_layout.addRow(self.name_label, self.name_entry)
        self.bottom_layout.addRow(self.surname_label, self.surname_entry)
        self.bottom_layout.addRow(self.phone_label, self.phone_entry)
        self.bottom_layout.addRow(self.email_label, self.email_entry)
        self.bottom_layout.addRow(self.img_label, self.img_btn)
        self.bottom_layout.addRow(self.address_label, self.address_entry)
        self.bottom_layout.addRow('', self.add_button)

        # setting main layout for window
        self.setLayout(self.main_layout)

    def upload_image(self):
        global default_img
        self.size = (128, 128)
        self.file_name, ok = QFileDialog.getOpenFileName(self, 'Upload Image', '', 'Image Files (*.jpeg *.png)')

        if ok:

            default_img = os.path.basename(self.file_name)
            img = Image.open(self.file_name)
            img = img.resize(self.size)
            img.save("images/{}".format(default_img))

    def add_employee(self):
        global default_img
        must_have_fields = ["Name", "Surname", "Phone"]
        name = self.name_entry.text()
        surname = self.surname_entry.text()
        phone = self.phone_entry.text()
        email = self.email_entry.text()
        img = default_img
        address = self.address_entry.toPlainText()
        if name and surname and phone != "":
            try:
                query = "INSERT INTO employees (name, surname, phone, email, image, address) VALUES(?, ?, ?, ?, ?, ?)"
                cursor.execute(query, (name, surname, phone, email, img, address))
                con.commit()
                QMessageBox.information(self, "Success", "Employee has been added")
                self.close()
                self.main = Main()

            except:
                QMessageBox.information(self, "Warning", "Employee hasn't been added. "
                                                         "Please check the fields and try again")
        else:
            if name != "":
                must_have_fields.pop(0)
            if surname != "":
                must_have_fields.pop(1)
            if phone != "":
                must_have_fields.pop(2)
            QMessageBox.information(self, "Warnings", "{} fields cannot be empty".format(must_have_fields))


def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
