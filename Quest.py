import tkinter as tk
from tkinter import simpledialog, messagebox
from ttkbootstrap import Style
from ttkbootstrap.widgets import Entry, Button, DateEntry

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quest.IO")
        self.root.geometry("500x500")
        self.root.resizable(False, False)  # Fixed window size

        # Apply ttkbootstrap style
        style = Style(theme="minty")
        self.root.config(bg="black")  # Set black background

        # Task list
        self.tasks = []

        # Padding for all widgets
        self.padding_x = 20  # Horizontal padding
        self.padding_y = 10  # Vertical padding

        # Create a frame for the scrollable area
        self.scrollable_frame = tk.Frame(self.root, bg="black")
        self.scrollable_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')  # Add to the grid

        # Create a canvas to hold the scrollable content
        self.canvas = tk.Canvas(self.scrollable_frame, bg="black")
        self.scrollable_content = tk.Frame(self.canvas, bg="black")
        self.scrollable_window = self.canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")

        # Create a scrollbar
        self.scrollbar = tk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Place the canvas and scrollbar in the frame
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Bind the configuration of the canvas to the scrollable content size
        self.scrollable_content.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create clickable button to add tasks
        self.create_btn = Button(self.root, text="Click to Create Task", bootstyle="primary", command=self.show_task_inputs)
        self.create_btn.grid(row=1, column=0, pady=self.padding_y, columnspan=2, sticky='nsew')  # Centered with spacing from top

        # Input fields (initially hidden)
        self.title_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.due_date_var = tk.StringVar()
        self.checklist_items = []  # Holds dynamic checklist items

        # Create input labels and entries
        self.title_label = tk.Label(self.scrollable_content, text="Title", bg="black", fg="white", font=("Helvetica", 10, "bold"))
        self.title_entry = Entry(self.scrollable_content, textvariable=self.title_var, width=40)

        self.description_label = tk.Label(self.scrollable_content, text="Description", bg="black", fg="white", font=("Helvetica", 10, "bold"))
        self.description_entry = Entry(self.scrollable_content, textvariable=self.description_var, width=40)

        self.due_date_label = tk.Label(self.scrollable_content, text="Due Date", bg="black", fg="white", font=("Helvetica", 10, "bold"))
        self.due_date_entry = DateEntry(self.scrollable_content, width=40)

        self.checklist_label = tk.Label(self.scrollable_content, text="Checklist", bg="black", fg="white", font=("Helvetica", 10, "bold"))
        self.add_checklist_btn = Button(self.scrollable_content, text="Add an item", bootstyle="secondary", command=self.add_checklist_item)

        self.checklist_frame = tk.Frame(self.scrollable_content, bg="black")

        self.add_btn = Button(self.scrollable_content, text="Add Task", command=self.add_task, bootstyle="success")

        # Listbox to display tasks
        self.task_listbox = tk.Listbox(self.root, height=10, width=50, selectmode=tk.SINGLE, bg="black", fg="white", font=("Helvetica", 10, "bold"))
        self.task_listbox.grid(row=2, column=0, columnspan=2, pady=self.padding_y, sticky='nsew')  # Centered and below the "Click to Create Task" button

        # Quit button
        self.quit_btn = Button(self.root, text="Quit", bootstyle="danger", command=self.quit_application)
        self.quit_btn.grid(row=3, column=0, columnspan=2, pady=self.padding_y, sticky='nsew')  # Positioned at the bottom

    def show_task_inputs(self):
        # Hide the create button
        self.create_btn.grid_remove()

        # Show the scrollable area for input fields
        self.scrollable_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')

        # Show input fields for title, description, due date, and checklist
        self.title_label.pack(pady=self.padding_y, anchor='w')
        self.title_entry.pack(pady=self.padding_y)

        self.description_label.pack(pady=self.padding_y, anchor='w')
        self.description_entry.pack(pady=self.padding_y)

        self.due_date_label.pack(pady=self.padding_y, anchor='w')
        self.due_date_entry.pack(pady=self.padding_y)

        self.checklist_label.pack(pady=self.padding_y, anchor='w')
        self.add_checklist_btn.pack(pady=self.padding_y)

        self.checklist_frame.pack(pady=self.padding_y, anchor='w')

        # Show the Add Task button
        self.add_btn.pack(pady=self.padding_y)

    def add_checklist_item(self):
        # Create a new entry for a checklist item
        checklist_var = tk.StringVar()
        checklist_entry = Entry(self.checklist_frame, textvariable=checklist_var, width=30)
        checklist_entry.pack(pady=2, anchor='w')  # Align items to the left
        self.checklist_items.append(checklist_var)  # Store the item for later retrieval

        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_task(self):
        title = self.title_var.get()
        description = self.description_var.get()
        due_date = self.due_date_entry.entry.get()  # Get the date as string
        checklist = [item.get() for item in self.checklist_items if item.get()]  # Retrieve checklist items

        if title and due_date:
            if hasattr(self, 'editing_task_index'):
                # If editing a task, update the selected task
                self.tasks[self.editing_task_index] = {"title": title, "description": description, "due_date": due_date, "checklist": checklist}
                del self.editing_task_index  # Remove the editing flag
            else:
                # Create task summary to add to Listbox
                self.tasks.append({"title": title, "description": description, "due_date": due_date, "checklist": checklist})

            self.update_task_listbox()

            # Clear inputs and reset form
            self.clear_inputs()
            self.hide_task_inputs()  # Hide the input fields after adding the task
            self.create_btn.grid(row=1, column=0, pady=20, columnspan=2, sticky='nsew')  # Show the "Create Task" button again
        else:
            messagebox.showwarning("Input Error", "Please enter a title and a due date")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task["title"])

    def clear_inputs(self):
        self.title_var.set("")
        self.description_var.set("")
        self.due_date_entry.entry.delete(0, tk.END)
        self.checklist_items.clear()  # Clear the stored checklist items
        for widget in self.checklist_frame.winfo_children():
            widget.destroy()  # Remove all checklist entries from the frame

        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def hide_task_inputs(self):
        # Hide all task input fields after task creation
        for widget in self.scrollable_content.winfo_children():
            widget.pack_forget()  # Hide all input widgets in the scrollable content

        # Hide the scrollable frame
        self.scrollable_frame.grid_remove()

    def show_task_options(self, event):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            selected_task = self.tasks[selected_index[0]]
            # Popup window to ask if user wants to view or edit the task
            action = messagebox.askquestion("Task Options", f"Do you want to view or edit the task: {selected_task['title']}?")
            if action == 'yes':
                # Fill the input fields with the selected task's details for editing
                self.fill_task_details(selected_task)
            else:
                # Show the task summary
                summary = self.format_task_summary(selected_task)
                messagebox.showinfo("Task Details", summary)

    def fill_task_details(self, task):
        # Fill the input fields with the selected task's details
        self.title_var.set(task["title"])
        self.description_var.set(task["description"])
        self.due_date_entry.set_date(task["due_date"])

        # Clear existing checklist items
        for widget in self.checklist_frame.winfo_children():
            widget.destroy()

        for item in task["checklist"]:
            checklist_var = tk.StringVar(value=item)
            checklist_entry = Entry(self.checklist_frame, textvariable=checklist_var, width=30)
            checklist_entry.pack(pady=2, anchor='w')
            self.checklist_items.append(checklist_var)  # Store the item for later retrieval

        # Show the scrollable area for editing
        self.show_task_inputs()

        # Set the editing index
        self.editing_task_index = self.tasks.index(task)

    def format_task_summary(self, task):
        # Format task details for display
        summary = f"Title: {task['title']}\nDescription: {task['description']}\nDue Date: {task['due_date']}\n\nChecklist:\n"
        if task["checklist"]:
            for item in task["checklist"]:
                summary += f"- {item}\n"
        else:
            summary += "No checklist items."
        return summary

    def quit_application(self):
        # Confirm if the user wants to quit the application
        if messagebox.askyesno("Quit", "Are you sure you want to quit the application?"):
            self.root.destroy()  # Close the application

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
