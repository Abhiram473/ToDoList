import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
from PyQt5.QtGui import QIcon

class ToDoListApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("To-Do List App")
        self.setGeometry(400, 400, 700, 600)

        self.setWindowIcon(QIcon("ToDo_Icon.jpg"))

        self.initialize_ui()

    def initialize_ui(self):
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Enter the task To-Do")
        self.task_input.setFixedSize(700, 50)

        self.view_button = QPushButton("View To-Do List", self)
        self.view_button.clicked.connect(self.view_todo_list)
        self.view_button.setFixedSize(700, 50)

        self.add_button = QPushButton("Add Task", self)
        self.add_button.clicked.connect(self.add_task)
        self.add_button.setFixedSize(700, 50)

        self.mark_button = QPushButton("Mark Task as Completed", self)
        self.mark_button.clicked.connect(self.mark_completed)
        self.mark_button.setFixedSize(700, 50)

        self.delete_button = QPushButton("Delete Task", self)
        self.delete_button.clicked.connect(self.delete_task)
        self.delete_button.setFixedSize(700, 50)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setFixedSize(700, 50)

        self.todo_list = QListWidget(self)

        layout = QVBoxLayout()
        layout.addWidget(self.task_input)
        layout.addWidget(self.view_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.mark_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.exit_button)
        layout.addWidget(self.todo_list)

        self.setLayout(layout)

        style = """
            QWidget {
                background-color: #f2f2f2;
            }
            
            QLabel {
                font-size: 16px;
                color: #333;
            }
            
            QLineEdit, QListWidget {
                font-size: 14px;
                color: #555;
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            
            QPushButton {
                font-size: 16px;
                color: #fff;
                background-color: #007BFF;
                border: 1px solid #007BFF;
                border-radius: 5px;
                padding: 5px 10px;
            }
            
            QPushButton:hover {
                background-color: #0056b3;
            }
        """

        self.setStyleSheet(style)

    def view_todo_list(self):
        self.todo_list.clear()
        try:
            with open("todo.txt", "r") as file:
                tasks = file.readlines()
                if tasks:
                    for task in tasks:
                        self.todo_list.addItem(task.strip())
                else:
                    self.show_message("To-Do List is Empty.")
        except Exception as e:
            print("Error:", e)

    def add_task(self):
        task = self.task_input.text().strip()
        if task:
            try:
                with open("todo.txt", "a") as file:
                    file.write(task + "\n")
                self.show_message("Task Added Successfully.")
                self.task_input.clear()
            except Exception as e:
                print("Error:", e)
        else:
            self.show_message("Please Enter a Valid Task.")

    def mark_completed(self):
        selected_item = self.todo_list.currentItem()
        if selected_item:
            try:
                task_number = self.todo_list.row(selected_item)
                with open("todo.txt", "r") as file:
                    tasks = file.readlines()
                if 0 <= task_number < len(tasks):
                    completed_task = tasks.pop(task_number)
                    with open("todo.txt", "w") as file:
                        file.writelines(tasks)
                    with open("completed.txt", "a") as completed_file:
                        completed_file.write(completed_task)
                    self.show_message("Task Marked as Completed.")
                    self.view_todo_list()
                else:
                    self.show_message("Invalid Task Number.")
            except Exception as e:
                print("Error:", e)
        else:
            self.show_message("Please Select a Task to Mark as Completed.")

    def delete_task(self):
        selected_item = self.todo_list.currentItem()
        if selected_item:
            try:
                task_number = self.todo_list.row(selected_item)
                with open("todo.txt", "r") as file:
                    tasks = file.readlines()
                if 0 <= task_number < len(tasks):
                    deleted_task = tasks.pop(task_number)
                    with open("todo.txt", "w") as file:
                        file.writelines(tasks)
                    self.show_message("Task Deleted Successfully.")
                    self.view_todo_list()
                else:
                    self.show_message("Invalid Task Number.")
            except Exception as e:
                print("Error:", e)
        else:
            self.show_message("Please Select a Task to Delete.")

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec_()


def main():
    app = QApplication(sys.argv)
    todo_app = ToDoListApp()
    todo_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    if not os.path.exists("todo.txt"):
        with open("todo.txt", "w"):
            pass
    if not os.path.exists("completed.txt"):
        with open("completed.txt", "w"):
            pass
    main()
