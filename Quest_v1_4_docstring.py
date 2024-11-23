import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import PhotoImage, Treeview
import json
import datetime

# Model class representing a single quest
class QuestModel:
    """
    Names of programmers that worked on this class: Sean, Arek, Michael, Jimmy
    Date of latest development: 11/14/2024
    
    Represents a quest with attributes like title, description, due date, priority, completion status, and category.
    """

    def __init__(self, title, description, due_date=None, priority=1, complete=False, category="General"):
        """
        Initialize a QuestModel instance.

        Args:
            title (str): The title of the quest.
            description (str): The description of the quest.
            due_date (str, optional): The due date of the quest in 'MM-DD-YYYY' format. Defaults to None.
            priority (int, optional): The priority of the quest (1 = highest priority). Defaults to 1.
            complete (bool, optional): Completion status of the quest. Defaults to False.
            category (str, optional): The category of the quest. Defaults to "General".
        """
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.complete = complete
        self.category = category

    def __str__(self):
        """
        Return a string representation of the quest.

        Returns:
            str: A formatted string representing the quest.
        """
        status = "Yes" if self.complete else "No"
        return f"[{status}] (Priority: {self.priority}) [{self.category}] {self.title}: {self.description}, Due: {self.due_date}"

    def to_dict(self):
        """
        Convert the quest attributes to a dictionary for JSON serialization.

        Returns:
            dict: A dictionary representation of the quest.
        """
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "complete": self.complete,
            "category": self.category,
        }

    @staticmethod
    def from_dict(data):
        """
        Create a QuestModel instance from a dictionary.

        Args:
            data (dict): A dictionary containing quest data.

        Returns:
            QuestModel: An instance of QuestModel populated with the dictionary data.
        """
        return QuestModel(
            title=data["title"],
            description=data["description"],
            due_date=data.get("due_date"),
            priority=data["priority"],
            complete=data["complete"],
            category=data["category"],
        )


class QuestController:
    """
    Names of programmers that worked on this class: Sean, Arek, Michael, Jimmy
    Date of latest development: 11/22/2024
    
    Controller class to manage a list of quests.
    """

    def __init__(self):
        """
        Initialize the QuestController with an empty quest list.
        """
        self.quests = []

    def add_quest(self, quest):
        """
        Add a quest to the list if its priority is unique.

        Args:
            quest (QuestModel): The quest to be added.

        Returns:
            bool: True if the quest was added successfully, False otherwise.
        """
        if self.is_duplicate_priority(quest.priority):
            return False
        self.quests.append(quest)
        self.sort_quests()
        return True

    def edit_quest(self, index, title, description, priority, category, due_date):
        """
        Edit an existing quest by index.

        Args:
            index (int): The index of the quest to edit.
            title (str): The updated title.
            description (str): The updated description.
            priority (int): The updated priority.
            category (str): The updated category.
            due_date (str): The updated due date.

        Returns:
            bool: True if the quest was successfully edited, False otherwise.
        """
        if 0 <= index < len(self.quests):
            if self.is_duplicate_priority(priority, exclude_index=index):
                return False
            self.quests[index].title = title
            self.quests[index].description = description
            self.quests[index].priority = priority
            self.quests[index].category = category
            self.quests[index].due_date = due_date
            self.sort_quests()
            return True
        return False

    def delete_quest(self, index):
        """
        Delete a quest by its index.

        Args:
            index (int): The index of the quest to delete.

        Returns:
            QuestModel or None: The deleted quest, or None if the index was invalid.
        """
        if 0 <= index < len(self.quests):
            return self.quests.pop(index)
        return None

    def mark_complete(self, index):
        """
        Toggle the completion status of a quest.

        Args:
            index (int): The index of the quest to toggle.
        """
        if 0 <= index < len(self.quests):
            self.quests[index].complete = not self.quests[index].complete

    def sort_quests(self):
        """
        Sort quests by category and priority.
        """
        self.quests.sort(key=lambda quest: (quest.category, quest.priority))

    def get_quests(self):
        """
        Retrieve the list of quests.

        Returns:
            list[QuestModel]: The list of quests.
        """
        return self.quests

    def save_quests(self, filename="quests.json"):
        """
        Save the quests to a JSON file.

        Args:
            filename (str, optional): The filename to save the quests to. Defaults to "quests.json".
        """
        with open(filename, "w") as file:
            quests_data = [quest.to_dict() for quest in self.quests]
            json.dump(quests_data, file)

    def load_quests(self, filename="quests.json"):
        """
        Load quests from a JSON file.

        Args:
            filename (str, optional): The filename to load quests from. Defaults to "quests.json".
        """
        try:
            with open(filename, "r") as file:
                quests_data = json.load(file)
                self.quests = [QuestModel.from_dict(data) for data in quests_data]
        except FileNotFoundError:
            pass

    def is_duplicate_priority(self, priority, exclude_index=None):
        """
        Check if a priority is already used, optionally excluding a specific index.

        Args:
            priority (int): The priority to check.
            exclude_index (int, optional): The index to exclude from the check. Defaults to None.

        Returns:
            bool: True if the priority is duplicated, False otherwise.
        """
        for idx, quest in enumerate(self.quests):
            if idx != exclude_index and quest.priority == priority:
                return True
        return False

    def is_valid_date(self, date_str):
        """
        Validate a date string.

        Args:
            date_str (str): The date string to validate.

        Returns:
            bool: True if the date is valid, False otherwise.
        """
        try:
            datetime.datetime.strptime(date_str, "%m-%d-%Y")
            return True
        except ValueError:
            return False

    def is_valid_priority(self, priority):
        """
        Validate the priority value.

        Args:
            priority (int): The priority to validate.

        Returns:
            bool: True if the priority is valid, False otherwise.
        """
        return priority is not None and priority >= 1
class QuestView:
    """
    Names of programmers that worked on this class: Sean, Arek, Michael, Jimmy
    Date of latest development: 11/21/2024
    
    View class to handle the graphical user interface for the Quest Manager application.
    """

    def __init__(self, root, controller):
        """
        Initialize the QuestView with the root window and controller.

        Args:
            root (ttk.Window): The main application window.
            controller (QuestController): The controller to manage quests.
        """
        self.controller = controller
        self.root = root
        self.root.title("Quest Manager")

        # Set the window icon (use a .png image file for cross-platform compatibility)
        icon = PhotoImage(name='logo', file='shaqqqIcon.png')
        self.root.iconphoto(True, icon)

        # Create the main layout frames
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create left and right frames
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

        # Configure grid weights
        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=2)

        # Create and configure the Treeview
        self.tree = Treeview(
            self.left_frame,
            columns=("Title", "Priority", "Category", "Complete", "Description", "Due Date"),
            show="headings",
        )
        self.tree.pack(pady=5, fill='both', expand=True)

        # Set Treeview column headings
        self.tree.heading("Title", text="Title", anchor="w")
        self.tree.heading("Priority", text="Priority", anchor="w")
        self.tree.heading("Category", text="Category", anchor="w")
        self.tree.heading("Complete", text="Done?", anchor="w")
        self.tree.heading("Description", text="Description", anchor="w")
        self.tree.heading("Due Date", text="Due Date", anchor="w")

        # Configure column widths
        self.tree.column("Title", width=150, anchor="w")
        self.tree.column("Priority", width=60, anchor="w")
        self.tree.column("Category", width=100, anchor="w")
        self.tree.column("Complete", width=40, anchor="w")
        self.tree.column("Description", width=300, anchor="w")
        self.tree.column("Due Date", width=80, anchor="w")

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Frame for buttons below the Treeview
        button_frame = ttk.Frame(self.left_frame)
        button_frame.pack(pady=5, fill='x')

        # Create buttons for quest actions
        self.add_button = ttk.Button(
            button_frame, text="Add", command=self.show_add_quest_fields, bootstyle=PRIMARY, width=12
        )
        self.add_button.pack(side=LEFT, expand=True, padx=5, pady=5)

        self.edit_button = ttk.Button(
            button_frame, text="Edit", command=self.show_edit_quest_fields, bootstyle=WARNING, width=12
        )
        self.edit_button.pack(side=LEFT, expand=True, padx=5, pady=5)

        self.complete_button = ttk.Button(
            button_frame, text="Complete", command=self.mark_complete, bootstyle=SUCCESS, width=12
        )
        self.complete_button.pack(side=LEFT, expand=True, padx=5, pady=5)

        self.delete_button = ttk.Button(
            button_frame, text="Delete", command=self.delete_quest, bootstyle=DANGER, width=12
        )
        self.delete_button.pack(side=LEFT, expand=True, padx=5, pady=5)

        self.save_button = ttk.Button(
            button_frame, text="Save", command=self.save_quests, bootstyle=SUCCESS, width=12
        )
        self.save_button.pack(side=LEFT, expand=True, padx=5, pady=5)

        self.load_button = ttk.Button(
            button_frame, text="Load", command=self.load_quests, bootstyle=INFO, width=12
        )
        self.load_button.pack(side=LEFT, expand=True, padx=5, pady=5)

        # Frame for the form to add/edit quests
        self.quest_form_frame = ttk.Frame(self.right_frame)
        self.quest_form_frame.pack(fill="both", pady=5)

        # Initialize placeholders for form elements
        self.title_entry = None
        self.description_entry = None
        self.category_entry = None
        self.priority_entry = None
        self.due_date_entry = None
        self.cancel_button = None
        self.submit_button = None
        self.title_label = None
        self.description_label = None
        self.category_label = None
        self.priority_label = None
        self.due_date_label = None

        # Selected quest index for editing
        self.selected_quest_index = None

        # Label for displaying feedback messages
        self.message_label = ttk.Label(self.right_frame, text="", bootstyle=INFO)
        self.message_label.pack(pady=5, fill="x")

        # Populate the Treeview with quests
        self.refresh_quests()

    def refresh_quests(self):
        """
        Refresh the Treeview to display the current list of quests.
        """
        for row in self.tree.get_children():
            self.tree.delete(row)
        for idx, quest in enumerate(self.controller.get_quests()):
            status = "Yes" if quest.complete else "No"
            self.tree.insert("", "end", iid=idx, values=(
                quest.title, quest.priority, quest.category, status, quest.description, quest.due_date
            ))

    def show_add_quest_fields(self):
        """
        Display the form fields to add a new quest.
        Prevents multiple forms from being shown simultaneously.
        """

        if self.title_entry is not None:
            return

        # Add quest form elements here...

        # Create and display form fields for title
        self.title_label = ttk.Label(self.quest_form_frame, text="Title:")
        self.title_label.pack(pady=3, padx=5)
        self.title_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.title_entry.pack(pady=3, padx=5)

        # Create and display form fields for description
        self.description_label = ttk.Label(self.quest_form_frame, text="Description:")
        self.description_label.pack(pady=3, padx=5)
        self.description_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.description_entry.pack(pady=3, padx=5)

        # Create and display form fields for category
        self.category_label = ttk.Label(self.quest_form_frame, text="Category:")
        self.category_label.pack(pady=3, padx=5)
        self.category_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.category_entry.insert(0, "General")  # Default category
        self.category_entry.pack(pady=3, padx=5)

        # Create and display form fields for priority
        self.priority_label = ttk.Label(self.quest_form_frame, text="Priority:")
        self.priority_label.pack(pady=3, padx=5)
        self.priority_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.priority_entry.pack(pady=3, padx=5)

        # Create and display form fields for due date
        self.due_date_label = ttk.Label(self.quest_form_frame, text="Due Date (MM-DD-YYYY):")
        self.due_date_label.pack(pady=3, padx=5)
        self.due_date_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.due_date_entry.pack(pady=3, padx=5)

        # Add quest button
        self.submit_button = ttk.Button(
            self.quest_form_frame, text="Add Quest", command=self.submit_add_quest, bootstyle=PRIMARY, width=12
        )
        self.submit_button.pack(side=LEFT, padx=3, pady=3)

        # Cancel quest button
        self.cancel_button = ttk.Button(
            self.quest_form_frame, text="Cancel", command=self.cancel_add_quest, bootstyle=SECONDARY, width=12
        )
        self.cancel_button.pack(side=LEFT, padx=3, pady=3)

    def submit_add_quest(self):
        """
        Handle the submission of a new quest.
        Validates input fields, ensures proper format, and adds the quest via the controller.

        Displays appropriate messages for validation errors or success.
        """
        # Collect input values from the form
        title = self.title_entry.get()
        description = self.description_entry.get()
        category = self.category_entry.get()
        priority = self.priority_entry.get()
        due_date = self.due_date_entry.get()

        # Validate that all fields are filled
        if not title or not description or not priority or not due_date:
            self.show_message("All fields are required.", "warning")
            return

        try:
            # Convert priority to an integer
            priority = int(priority)
        except ValueError:
            self.show_message("Priority must be a valid integer.", "warning")
            return

        # Validate priority
        if not self.controller.is_valid_priority(priority):
            self.show_message("Priority must be an integer greater than or equal to 1.", "warning")
            return

        # Validate date format
        if not self.controller.is_valid_date(due_date):
            self.show_message("Please enter a valid date in the format MM-DD-YYYY.", "warning")
            return

        # Attempt to add the new quest
        if not self.controller.add_quest(QuestModel(title, description, due_date, priority, category=category)):
            self.show_message(f"Priority {priority} already exists. Please choose another priority.", "warning")
            return

        # Refresh the view and reset the form
        self.refresh_quests()
        self.cancel_add_quest()
        self.show_message(f"Quest '{title}' added.", "success")

    def cancel_add_quest(self):
        """
        Cancel the addition of a quest and clear the form fields.
        """
        if self.title_entry:
            # Destroy all form fields and labels
            self.title_label.destroy()
            self.title_entry.destroy()
            self.description_label.destroy()
            self.description_entry.destroy()
            self.category_label.destroy()
            self.category_entry.destroy()
            self.priority_label.destroy()
            self.priority_entry.destroy()
            self.due_date_label.destroy()
            self.due_date_entry.destroy()
            self.submit_button.destroy()
            self.cancel_button.destroy()

        # Reset form field references to None
        self.title_label = self.title_entry = self.description_label = self.description_entry = \
            self.category_label = self.category_entry = self.priority_label = self.priority_entry = \
            self.due_date_label = self.due_date_entry = self.submit_button = self.cancel_button = None

    def show_message(self, message, style):
        """
        Display a feedback message to the user.

        Args:
            message (str): The message to display.
            style (str): The style of the message (e.g., "info", "warning", "success").
        """
        self.message_label.config(text=message, bootstyle=style)
        self.root.after(3000, lambda: self.message_label.config(text=""))  # Automatically clear the message after 3 seconds

    def show_edit_quest_fields(self):
        """
        Display the form fields for editing a selected quest.
        Pre-fills the form with the data of the selected quest.
        """
        selected_item = self.tree.selection()  # Check if a quest is selected in the Treeview
        if not selected_item:
            self.show_message("Please select a quest to edit.", "warning")
            return

        # Get the index of the selected quest
        self.selected_quest_index = int(selected_item[0])
        quest = self.controller.get_quests()[self.selected_quest_index]

        # Clear any existing form fields
        self.cancel_add_quest()

        # Populate the form with the selected quest's data
        self.title_label = ttk.Label(self.quest_form_frame, text="Title:")
        self.title_label.pack(pady=3, padx=5)
        self.title_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.title_entry.insert(0, quest.title)
        self.title_entry.pack(pady=3, padx=5)

        self.description_label = ttk.Label(self.quest_form_frame, text="Description:")
        self.description_label.pack(pady=3, padx=5)
        self.description_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.description_entry.insert(0, quest.description)
        self.description_entry.pack(pady=3, padx=5)

        self.category_label = ttk.Label(self.quest_form_frame, text="Category:")
        self.category_label.pack(pady=3, padx=5)
        self.category_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.category_entry.insert(0, quest.category)
        self.category_entry.pack(pady=3, padx=5)

        self.priority_label = ttk.Label(self.quest_form_frame, text="Priority:")
        self.priority_label.pack(pady=3, padx=5)
        self.priority_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.priority_entry.insert(0, str(quest.priority))
        self.priority_entry.pack(pady=3, padx=5)

        self.due_date_label = ttk.Label(self.quest_form_frame, text="Due Date (MM-DD-YYYY):")
        self.due_date_label.pack(pady=3, padx=5)
        self.due_date_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.due_date_entry.insert(0, quest.due_date)
        self.due_date_entry.pack(pady=3, padx=5)

        self.submit_button = ttk.Button(
            self.quest_form_frame, text="Save Changes", command=self.submit_edit_quest, bootstyle=PRIMARY, width=12
        )
        self.submit_button.pack(side=LEFT, padx=3, pady=3)

        self.cancel_button = ttk.Button(
            self.quest_form_frame, text="Cancel", command=self.cancel_edit_quest, bootstyle=SECONDARY, width=12
        )
        self.cancel_button.pack(side=LEFT, padx=3, pady=3)

    def submit_edit_quest(self):
        """
        Handle the submission of edited quest data.
        Validates input fields, ensures proper format, and updates the quest via the controller.

        Displays appropriate messages for validation errors or success.
        """
        title = self.title_entry.get()
        description = self.description_entry.get()
        category = self.category_entry.get()
        priority = self.priority_entry.get()
        due_date = self.due_date_entry.get()

        if not title or not description or not priority or not due_date:
            self.show_message("All fields are required.", "warning")
            return

        try:
            priority = int(priority)
        except ValueError:
            self.show_message("Priority must be a valid integer.", "warning")
            return

        if not self.controller.is_valid_priority(priority):
            self.show_message("Priority must be an integer greater than or equal to 1.", "warning")
            return

        if not self.controller.is_valid_date(due_date):
            self.show_message("Please enter a valid date in the format MM-DD-YYYY.", "warning")
            return

        if not self.controller.edit_quest(self.selected_quest_index, title, description, priority, category, due_date):
            self.show_message(f"Priority {priority} already exists. Please choose another priority.", "warning")
            return

        self.refresh_quests()
        self.cancel_edit_quest()
        self.show_message("Quest updated.", "success")
    def cancel_edit_quest(self):
        """
        Cancel the editing of a quest and clear the form fields.
        Resets the selected quest index.
        """
        self.cancel_add_quest()
        self.selected_quest_index = None

    def mark_complete(self):
        """
        Toggle the completion status of the selected quest.
        Updates the quest's status and refreshes the Treeview.

        Displays a success message indicating the new status.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            self.show_message("Please select a quest to mark as complete.", "warning")
            return

        index = int(selected_item[0])
        quest = self.controller.get_quests()[index]
        if quest.complete:
            message = "Quest marked as incomplete."
        else:
            message = "Quest marked as complete."

        self.controller.mark_complete(index)
        self.refresh_quests()
        self.cancel_add_quest()
        self.show_message(message, "success")

    def delete_quest(self):
        """
        Delete the selected quest from the list.
        Updates the Treeview and displays a success message.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            self.show_message("Please select a quest to delete.", "warning")
            return

        index = int(selected_item[0])
        self.controller.delete_quest(index)
        self.refresh_quests()
        self.cancel_add_quest()
        self.show_message("Quest deleted.", "success")

    def save_quests(self):
        """
        Save all quests to a JSON file.
        Displays a success message upon saving.
        """
        self.controller.save_quests()
        self.show_message("Quests saved.", "success")
        self.cancel_add_quest()

    def load_quests(self):
        """
        Load quests from a JSON file.
        Updates the Treeview and displays a success message upon loading.
        """
        self.controller.load_quests()
        self.refresh_quests()
        self.show_message("Quests loaded.", "success")
        self.cancel_add_quest()

# Main entry point for the application
if __name__ == "__main__":
    root = ttk.Window(themename="darkly") # Create the root window with a dark theme
    controller = QuestController()  # Create the controller
    view = QuestView(root, controller) # Create the view and link it to the controller
    root.mainloop() # Start the main event loop