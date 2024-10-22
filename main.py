from task_manager import TaskManager

def main():
    manager = TaskManager()

    while True:
        print("\nOptions:")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Tasks by Category")
        print("4. Mark Task as Completed")
        print("5. Remove Completed Tasks")
        print("6. View All Existing Categories")
        print("7. Quit")

        choice = input("Choose an option: ")

        if choice == '1':
            task_description = input("Enter task description: ")
            task_category = manager.select_category()  # Select category with options
            if task_category:
                priority_input = input("Enter task priority (1-5) or press Enter for default (1): ")
                priority = 1  # Default priority
                if priority_input:
                    try:
                        priority = int(priority_input)
                        if priority < 1 or priority > 5:
                            print("Invalid priority! Please enter a number between 1 and 5.")
                            continue
                    except ValueError:
                        print("Invalid input! Using default priority (1).")
                manager.add_task(task_description, task_category, priority)
            else:
                print("Task not added due to invalid category selection.")
        elif choice == '2':
            manager.view_tasks()
        elif choice == '3':
            category = input("Enter category to view: ").lower()  # Normalize input for category
            manager.view_tasks_by_category(category)
        elif choice == '4':
            manager.mark_pending_task_completed()
        elif choice == '5':
            manager.remove_completed_tasks()
        elif choice == '6':
            manager.show_categories()  # Call the method to show categories
        elif choice == '7':
            print("Exiting task manager.")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()