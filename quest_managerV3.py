import tkinter as tk
from tkinter import simpledialog, messagebox, Listbox, Scrollbar

class QuestModel:
    def __init__(self, title, description, due_date=None, priority=1, complete=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.complete = complete

    def __str__(self):
        status = "✓" if self.complete else "✗"
        return f"[{status}] (Priority: {self.priority}) {self.title}: {self.description}"

class QuestController:
    def __init__(self):
        self.quests = []

    def add_quest(self, quest):
        self.quests.append(quest)
        self.sort_quests()

    def edit_quest(self, index, title, description, priority):
        if 0 <= index < len(self.quests):
            self.quests[index].title = title
            self.quests[index].description = description
            self.quests[index].priority = priority
            self.sort_quests()

    def delete_quest(self, index):
        if 0 <= index < len(self.quests):
            return self.quests.pop(index)
        return None

    def mark_complete(self, index):
        if 0 <= index < len(self.quests):
            self.quests[index].complete = not self.quests[index].complete

    def sort_quests(self):
        self.quests.sort(key=lambda quest: quest.priority)

    def get_quests(self):
        return self.quests

class QuestView:
    def __init__(self, root, controller):
        self.controller = controller

        self.root = root
        self.root.title("Quest Manager")

        self.quest_listbox = Listbox(root, height=10, width=50)
        self.quest_listbox.pack(pady=10)

        scrollbar = Scrollbar(root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.quest_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.quest_listbox.yview)

        self.add_button = tk.Button(root, text="Add Quest", command=self.add_quest)
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(root, text="Edit Quest", command=self.edit_quest)
        self.edit_button.pack(pady=5)

        self.complete_button = tk.Button(root, text="Mark as Complete", command=self.mark_complete)
        self.complete_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Quest", command=self.delete_quest)
        self.delete_button.pack(pady=5)

        self.refresh_quests()

    def refresh_quests(self):
        self.quest_listbox.delete(0, tk.END)
        for quest in self.controller.get_quests():
            self.quest_listbox.insert(tk.END, quest)

    def add_quest(self):
        quest_title = simpledialog.askstring("Add Quest", "Enter the quest title:")
        quest_description = simpledialog.askstring("Add Quest", "Enter the quest description:")
        if quest_title and quest_description:
            priority = simpledialog.askinteger("Add Quest", "Enter the priority (integer):")
            if priority is not None:
                new_quest = QuestModel(quest_title, quest_description, priority=priority)
                self.controller.add_quest(new_quest)
                self.refresh_quests()
                messagebox.showinfo("Success", f"Quest '{quest_title}' added.")

    def edit_quest(self):
        selected_index = self.quest_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Edit Quest", "Please select a quest to edit.")
            return
        index = selected_index[0]
        current_quest = self.controller.get_quests()[index]
        new_title = simpledialog.askstring("Edit Quest", "Enter the new quest title:", initialvalue=current_quest.title)
        new_description = simpledialog.askstring("Edit Quest", "Enter the new quest description:", initialvalue=current_quest.description)
        new_priority = simpledialog.askinteger("Edit Quest", "Enter the new priority (integer):", initialvalue=current_quest.priority)
        if new_title and new_description and new_priority is not None:
            self.controller.edit_quest(index, new_title, new_description, new_priority)
            self.refresh_quests()
            messagebox.showinfo("Success", "Quest updated.")

    def mark_complete(self):
        selected_index = self.quest_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Mark as Complete", "Please select a quest to mark as complete.")
            return
        index = selected_index[0]
        self.controller.mark_complete(index)
        self.refresh_quests()
        messagebox.showinfo("Success", "Quest status updated.")

    def delete_quest(self):
        selected_index = self.quest_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Delete Quest", "Please select a quest to delete.")
            return
        index = selected_index[0]
        removed_quest = self.controller.delete_quest(index)
        if removed_quest:
            self.refresh_quests()
            messagebox.showinfo("Success", f"Quest '{removed_quest.title}' deleted.")

class QuestStart:
    def __init__(self, root):
        controller = QuestController()
        view = QuestView(root, controller)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuestStart(root)
    root.mainloop()
