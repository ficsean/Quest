This is only a preview/blueprint build of "Quest". NOT THE FINAL PRODUCT.
![1](https://github.com/user-attachments/assets/8d378b34-2207-46f7-adc5-2f8cfaa66b80)
![2](https://github.com/user-attachments/assets/427a3b87-c272-4e71-a66a-45b31bb606bf)
![3](https://github.com/user-attachments/assets/add8ae90-6fdc-4653-9050-94825c9a2e3a)
![4](https://github.com/user-attachments/assets/ac590e3a-fd73-46d0-a2ba-c75dbe2dab41)
![5](https://github.com/user-attachments/assets/bb05d922-8b42-443e-9cb3-872ad6fb16cb)
![6](https://github.com/user-attachments/assets/59e52a83-7f92-4d69-b323-e686cfd1006c)

Quest Hierarchy (Preview Expectations before developing the GUI)
=======================
Scene 1

When opening the application, I want it to show the title of the application saying "Quest.IO".

If never been used, it should ask if you would like to "Create a Task".

If used previously, show "Running" task with their title and date started on the List box.

If uses previously, show the search option to find a task you want to look/view/edit.

Functions:
-Task Creation Function = In-progress
-Listbox (Hold Previous Made Tasks)  = In-progress
-Search function  = In-progress
-Edit function (for click and edit or search and view/edit)  = In-progress
-Quit Function  = In-progress


=======================

Scene 2

Within "Create a Task", it will have Title of Task, Description that explains the task, Objectives/Side Missions to complete the task in-hand, and percentage meter for how close to completing Objectives/side missions (Checklist). Also, the possibility of deleting entire Objectives/Side Mission to add new set of Objectives/Side missions. Lastly, Finished editing task and official confirming the "Run" of a Task.

Functions:
-Title = Completed
-Description = Completed
-Checklist (Objectives/Side Missions) = In-progress
-Percentage Meter with Mark for Completion) = Not Implemented Yet
-Delete  = Not Implemented Yet
-Run Task = In-progress

=======================

Scene 3

This is similar to the first Scene, it will show running tasks and user is able to view/edit/delete a task.

Functions:
-Percentage by number shown right beside Task  = Not Implemented Yet
-List box (Tasks by Title) = In-progress
-Search Function (Allows for View/Edit/Delete similar to clicking the List box item) = Not Implemented Yet
-Quit Function = Completed  



==============================================

__Quest (Task Management Application) = CRUD App__
==============================================

Objectives for Project:  
- Problem Solving  
- Apply learned skills in
  - RAD and Object-Oriented Analysis,
  - Design and Implementation. 
- Implementation Skills (Programming)  
- GUI  
- Basic Software Engineering  
- Agile Development (Scrum)  
- Discuss application and user during presentation (towards the end)  

===============================================

Technologies being used:
- Python3
  - tkinter
  - ttkbootstrap
  - pyinstaller (to make it into an executable at the end)

===============================================

User Case Stories for why you should use the application:  

1. User Story: Creating a Task (Create, Read, Update, Delete)  
  
- As a user, I want to create new tasks with a title, description, and due date
So that I can organize and track my tasks efficiently.

2. User Story: Searching Tasks (Searching)

- As a user, I want to search my tasks
So that I can find and read my tasks as fast as possible.

3. User Story: Organizing Tasks into Categories (Sorting)  

- As a user, I want to categorize tasks into different lists or projects
So that I can keep related tasks together and better manage my workload.  

4. User Story: Marking Tasks as Completed (Condition)  

- As a user, I want to mark tasks as completed with a single action
So that I can easily keep track of my progress and maintain an updated task list.  

5. User Story: Setting Task Reminders (Condition)  

- As a user, I want to set reminders for tasks with specific dates and times
So that I can receive notifications and ensure that I don’t miss deadlines.  

6. (If, web-based) User Story: Collaborating on Shared Tasks (Permissions)  

- As a user, I want to share tasks and assign them to other users
So that I can collaborate with team members and manage group projects more effectively.  

Note: Our option for Database System, we can store information into a text file.  

Feature: (6 Option) User Customization  
