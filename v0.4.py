import tkinter as tk
from tkinter import Listbox, Scrollbar, StringVar, Text, END
from ttkbootstrap import Style

class Quest:
    def __init__(self, root):
        # Initialize application with darkly themed style
        self.style = Style(theme='darkly')
        self.root = root
        self.root.title("Quest")  # Set window title
        self.quests = []  # List to store quest data
        self.createWidgets()  # Create UI widgets
        self.refreshQuests()  # Refresh quest display

    def createWidgets(self):
        # Create all UI components
        self.createSearch()     # Search bar for quests
        self.createListbox()    # Listbox to display quests
        self.createDetails()    # Label to display quest details
        self.createFrame()      # Frame for input fields
        self.createButtons()    # Buttons for add, update, delete
        self.createStatus()     # Status message display

    def createSearch(self):
        # Create search input for filtering quests by title
        tk.Label(self.root, text="Search Quest by Title").pack(pady=5)
        self.searchInput = tk.Entry(self.root)
        self.searchInput.pack(pady=5)
        self.searchInput.bind("<KeyRelease>", self.filterQuests)  # Bind for filtering
        self.searchInput.bind("<FocusIn>", self.clearDetails)      # Clear details when focusing on search

    def createListbox(self):
        # Create listbox for displaying quests
        tk.Label(self.root, text="Quest Display").pack(pady=5)
        self.questListbox = Listbox(self.root, height=10, width=40)
        self.questListbox.pack(pady=5)
        self.questListbox.bind('<<ListboxSelect>>', self.displayDetails)  # Display details on selection

        # Create and configure scrollbar for listbox
        scrollbar = Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.questListbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.questListbox.yview)

    def createDetails(self):
        # Create label to show details of selected quest
        self.questDetails = StringVar()  # StringVar for dynamic text updates
        tk.Label(self.root, textvariable=self.questDetails, wraplength=350, justify="left").pack(pady=5)

    def createFrame(self):
        # Create frame for input fields
        self.frameInput = tk.Frame(self.root)
        self.frameInput.pack(pady=5)

        # Input field for title
        tk.Label(self.frameInput, text="Quest Title").grid(row=0, column=0, padx=5, pady=2)
        self.titleInput = tk.Entry(self.frameInput, width=30)
        self.titleInput.grid(row=1, column=0, padx=5, pady=2)
        self.titleInput.bind("<FocusIn>", self.clearDetails)  # Clear details on focus

        # Input field for description
        tk.Label(self.frameInput, text="Quest Description").grid(row=2, column=0, padx=5, pady=2)
        self.descriptionInput = Text(self.frameInput, height=3, width=30)
        self.descriptionInput.grid(row=3, column=0, padx=5, pady=2)
        self.descriptionInput.bind("<FocusIn>", self.clearDetails)  # Clear details on focus

        # Input field for due date
        tk.Label(self.frameInput, text="Quest Due Date").grid(row=4, column=0, padx=5, pady=2)
        self.dueDateInput = tk.Entry(self.frameInput, width=30)
        self.dueDateInput.grid(row=5, column=0, padx=5, pady=2)
        self.dueDateInput.bind("<FocusIn>", self.clearDetails)  # Clear details on focus

    def createButtons(self):
        # Create buttons for adding, updating, and deleting quests
        buttons = [("Add Quest", self.addQuest), 
                   ("Update Quest", self.updateQuest), 
                   ("Delete Quest", self.deleteQuest)]
        for text, command in buttons:
            tk.Button(self.root, text=text, command=command).pack(pady=2)

    def createStatus(self):
        # Create status message area
        self.statusMessage = StringVar()
        tk.Label(self.root, textvariable=self.statusMessage, fg="blue").pack(pady=5)

    def refreshQuests(self):
        # Refresh listbox with current quest list
        self.questListbox.delete(0, END)
        for quest in self.quests:
            self.questListbox.insert(END, f"{quest['title']} (Due: {quest['dueDate']})")
        self.displayDetails(None)  # Clear details on refresh

    def filterQuests(self, event):
        # Filter quests based on search input
        query = self.searchInput.get().lower()
        self.questListbox.delete(0, END)  # Clear current list
        for quest in self.quests:
            if query in quest['title'].lower():  # Check if query matches quest title
                self.questListbox.insert(END, f"{quest['title']} (Due: {quest['dueDate']})")

    def displayDetails(self, event):
        # Display details of selected quest
        selectedIndex = self.questListbox.curselection()
        if selectedIndex:
            quest = self.getSelectedQuest(selectedIndex[0])  # Get selected quest
            details = f"Title: {quest['title']}\nDescription: {quest['description']}\nDue Date: {quest['dueDate']}"
            self.questDetails.set(details)  # Update details display

    def getSelectedQuest(self, index):
        # Retrieve quest object corresponding to selected index
        questTitle = self.questListbox.get(index).split(" (Due:")[0]  # Extract title
        for quest in self.quests:
            if quest['title'] == questTitle:  # Match title to find quest
                return quest
        return None

    def addQuest(self):
        # Add new quest to list
        self.clearDetails()  # Clear details area
        title, description, dueDate = self.getInputData()  # Get input data
        if self.validateInput(title, description, dueDate):  # Validate input
            self.quests.append({'title': title, 'description': description, 'dueDate': dueDate})  # Add quest
            self.refreshQuests()  # Refresh quest display
            self.setStatus(f"Quest '{title}' added.")  # Set status message
            self.clearInput()  # Clear input fields

    def updateQuest(self):
        # Update selected quest
        self.clearDetails()  # Clear details area
        selectedIndex = self.questListbox.curselection()  # Get selected index
        if not selectedIndex:
            self.setStatus("Please select a Quest to update.")  # Error if none selected
            return
        quest = self.getSelectedQuest(selectedIndex[0])  # Get selected quest
        title, description, dueDate = self.getInputData()  # Get input data
        if self.validateInput(title, description, dueDate):  # Validate input
            quest.update({'title': title, 'description': description, 'dueDate': dueDate})  # Update quest
            self.refreshQuests()  # Refresh quest display
            self.displayDetails(None)  # Clear details display
            self.setStatus("Quest updated.")  # Set status message
            self.clearInput()  # Clear input fields

    def deleteQuest(self):
        # Delete selected quest
        self.clearDetails()  # Clear details area
        selectedIndex = self.questListbox.curselection()  # Get selected index
        if not selectedIndex:
            self.setStatus("Please select a Quest to delete.")  # Error if none selected
            return
        quest = self.getSelectedQuest(selectedIndex[0])  # Get selected quest
        if quest:
            self.quests.remove(quest)  # Remove quest from list
            self.refreshQuests()  # Refresh quest display
            self.clearInput()  # Clear input fields
            self.setStatus(f"Quest '{quest['title']}' deleted.")  # Set status message
            self.clearDetails()  # Clear details display

    def clearDetails(self, event=None):
        # Clear quest details display
        self.questDetails.set("")  # Reset details StringVar

    def clearInput(self):
        # Clear all input fields
        self.titleInput.delete(0, END)
        self.descriptionInput.delete(1.0, END)
        self.dueDateInput.delete(0, END)
        self.searchInput.delete(0, END)  # Clear search input

    def setStatus(self, message):
        # Set status message
        self.statusMessage.set(message)
        self.clearStatusAfterDelay(3000)  # Clear message after delay

    def clearStatusAfterDelay(self, delay):
        # Clear status message after specified delay
        self.root.after(delay, lambda: self.statusMessage.set(""))

    def getInputData(self):
        # Get input data from fields
        title = self.titleInput.get().strip()
        description = self.descriptionInput.get(1.0, END).strip()
        dueDate = self.dueDateInput.get().strip()
        return title, description, dueDate

    def validateInput(self, title, description, dueDate):
        # Validate input fields are filled
        if not (title and description and dueDate):
            self.setStatus("Please fill in all fields.")  # Error message if fields are empty
            return False
        return True  # Return true if all fields are filled

if __name__ == "__main__":
    root = tk.Tk()  # Create main window
    app = Quest(root)  # Initiliaze Quest application
    root.mainloop()  # Start main loop