def display_quests(quests):
    if not quests:
        print("No quests available.")
    else:
        print("Quests:")
        for i, quest in enumerate(quests, start=1):
            print(f"{i}. {quest}")
def add_quest(quests):
    quest = input("Enter the quest: ")
    quests.append(quest)
    print(f"Quest '{quest}' added.")
def edit_quest(quests):
    display_quests(quests)
    try:
        quest_num = int(input("Enter the quest number to edit: "))
        if 1 <= quest_num <= len(quests):
            new_quest = input("Enter the new quest: ")
            quests[quest_num - 1] = new_quest
            print("Quest updated.")
        else:
            print("Invalid quest number.")
    except ValueError:
        print("Please enter a valid number.")
def delete_quest(quests):
    display_quests(quests)
    try:
        quest_num = int(input("Enter the quest number to delete: "))
        if 1 <= quest_num <= len(quests):
            removed_quest = quests.pop(quest_num - 1)
            print(f"Quest '{removed_quest}' deleted.")
        else:
            print("Invalid quest number.")
    except ValueError:
        print("Please enter a valid number.")
def main():
    quests = []
    while True:
        print("\nQuest Manager")
        print("1. Display Quests")
        print("2. Add Quest")
        print("3. Edit Quest")
        print("4. Delete Quest")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            display_quests(quests)
        elif choice == '2':
            add_quest(quests)
        elif choice == '3':
            edit_quest(quests)
        elif choice == '4':
            delete_quest(quests)
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()