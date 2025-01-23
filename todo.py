import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QLabel, QComboBox, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Super Beautiful To-Do List")
        self.setGeometry(300, 300, 600, 700)

        # Initialize dark mode
        self.is_dark_mode = False

        # Initialize tasks
        self.ongoing_tasks = {}
        self.finished_tasks = {}

        # Load tasks from file if it exists
        self.load_tasks()

        self.initUI()

    def initUI(self):
        # Set main layout
        main_layout = QVBoxLayout()

        # Title Label
        self.title_label = QLabel("Your To-Do List")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        main_layout.addWidget(self.title_label)

        # Task Entry
        self.task_entry = QLineEdit(self)
        self.task_entry.setPlaceholderText("Enter your task")
        self.task_entry.setStyleSheet(self.get_input_style())
        main_layout.addWidget(self.task_entry)

        # Category Selection
        self.category_combobox = QComboBox(self)
        self.category_combobox.addItems(["Work", "Personal", "High Priority"])
        self.category_combobox.setStyleSheet(self.get_input_style())
        main_layout.addWidget(self.category_combobox)

        # Add Task Button
        add_task_button = QPushButton("Add Task", self)
        add_task_button.setStyleSheet(self.get_button_style())
        add_task_button.clicked.connect(self.add_task)
        add_task_button.setToolTip("Click to add a task")
        main_layout.addWidget(add_task_button)

        # Ongoing Tasks List
        self.ongoing_tasks_list = QListWidget(self)
        self.ongoing_tasks_list.setStyleSheet(self.get_list_style())
        self.ongoing_tasks_list.setToolTip("Click on a task to select it")
        main_layout.addWidget(self.ongoing_tasks_list)

        # Finished Tasks List
        self.finished_tasks_list = QListWidget(self)
        self.finished_tasks_list.setStyleSheet(self.get_list_style())
        self.finished_tasks_list.setToolTip("Tasks that are finished")
        main_layout.addWidget(self.finished_tasks_list)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(self.get_progress_style())
        main_layout.addWidget(self.progress_bar)

        # Action Buttons (Mark Done, Remove)
        action_layout = QHBoxLayout()

        mark_done_button = QPushButton("Mark as Done", self)
        mark_done_button.clicked.connect(self.mark_done)
        mark_done_button.setStyleSheet(self.get_button_style())
        mark_done_button.setToolTip("Click to mark the selected task as done")
        action_layout.addWidget(mark_done_button)

        remove_button = QPushButton("Remove Task", self)
        remove_button.clicked.connect(self.remove_task)
        remove_button.setStyleSheet(self.get_button_style())
        remove_button.setToolTip("Click to remove the selected task")
        action_layout.addWidget(remove_button)

        main_layout.addLayout(action_layout)

        # Search Bar
        self.search_entry = QLineEdit(self)
        self.search_entry.setPlaceholderText("Search tasks")
        self.search_entry.setStyleSheet(self.get_input_style())
        self.search_entry.textChanged.connect(self.search_tasks)
        main_layout.addWidget(self.search_entry)

        # Sort Tasks Button
        sort_button = QPushButton("Sort Tasks", self)
        sort_button.clicked.connect(self.sort_tasks)
        sort_button.setStyleSheet(self.get_button_style())
        sort_button.setToolTip("Click to sort tasks alphabetically")
        main_layout.addWidget(sort_button)

        # Toggle Dark Mode Button
        toggle_theme_button = QPushButton("Toggle Dark Mode", self)
        toggle_theme_button.clicked.connect(self.toggle_theme)
        toggle_theme_button.setStyleSheet(self.get_button_style())
        toggle_theme_button.setToolTip("Click to toggle between dark and light modes")
        main_layout.addWidget(toggle_theme_button)

        # Set the layout for the window
        self.setLayout(main_layout)

    def get_input_style(self):
        """Returns the input field style for both light and dark mode"""
        if self.is_dark_mode:
            return """
                padding: 10px;
                font-size: 16px;
                border-radius: 10px;
                border: 1px solid #444;
                background-color: #333;
                color: white;
            """
        else:
            return """
                padding: 10px;
                font-size: 16px;
                border-radius: 10px;
                border: 1px solid #ccc;
                background-color: #f7f7f7;
                color: black;
            """

    def get_button_style(self):
        """Returns the button style for both light and dark mode"""
        if self.is_dark_mode:
            return """
                background-color: #2196F3;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 10px;
            """
        else:
            return """
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 10px;
            """

    def get_list_style(self):
        """Returns the style for the tasks list"""
        if self.is_dark_mode:
            return """
                font-size: 16px;
                background-color: #444;
                color: white;
                border-radius: 10px;
                padding: 10px;
            """
        else:
            return """
                font-size: 16px;
                background-color: #f7f7f7;
                color: black;
                border-radius: 10px;
                padding: 10px;
            """

    def get_progress_style(self):
        """Returns the progress bar style"""
        if self.is_dark_mode:
            return """
                border-radius: 10px;
                height: 20px;
                background-color: #666;
            """
        else:
            return """
                border-radius: 10px;
                height: 20px;
                background-color: #f7f7f7;
            """

    def toggle_theme(self):
        """Switches between dark and light modes"""
        self.is_dark_mode = not self.is_dark_mode
        self.update_ui()

    def update_ui(self):
        """Applies the current theme to the entire UI"""
        self.setStyleSheet(self.get_main_style())
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #4CAF50;" if not self.is_dark_mode else "font-size: 28px; font-weight: bold; color: #4CAF50;")

    def get_main_style(self):
        """Returns the main window style depending on the mode"""
        if self.is_dark_mode:
            return """
                background-color: #2E2E2E;
                color: white;
            """
        else:
            return """
                background-color: #f7f7f7;
                color: black;
            """

    def add_task(self):
        task = self.task_entry.text()
        category = self.category_combobox.currentText()

        if task != "":
            # Add the task to the ongoing tasks list
            self.ongoing_tasks[task] = category
            self.task_entry.clear()
            self.save_tasks()
            self.update_task_lists()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a task.")

    def mark_done(self):
        selected_task = self.ongoing_tasks_list.currentItem()

        if selected_task:
            task_text = selected_task.text().split(" - ")[0]  # Get task text from the format "task - category"
            
            if task_text in self.ongoing_tasks:
                # Move the task to the finished list
                category = self.ongoing_tasks.pop(task_text)
                self.finished_tasks[task_text] = category

                self.save_tasks()
                self.update_task_lists()
                self.update_progress()
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a task to mark as done.")

    def remove_task(self):
        selected_task = self.ongoing_tasks_list.currentItem()

        if selected_task:
            task_text = selected_task.text().split(" - ")[0]  # Get task text from the format "task - category"
            
            if task_text in self.ongoing_tasks:
                del self.ongoing_tasks[task_text]
                self.save_tasks()
                self.update_task_lists()
                self.update_progress()
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a task to remove.")

    def search_tasks(self):
        search_text = self.search_entry.text().lower()
        for i in range(self.ongoing_tasks_list.count()):
            item = self.ongoing_tasks_list.item(i)
            item.setHidden(search_text not in item.text().lower())

        for i in range(self.finished_tasks_list.count()):
            item = self.finished_tasks_list.item(i)
            item.setHidden(search_text not in item.text().lower())

    def sort_tasks(self):
        ongoing_task_list = [self.ongoing_tasks_list.item(i).text() for i in range(self.ongoing_tasks_list.count())]
        ongoing_task_list.sort()

        self.ongoing_tasks_list.clear()
        self.ongoing_tasks_list.addItems(ongoing_task_list)

    def update_progress(self):
        total_tasks = len(self.ongoing_tasks) + len(self.finished_tasks)
        if total_tasks == 0:
            self.progress_bar.setValue(0)
            return

        completed_tasks = len(self.finished_tasks)
        progress = (completed_tasks / total_tasks) * 100
        self.progress_bar.setValue(int(progress))

    def save_tasks(self):
        # Save both ongoing and finished tasks
        with open("tasks.json", "w") as f:
            json.dump({"ongoing_tasks": self.ongoing_tasks, "finished_tasks": self.finished_tasks}, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                self.ongoing_tasks = data.get("ongoing_tasks", {})
                self.finished_tasks = data.get("finished_tasks", {})
        except FileNotFoundError:
            self.ongoing_tasks = {}
            self.finished_tasks = {}

    def update_task_lists(self):
        self.ongoing_tasks_list.clear()
        for task, category in self.ongoing_tasks.items():
            self.ongoing_tasks_list.addItem(f"{task} - {category}")

        self.finished_tasks_list.clear()
        for task, category in self.finished_tasks.items():
            self.finished_tasks_list.addItem(f"{task} - {category}")

# Main function to run the app
def main():
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
