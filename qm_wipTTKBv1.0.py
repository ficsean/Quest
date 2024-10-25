import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox, Scrollbar, Frame
from ttkbootstrap import Style
from ttkbootstrap.widgets import Treeview
import json


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
        return f"[{status}] (Priority: {self.priority}) [{self.category}] {self.title}: {self.description}"

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
        self.quests.append(quest)
        self.sort_quests()

    def edit_quest(self, index, title, description, priority, category):
        if 0 <= index < len(self.quests):
            self.quests[index].title = title
            self.quests[index].description = description
            self.quests[index].priority = priority
            self.quests[index].category = category
            self.sort_quests()

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

    def get_quests_by_category(self, category):
        return [quest for quest in self.quests if quest.category == category]

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
            messagebox.showwarning("Load Quests", "No saved quests found.")


class QuestView:
    def __init__(self, root, controller):
        self.controller = controller

        self.root = root
        self.root.title("Quest Manager")

        # Treeview widget for displaying quests
        self.tree = Treeview(root, columns=("Title", "Priority", "Category", "Complete", "Description"), show="headings")
        self.tree.heading("Title", text="Title", anchor="w")
        self.tree.heading("Priority", text="Priority", anchor="w")
        self.tree.heading("Category", text="Category", anchor="w")
        self.tree.heading("Complete", text="Done?", anchor="w")
        self.tree.heading("Description", text="Description", anchor="w")
        self.tree.column("Title", width=200, anchor="w")
        self.tree.column("Priority", width=75, anchor="w")
        self.tree.column("Category", width=150, anchor="w")
        self.tree.column("Complete", width=50, anchor="w")
        self.tree.column("Description", width=750, anchor="w")
        self.tree.pack(pady=10, fill='x')

        scrollbar = Scrollbar(root)
        scrollbar.pack(side=ttk.RIGHT, fill=ttk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        button_frame = Frame(root)
        button_frame.pack(pady=10)

        self.add_button = ttk.Button(
            button_frame, text="Add Quest", command=self.add_quest, bootstyle=PRIMARY
        )
        self.add_button.pack(side=ttk.LEFT, padx=5)

        self.edit_button = ttk.Button(
            button_frame, text="Edit Quest", command=self.edit_quest, bootstyle=WARNING
        )
        self.edit_button.pack(side=ttk.LEFT, padx=5)

        self.complete_button = ttk.Button(
            button_frame, text="Mark as Complete", command=self.mark_complete, bootstyle=SUCCESS
        )
        self.complete_button.pack(side=ttk.LEFT, padx=5)

        self.delete_button = ttk.Button(
            button_frame, text="Delete Quest", command=self.delete_quest, bootstyle=DANGER
        )
        self.delete_button.pack(side=ttk.LEFT, padx=5)

        self.category_button = ttk.Button(
            button_frame, text="Filter by Category", command=self.filter_by_category, bootstyle=INFO
        )
        self.category_button.pack(side=ttk.LEFT, padx=5)

        self.display_all_button = ttk.Button(
            button_frame, text="Display All Quests", command=self.display_all_quests, bootstyle=SECONDARY
        )
        self.display_all_button.pack(side=ttk.LEFT, padx=5)

        self.save_button = ttk.Button(
            button_frame, text="Save Quests", command=self.save_quests, bootstyle=SUCCESS
        )
        self.save_button.pack(side=ttk.LEFT, padx=5)

        self.load_button = ttk.Button(
            button_frame, text="Load Quests", command=self.load_quests, bootstyle=INFO
        )
        self.load_button.pack(side=ttk.LEFT, padx=5)

        self.refresh_quests()

    def refresh_quests(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for idx, quest in enumerate(self.controller.get_quests()):
            status = "Yes" if quest.complete else "No"
            self.tree.insert("", "end", iid=idx, values=(quest.title, quest.priority, quest.category, status, quest.description))

    def add_quest(self):
        quest_title = simpledialog.askstring("Add Quest", "Enter the quest title:")
        quest_description = simpledialog.askstring("Add Quest", "Enter the quest description:")
        quest_category = simpledialog.askstring(
            "Add Quest", "Enter the quest category:", initialvalue="General"
        )
        if quest_title and quest_description:
            priority = simpledialog.askinteger("Add Quest", "Enter the priority (integer):")
            if priority is not None:
                new_quest = QuestModel(
                    quest_title, quest_description, priority=priority, category=quest_category
                )
                self.controller.add_quest(new_quest)
                self.refresh_quests()
                messagebox.showinfo("Success", f"Quest '{quest_title}' added.")

    def edit_quest(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Edit Quest", "Please select a quest to edit.")
            return
        index = int(selected_item[0])
        current_quest = self.controller.get_quests()[index]
        new_title = simpledialog.askstring(
            "Edit Quest", "Enter the new quest title:", initialvalue=current_quest.title
        )
        new_description = simpledialog.askstring(
            "Edit Quest", "Enter the new quest description:", initialvalue=current_quest.description
        )
        new_priority = simpledialog.askinteger(
            "Edit Quest", "Enter the new priority (integer):", initialvalue=current_quest.priority
        )
        new_category = simpledialog.askstring(
            "Edit Quest", "Enter the new quest category:", initialvalue=current_quest.category
        )
        if new_title and new_description and new_priority is not None:
            self.controller.edit_quest(index, new_title, new_description, new_priority, new_category)
            self.refresh_quests()
            messagebox.showinfo("Success", "Quest updated.")

    def mark_complete(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Mark as Complete", "Please select a quest to mark as complete.")
            return
        index = int(selected_item[0])
        self.controller.mark_complete(index)
        self.refresh_quests()
        messagebox.showinfo("Success", "Quest status updated.")

    def delete_quest(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete Quest", "Please select a quest to delete.")
            return
        index = int(selected_item[0])
        removed_quest = self.controller.delete_quest(index)
        if removed_quest:
            self.refresh_quests()
            messagebox.showinfo("Success", f"Quest '{removed_quest.title}' deleted.")

    def filter_by_category(self):
        category = simpledialog.askstring("Filter Quests", "Enter the category to filter by:")
        if category:
            filtered_quests = self.controller.get_quests_by_category(category)
            for row in self.tree.get_children():
                self.tree.delete(row)
            for idx, quest in enumerate(filtered_quests):
                status = "Yes" if quest.complete else "No"
                self.tree.insert("", "end", iid=idx, values=(quest.title, quest.priority, quest.category, status, quest.description))

    def display_all_quests(self):
        self.refresh_quests()

    def save_quests(self):
        self.controller.save_quests()
        messagebox.showinfo("Success", "All quests have been saved successfully.")

    def load_quests(self):
        self.controller.load_quests()
        self.refresh_quests()
        messagebox.showinfo("Success", "Quests loaded successfully.")


class QuestStart:
    def __init__(self, root):
        controller = QuestController()
        view = QuestView(root, controller)
        # Prompt user to add their first quest at the start
        view.add_quest()


if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = QuestStart(root)
    root.mainloop()
