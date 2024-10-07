import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Querybox, Messagebox

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

        self.quests = []
        self.editing_index = None  # Initialize editing_index here

        # Using Treeview to replace Listbox for better styling compatibility with ttkbootstrap
        self.quest_listbox = ttk.Treeview(root, columns=("Quest", "Priority", "Complete"), show="headings", height=10)
        self.quest_listbox.heading("Quest", text="Quest")
        self.quest_listbox.heading("Priority", text="Priority")
        self.quest_listbox.heading("Complete", text="Complete")

        # Configure columns to fit within the common width
        self.quest_listbox.column("Quest", width=250)
        self.quest_listbox.column("Priority", width=100)
        self.quest_listbox.column("Complete", width=100)

        self.quest_listbox.pack(pady=10, padx=10, fill='x', expand=True)  # Expand Treeview to fill window width

        # Input fields for quest description
        ttk.Label(root, text="Quest Description:").pack(pady=5)
        self.description_entry = ttk.Entry(root, width=40)
        self.description_entry.pack(pady=5)

        # Input fields for quest priority
        ttk.Label(root, text="Priority (1-4):").pack(pady=5)
        self.priority_entry = ttk.Entry(root, width=40)
        self.priority_entry.pack(pady=5)

        # Warning label for displaying input errors
        self.warning_label = ttk.Label(root, text="", foreground="red")
        self.warning_label.pack(pady=5)

        # Add Button
        self.add_button = ttk.Button(
            root, text="Add Quest", command=self.add_quest, bootstyle=PRIMARY
        )
        self.add_button.pack(side=LEFT, padx=5, pady=5)
        
        # Edit Button
        self.edit_button = ttk.Button(
            root, text="Edit Quest", command=self.edit_quest, bootstyle=WARNING
        )
        self.edit_button.pack(side=LEFT, padx=5, pady=5)
        
        # Complete Quest Button
        self.complete_button = ttk.Button(
            root, text="Complete Quest", command=self.mark_complete, bootstyle=SUCCESS
        )
        self.complete_button.pack(side=LEFT, padx=5, pady=5)

        # Delete Button
        self.delete_button = ttk.Button(
            root, text="Delete Quest", command=self.delete_quest, bootstyle=DANGER
        )
        self.delete_button.pack(side=LEFT, padx=5, pady=5)

        self.refresh_quests()

    def refresh_quests(self):
        # Clear the Treeview
        for item in self.quest_listbox.get_children():
            self.quest_listbox.delete(item)

        # Add new items to the Treeview
        for quest in self.quests:
            complete_status = "✓" if quest.complete else "✗"
            self.quest_listbox.insert('', 'end', values=(quest.description, quest.priority, complete_status))

    def add_quest(self):
        # Clear any previous warning message
        self.warning_label.config(text="")

        # Get the input values
        quest_description = self.description_entry.get().strip()
        try:
            priority = int(self.priority_entry.get().strip())
            if not (1 <= priority <= 4):
                raise ValueError("Priority must be between 1 and 4.")
        except ValueError:
            self.warning_label.config(text="Please enter a Quest description and a priority (integer) between 1 and 4.")
            return

        if quest_description:
            new_quest = Quest(quest_description, priority)
            self.quests.append(new_quest)
            self.sort_quests()
            self.refresh_quests()
            # Clear input fields after adding the quest
            self.description_entry.delete(0, END)
            self.priority_entry.delete(0, END)
        else:
            self.warning_label.config(text="Please enter a quest description.")
        
    def edit_quest(self):
        selected_item = self.quest_listbox.selection()
        if not selected_item:
            self.warning_label.config(text="Please select a quest to edit.", foreground="red")
            return

        # Get the current quest based on the selected item
        self.editing_index = self.quest_listbox.index(selected_item[0])
        current_quest = self.quests[self.editing_index]

        # Fill the input fields with the current quest's data
        self.description_entry.delete(0, 'end')
        self.description_entry.insert(0, current_quest.description)

        self.priority_entry.delete(0, 'end')
        self.priority_entry.insert(0, str(current_quest.priority))

        # Hide the Add button and show the Save button
        self.add_button.pack_forget()
        self.complete_button.pack_forget()
        self.edit_button.pack_forget()
        self.delete_button.pack_forget()

        self.save_button = ttk.Button(
            self.root, text="Save Quest", command=self.save_quest, bootstyle=SUCCESS
        )
        self.save_button.pack(side=LEFT, padx=5, pady=5)

        self.cancel_button = ttk.Button(
            self.root, text="Cancel", command=self.cancel_edit, bootstyle=WARNING
        )
        self.cancel_button.pack(side=LEFT, padx=5, pady=5)

        # Optionally, reset the warning label
        self.warning_label.config(text="")


    
    def save_quest(self):
        new_description = self.description_entry.get()
        new_priority = self.priority_entry.get()

        if new_description and new_priority.isdigit():
            new_priority = int(new_priority)
            self.quests[self.editing_index] = Quest(
                new_description, new_priority, self.quests[self.editing_index].complete
            )
            self.sort_quests()
            self.refresh_quests()
            self.warning_label.config(text="Success. Quest updated.", foreground="green")
            new_description = self.description_entry.delete(0, 'end')
            new_priority = self.priority_entry.delete(0, 'end')
        else:
            self.warning_label.config(text="Invalid input. Please check your values.", foreground="red")

        # Optionally hide the save button after saving
        self.save_button.pack_forget()
        self.cancel_button.pack_forget()
        self.add_button.pack(side=LEFT, padx=5, pady=5)
        self.edit_button.pack(side=LEFT, padx=5, pady=5)
        self.complete_button.pack(side=LEFT, padx=5, pady=5)
        self.delete_button.pack(side=LEFT, padx=5, pady=5)

    def cancel_edit(self):
        # Clear the input fields
        self.description_entry.delete(0, 'end')
        self.priority_entry.delete(0, 'end')

        # Hide the save and cancel buttons and show the original buttons again
        self.save_button.pack_forget()
        self.cancel_button.pack_forget()
        self.add_button.pack(side=LEFT, padx=5, pady=5)
        self.edit_button.pack(side=LEFT, padx=5, pady=5)
        self.complete_button.pack(side=LEFT, padx=5, pady=5)
        self.delete_button.pack(side=LEFT, padx=5, pady=5)

        # Optionally, reset the warning label
        self.warning_label.config(text="")


    def sort_quests(self):
        self.quests.sort(key=lambda quest: quest.priority)

    def mark_complete(self):
        selected_item = self.quest_listbox.selection()
        if not selected_item:
            self.warning_label.config(text="Please select a quest to mark as complete.", foreground="red")
            return
        quest = self.quests[self.quest_listbox.index(selected_item[0])]
        quest.complete = not quest.complete  # Toggle the complete status
        self.refresh_quests()
        self.warning_label.config(text=f"Quest '{quest.description}' marked as {'complete' if quest.complete else 'incomplete'}.", foreground="green")

    def delete_quest(self):
        selected_item = self.quest_listbox.selection()
        if not selected_item:
            self.warning_label.config(text="Please select a quest to delete.", foreground="red")
            return
        removed_quest = self.quests.pop(self.quest_listbox.index(selected_item[0]))
        self.refresh_quests()
        self.warning_label.config(text=f"Quest '{removed_quest.description}' deleted.", foreground="green")

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = QuestManager(root)
    root.mainloop()
