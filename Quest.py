import tkinter as tk
from tkinter import simpledialog, messagebox, Listbox, Scrollbar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import *
from ttkbootstrap.tableview import *


class Quest:
    def __init__(self, description, priority=1, complete=False):
        self.description = description
        self.priority = priority
        self.complete = complete

    def __str__(self):
        status = "✓" if self.complete else "✗"
        return f"[{status}] (Priority: {self.priority}) {self.description}"


class QuestManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Quest Manager")

        # self.root.iconbitmap("1297208.png")
        # self.root.iconbitmap(default="1297208.png")

        self.quests = []

        self.quest_listbox = Listbox(root, height=10, width=50)
        self.quest_listbox.pack(pady=10)
        # self.quest_listbox = ttk.Treeview(root, column='Quest', bootstyle=PRIMARY)
        # self.quest_listbox.pack(pady=10)

        self.add_button = ttk.Button(
            root, text="Add Quest", command=self.add_quest, bootstyle=PRIMARY
        )
        self.add_button.pack(side=LEFT, padx=5, pady=5)

        self.edit_button = ttk.Button(
            root, text="Edit Quest", command=self.edit_quest, bootstyle=WARNING
        )
        self.edit_button.pack(side=LEFT, padx=5, pady=5)

        self.complete_button = ttk.Button(
            root, text="Complete Quest", command=self.mark_complete, bootstyle=SUCCESS
        )
        self.complete_button.pack(side=LEFT, padx=5, pady=5)

        self.delete_button = ttk.Button(
            root, text="Delete Quest", command=self.delete_quest, bootstyle=DANGER
        )
        self.delete_button.pack(side=LEFT, padx=5, pady=5)

        self.refresh_quests()

    def refresh_quests(self):
        self.quest_listbox.delete(0, ttk.END)
        for quest in self.quests:
            self.quest_listbox.insert(ttk.END, quest)

    def add_quest(self):
        quest_description = Querybox.get_string(
            "Add Quest", "Enter the quest description:"
        )
        if quest_description:
            priority = Querybox.get_integer(
                "Add Quest Priority integer 1-4", "Enter the priority (integer):"
            )
            if priority is not None:
                new_quest = Quest(quest_description, priority)
                self.quests.append(new_quest)
                self.sort_quests()
                self.refresh_quests()
                Messagebox.show_info("Success", f"Quest '{quest_description}' added.")

    def edit_quest(self):
        selected_index = self.quest_listbox.curselection()
        if not selected_index:
            Messagebox.show_warning("Edit Quest", "Please select a quest to edit.")
            return
        current_quest = self.quests[selected_index[0]]
        new_description = Querybox.get_string(
            "Edit Quest",
            "Enter the new quest description:",
            initialvalue=current_quest.description,
        )
        new_priority = Querybox.get_integer(
            "Edit Quest",
            "Enter the new priority (integer):",
            initialvalue=current_quest.priority,
        )
        if new_description and new_priority is not None:
            self.quests[selected_index[0]] = Quest(
                new_description, new_priority, current_quest.complete
            )
            self.sort_quests()
            self.refresh_quests()
            Messagebox.show_info("Success", "Quest updated.")

    def sort_quests(self):
        self.quests.sort(key=lambda quest: quest.priority)

    def mark_complete(self):
        selected_index = self.quest_listbox.curselection()
        if not selected_index:
            Messagebox.show_warning(
                "Mark as Complete", "Please select a quest to mark as complete."
            )
            return
        quest = self.quests[selected_index[0]]
        quest.complete = not quest.complete  # Toggle the complete status
        self.refresh_quests()
        Messagebox.show_info(
            "Success",
            f"Quest '{quest.description}' marked as {'complete' if quest.complete else 'incomplete'}.",
        )

    def delete_quest(self):
        selected_index = self.quest_listbox.curselection()
        if not selected_index:
            Messagebox.show_warning("Delete Quest", "Please select a quest to delete.")
            return
        removed_quest = self.quests.pop(selected_index[0])
        self.refresh_quests()
        Messagebox.show_info("Success", f"Quest '{removed_quest.description}' deleted.")


if __name__ == "__main__":

    root = ttk.Window(themename="darkly")
    app = QuestManager(root)
    root.mainloop()
