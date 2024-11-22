import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import PhotoImage, Treeview
import json, datetime


class QuestModel:
    def __init__(self, title, description, due_date=None, priority=1, complete=False, category="General"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.complete = complete
        self.category = category

    def __str__(self):
        status = "Yes" if self.complete else "No"
        return f"[{status}] (Priority: {self.priority}) [{self.category}] {self.title}: {self.description}, Due: {self.due_date}"

    def to_dict(self):
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
        return QuestModel(
            title=data["title"],
            description=data["description"],
            due_date=data.get("due_date"),
            priority=data["priority"],
            complete=data["complete"],
            category=data["category"],
        )


class QuestController:
    def __init__(self):
        self.quests = []

    def add_quest(self, quest):
        if self.is_duplicate_priority(quest.priority):
            return False
        self.quests.append(quest)
        self.sort_quests()
        return True

    def edit_quest(self, index, title, description, priority, category, due_date):
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
        if 0 <= index < len(self.quests):
            return self.quests.pop(index)
        return None

    def mark_complete(self, index):
        if 0 <= index < len(self.quests):
            self.quests[index].complete = not self.quests[index].complete

    def sort_quests(self):
        self.quests.sort(key=lambda quest: (quest.category, quest.priority))

    def get_quests(self):
        return self.quests

    def save_quests(self, filename="quests.json"):
        with open(filename, "w") as file:
            quests_data = [quest.to_dict() for quest in self.quests]
            json.dump(quests_data, file)

    def load_quests(self, filename="quests.json"):
        try:
            with open(filename, "r") as file:
                quests_data = json.load(file)
                self.quests = [QuestModel.from_dict(data) for data in quests_data]
        except FileNotFoundError:
            pass

    def is_duplicate_priority(self, priority, exclude_index=None):
        for idx, quest in enumerate(self.quests):
            if idx != exclude_index and quest.priority == priority:
                return True
        return False
    
    def is_valid_date(self, date_str):
        try:
            datetime.datetime.strptime(date_str, "%m-%d-%Y")
            return True
        except ValueError:
            return False

    def is_valid_priority(self, priority):
        return priority is not None and priority >= 1


class QuestView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Quest Manager")

        # Set the window icon (use a .png image file for cross-platform compatibility)
        icon = PhotoImage(name='logo', file='shaqqqIcon.png')  # image file
        self.root.iconphoto(True, icon)

        self.main_frame = ttk.Frame(root)
        # self.main_frame.pack(fill='both', expand=True)
        self.main_frame.grid(row=0, column=0, sticky="nsew")  # Fill window
        self.root.grid_rowconfigure(0, weight=1)  # Make main frame responsive
        self.root.grid_columnconfigure(0, weight=1)

        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

        self.main_frame.grid_columnconfigure(0, weight=3)  # Left frame takes 3 parts
        self.main_frame.grid_columnconfigure(1, weight=1)  # Right frame takes 1 part
        self.main_frame.grid_rowconfigure(0, weight=1)  # Both frames grow vertically


        # # Create a frame to hold the Treeview and its scrollbar
        tree_frame = ttk.Frame(self.left_frame)

        self.tree = Treeview(self.left_frame, columns=("Title", "Priority", "Category", "Complete", "Description", "Due Date"), show="headings")
        self.tree.pack(pady=5, fill='both', expand=True)
        # Heading details
        self.tree.heading("Title", text="Title", anchor="w")
        self.tree.heading("Priority", text="Priority", anchor="w")
        self.tree.heading("Category", text="Category", anchor="w")
        self.tree.heading("Complete", text="Done?", anchor="w")
        self.tree.heading("Description", text="Description", anchor="w")
        self.tree.heading("Due Date", text="Due Date", anchor="w")
        # column details
        self.tree.column("Title", width=150, anchor="w")
        self.tree.column("Priority", width=60, anchor="w")
        self.tree.column("Category", width=100, anchor="w")
        self.tree.column("Complete", width=40, anchor="w")
        self.tree.column("Description", width=300, anchor="w")
        self.tree.column("Due Date", width=80, anchor="w")

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")  # Scrollbar on the right of Treeview

        # Link the Treeview to the scrollbar
        self.tree.configure(yscrollcommand=scrollbar.set)

        button_frame = ttk.Frame(self.left_frame)
        button_frame.pack(pady=5, fill='x')

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

        self.refresh_quests()

        self.quest_form_frame = ttk.Frame(self.right_frame)
        self.quest_form_frame.pack(fill="both", pady=5)

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

        self.selected_quest_index = None

        self.message_label = ttk.Label(self.right_frame, text="", bootstyle=INFO)
        self.message_label.pack(pady=5, fill="x")


    def refresh_quests(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for idx, quest in enumerate(self.controller.get_quests()):
            status = "Yes" if quest.complete else "No"
            self.tree.insert("", "end", iid=idx, values=(
                quest.title, quest.priority, quest.category, status, quest.description, quest.due_date
            ))

    def show_add_quest_fields(self):
        if self.title_entry is not None:
            return

        self.title_label = ttk.Label(self.quest_form_frame, text="Title:")
        self.title_label.pack(pady=3, padx=5)
        self.title_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.title_entry.pack(pady=3, padx=5)

        self.description_label = ttk.Label(self.quest_form_frame, text="Description:")
        self.description_label.pack(pady=3, padx=5)
        self.description_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.description_entry.pack(pady=3, padx=5)

        self.category_label = ttk.Label(self.quest_form_frame, text="Category:")
        self.category_label.pack(pady=3, padx=5)
        self.category_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.category_entry.insert(0, "General")
        self.category_entry.pack(pady=3, padx=5)

        self.priority_label = ttk.Label(self.quest_form_frame, text="Priority:")
        self.priority_label.pack(pady=3, padx=5)
        self.priority_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.priority_entry.pack(pady=3, padx=5)

        self.due_date_label = ttk.Label(self.quest_form_frame, text="Due Date (MM-DD-YYYY):")
        self.due_date_label.pack(pady=3, padx=5)
        self.due_date_entry = ttk.Entry(self.quest_form_frame, width=30)
        self.due_date_entry.pack(pady=3, padx=5)

        self.submit_button = ttk.Button(self.quest_form_frame, text="Add Quest", command=self.submit_add_quest, bootstyle=PRIMARY, width=12)
        self.submit_button.pack(side=LEFT, padx=3, pady=3)

        self.cancel_button = ttk.Button(self.quest_form_frame, text="Cancel", command=self.cancel_add_quest, bootstyle=SECONDARY, width=12)
        self.cancel_button.pack(side=LEFT, padx=3, pady=3)

    def submit_add_quest(self):
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

        if not self.controller.add_quest(QuestModel(title, description, due_date, priority, category=category)):
            self.show_message(f"Priority {priority} already exists. Please choose another priority.", "warning")
            return

        self.refresh_quests()
        self.cancel_add_quest()
        self.show_message(f"Quest '{title}' added.", "success")

    def show_message(self, message, style):
        self.message_label.config(text=message, bootstyle=style)
        self.root.after(3000, lambda: self.message_label.config(text=""))

    def cancel_add_quest(self):
        if self.title_entry:
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

        self.title_label = self.title_entry = self.description_label = self.description_entry = \
            self.category_label = self.category_entry = self.priority_label = self.priority_entry = \
            self.due_date_label = self.due_date_entry = self.submit_button = self.cancel_button = None

    def show_edit_quest_fields(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.show_message("Please select a quest to edit.", "warning")
            return

        self.selected_quest_index = int(selected_item[0])
        quest = self.controller.get_quests()[self.selected_quest_index]

        self.cancel_add_quest()

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
        self.due_date_entry = ttk.Entry(self.quest_form_frame, bootstyle=PRIMARY, width=30)
        self.due_date_entry.insert(0, quest.due_date)
        self.due_date_entry.pack(pady=3, padx=5)

        self.submit_button = ttk.Button(self.quest_form_frame, text="Save Changes", command=self.submit_edit_quest, bootstyle=PRIMARY, width=12)
        self.submit_button.pack(side=LEFT, padx=3, pady=3)

        self.cancel_button = ttk.Button(self.quest_form_frame, text="Cancel", command=self.cancel_edit_quest, bootstyle=SECONDARY, width=12)
        self.cancel_button.pack(side=LEFT, padx=3, pady=3)

    def submit_edit_quest(self):
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
        self.cancel_add_quest()
        self.selected_quest_index = None

    def mark_complete(self):
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
        self.controller.save_quests()
        self.show_message("Quests saved.", "success")
        self.cancel_add_quest()

    def load_quests(self):
        self.controller.load_quests()
        self.refresh_quests()
        self.show_message("Quests loaded.", "success")
        self.cancel_add_quest()


if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    controller = QuestController()
    view = QuestView(root, controller)
    root.mainloop()