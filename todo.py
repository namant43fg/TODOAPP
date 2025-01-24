import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QLabel, QComboBox, QProgressBar, QMessageBox, QDateEdit, QCheckBox
from PyQt5.QtCore import Qt, QDate, QTimer
from PyQt5.QtGui import QFont

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Super Beautiful To-Do List")
        self.setGeometry(300, 300, 600, 700)

        # Initialize dark mode
        self.is_dark_mode = False

        # Initialize tasks
        self.ongoing_tasks = {}
        self.finished_tasks = []

        # Load tasks from file if it exists
        self.load_tasks()

        self.initUI()

        # Initialize notification timer
        self.notification_timer = QTimer(self)
        self.notification_timer.timeout.connect(self.check_due_dates)
        self.notification_timer.start(60000)  # Check every minute

    def initUI(self):
        # Set main layout
        main_layout = QVBoxLayout()

        # Title Label
        self.title_label = QLabel("Your To-Do List")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        main_layout.addWidget(self.title_label)

        # Task Entry
        self.task_entry = QLineEdit(self)
        self.task_entry.setPlaceholderText("Enter your task")
        self.task_entry.setStyleSheet(self.get_input_style())
        main_layout.addWidget(self.task_entry)

        # Due Date Picker
        self.due_date_picker = QDateEdit(self)
        self.due_date_picker.setCalendarPopup(True)
        self.due_date_picker.setDate(QDate.currentDate())
        self.due_date_picker.setStyleSheet(self.get_input_style())
        main_layout.addWidget(self.due_date_picker)

        # Priority Selection
        self.priority_combobox = QComboBox(self)
        self.priority_combobox.addItems(["Low", "Medium", "High"])
        self.priority_combobox.setStyleSheet(self.get_input_style())
        main_layout.addWidget(self.priority_combobox)

        # Add Task Button
        add_task_button = QPushButton("Add Task", self)
        add_task_button.setStyleSheet(self.get_button_style())
        add_task_button.clicked.connect(self.add_task)
        main_layout.addWidget(add_task_button)

        # Date Filter Picker
        self.date_filter_picker = QDateEdit(self)
        self.date_filter_picker.setCalendarPopup(True)
        self.date_filter_picker.setDate(QDate.currentDate())
        self.date_filter_picker.setStyleSheet(self.get_input_style())
        self.date_filter_picker.dateChanged.connect(self.update_task_lists)
        main_layout.addWidget(self.date_filter_picker)

        # Ongoing Tasks List
        self.ongoing_tasks_list = QListWidget(self)
        self.ongoing_tasks_list.setStyleSheet(self.get_list_style())
        main_layout.addWidget(self.ongoing_tasks_list)

        # Finished Tasks List
        self.finished_tasks_list = QListWidget(self)
        self.finished_tasks_list.setStyleSheet(self.get_list_style())
        main_layout.addWidget(self.finished_tasks_list)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(self.get_progress_style())
        main_layout.addWidget(self.progress_bar)

        # Mark Done Button
        mark_done_button = QPushButton("Mark as Done", self)
        mark_done_button.setStyleSheet(self.get_button_style())
        mark_done_button.clicked.connect(self.mark_done)
        main_layout.addWidget(mark_done_button)

        # Hide Finished Tasks Checkbox
        self.hide_finished_checkbox = QCheckBox("Hide Finished Tasks", self)
        self.hide_finished_checkbox.stateChanged.connect(self.toggle_hide_finished)
        main_layout.addWidget(self.hide_finished_checkbox)

        # Set the layout for the window
        self.setLayout(main_layout)

    def get_input_style(self):
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

    def add_task(self):
        task = self.task_entry.text()
        due_date = self.due_date_picker.date().toString("yyyy-MM-dd")
        priority = self.priority_combobox.currentText()

        if task != "":
            self.ongoing_tasks[task] = {"due_date": due_date, "priority": priority}
            self.task_entry.clear()
            self.save_tasks()
            self.update_task_lists()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a task.")

    def update_task_lists(self):
        priority_map = {"Low": 1, "Medium": 2, "High": 3}
        self.ongoing_tasks_list.clear()

        # Get selected filter date
        selected_date = self.date_filter_picker.date().toString("yyyy-MM-dd")

        # Filter and display tasks for the selected date
        for task, details in sorted(self.ongoing_tasks.items(), key=lambda x: priority_map[x[1]["priority"]], reverse=True):
            if details["due_date"] == selected_date:
                task_display = f"{task} - Due: {details['due_date']} - Priority: {details['priority']}"
                self.ongoing_tasks_list.addItem(task_display)

        self.finished_tasks_list.clear()
        if not self.hide_finished_checkbox.isChecked():
            for task in self.finished_tasks:
                self.finished_tasks_list.addItem(task)

        self.update_progress()

    def update_progress(self):
        total_tasks = len(self.ongoing_tasks) + len(self.finished_tasks)
        if total_tasks == 0:
            self.progress_bar.setValue(0)
            return

        completed_tasks = len(self.finished_tasks)
        progress = (completed_tasks / total_tasks) * 100

        if progress < 50:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")
        elif progress < 80:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
        else:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")

        self.progress_bar.setValue(int(progress))

    def mark_done(self):
        selected_item = self.ongoing_tasks_list.currentItem()
        if selected_item:
            task_text = selected_item.text().split(" - ")[0]  # Extract task name
            if task_text in self.ongoing_tasks:
                self.finished_tasks.append(task_text)
                del self.ongoing_tasks[task_text]
                self.save_tasks()
                self.update_task_lists()
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a task to mark as done.")

    def toggle_hide_finished(self):
        self.update_task_lists()

    def check_due_dates(self):
        today = QDate.currentDate().toString("yyyy-MM-dd")
        overdue_tasks = [task for task, details in self.ongoing_tasks.items() if details["due_date"] < today]

        if overdue_tasks:
            QMessageBox.warning(self, "Overdue Tasks", f"You have overdue tasks: {', '.join(overdue_tasks)}")

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.ongoing_tasks, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = f.read()
                if data.strip():
                    self.ongoing_tasks = json.loads(data)
                else:
                    self.ongoing_tasks = {}
        except (FileNotFoundError, json.JSONDecodeError):
            self.ongoing_tasks = {}

# Main function to run the app
def main():
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
