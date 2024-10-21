import json
import os
import platform
from datetime import datetime

class Task:
    def __init__(self, description, category, priority=1, completed=False, created_at=None):
        self.description = description
        self.category = category.lower()  # Store categories in lowercase
        self.priority = priority
        self.completed = completed
        self.created_at = created_at if created_at else datetime.now().strftime('%d/%m/%y %H:%M:%S')

    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            description=task_dict['description'],
            category=task_dict['category'],
            priority=task_dict['priority'],
            completed=task_dict['completed'],
            created_at=task_dict['created_at']
        )

    def __str__(self):
        return f"[{'X' if self.completed else ' '}] {self.description} ({self.category}) - Priority: {self.priority} - Added: {self.created_at}"


class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    def add_task(self, description, category, priority):
        task = Task(description, category, priority)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task added: {description} to {category} category with priority {priority}")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks for today!")
        else:
            print("\nToday's Tasks:")
            for i, task in enumerate(self.tasks, 1):
                print(f"{i}. {task}")

    def view_pending_tasks(self):
        """View tasks that are not completed."""
        pending_tasks = [task for task in self.tasks if not task.completed]
        if not pending_tasks:
            print("No pending tasks!")
        else:
            print("\nPending Tasks:")
            for i, task in enumerate(pending_tasks, 1):
                print(f"{i}. {task}")
        return pending_tasks

    def view_tasks_by_category(self, category):
        category = category.lower()  # Normalize the category for comparison
        tasks_in_category = [task for task in self.tasks if task.category == category]
        if not tasks_in_category:
            print(f"No tasks in the '{category}' category!")
        else:
            print(f"\nTasks in '{category}' category:")
            for i, task in enumerate(tasks_in_category, 1):
                print(f"{i}. {task}")

    def get_categories(self):
        """Get a unique set of categories from existing tasks."""
        return list(set(task.category for task in self.tasks))

    def show_categories(self):
        """Display all the existing categories."""
        categories = self.get_categories()
        if categories:
            print("\nExisting categories:")
            for index, category in enumerate(categories, 1):
                print(f"{index}. {category}")
        else:
            print("No categories available.")

    def select_category(self):
        """Allows user to select a category by number or create a new one."""
        self.show_categories()
        existing_categories = {cat.lower(): cat for cat in self.get_categories()}  # Store categories as lowercase keys

        try:
            category_choice = int(input("Select a category by number (or enter 0 to create a new one): "))
            if category_choice == 0:
                new_category = input("Enter the new category name (in lowercase): ").lower()
                if new_category in existing_categories:
                    print(f"Category '{new_category}' already exists. Please choose a different name.")
                    return None
                return new_category
            elif 1 <= category_choice <= len(existing_categories):
                return existing_categories[list(existing_categories.keys())[category_choice - 1]]
            else:
                print("Invalid choice! Would you like to create a new category? (y/n): ")
                if input().lower() == 'y':
                    new_category = input("Enter the new category name (in lowercase): ").lower()
                    if new_category in existing_categories:
                        print(f"Category '{new_category}' already exists. Please choose a different name.")
                        return None
                    return new_category
                else:
                    return None
        except ValueError:
            print("Please enter a valid number.")
            return None

    def mark_task_completed(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1].mark_completed()
            self.save_tasks()
            print(f"Task {task_number} marked as completed.")
        else:
            print("Invalid task number!")

    def mark_pending_task_completed(self):
        """Show pending tasks and allow the user to mark one as completed."""
        pending_tasks = self.view_pending_tasks()
        if not pending_tasks:
            return  # No pending tasks to mark as completed

        try:
            task_number = int(input("Enter task number to mark as completed: "))
            if 0 < task_number <= len(pending_tasks):
                # Mark the corresponding pending task as completed
                selected_task = pending_tasks[task_number - 1]
                self.tasks[self.tasks.index(selected_task)].mark_completed()
                self.save_tasks()
                print(f"Task '{selected_task.description}' marked as completed.")
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number.")

    def remove_completed_tasks(self):
        self.tasks = [task for task in self.tasks if not task.completed]
        self.save_tasks()
        print("All completed tasks removed!")

    def save_tasks(self):
        """Saves tasks to a JSON file."""
        try:
            with open(self.filename, 'w') as f:
                tasks_as_dict = [task.to_dict() for task in self.tasks]
                json.dump(tasks_as_dict, f, indent=4)
            print(f"Tasks saved to {self.filename}")
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def load_tasks(self):
        """Loads tasks from a JSON file, if it exists."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    tasks_as_dict = json.load(f)
                    self.tasks = [Task.from_dict(task) for task in tasks_as_dict]
                print(f"Tasks loaded from {self.filename}")
            except json.JSONDecodeError:
                print(f"Error reading {self.filename}: file is corrupted. Starting fresh.")
                self.tasks = []
            except Exception as e:
                print(f"Error loading tasks: {e}")
                self.tasks = []
        else:
            print("No existing tasks found, starting fresh.")

def clear_console():
    """Clear the console based on the operating system."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

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
        clear_console()  # Clear the console right after getting input

        if choice == '1':
            task_description = input("Enter task description: ")
            task_category = manager.select_category()  # Select category with options
            if task_category:
                try:
                    priority = int(input("Enter task priority (1-5): "))
                    if priority < 1 or priority > 5:
                        print("Invalid priority! Please enter a number between 1 and 5.")
                        continue
                except ValueError:
                    print("Invalid input! Please enter a number between 1 and 5.")
                    continue
                clear_console()  # Clear console after inputs
                manager.add_task(task_description, task_category, priority)
            else:
                clear_console()  # Clear console after invalid category
                print("Task not added due to invalid category selection.")
        elif choice == '2':
            clear_console()  # Clear console before viewing tasks
            manager.view_tasks()
        elif choice == '3':
            clear_console()  # Clear console before viewing category tasks
            category = input("Enter category to view: ").lower()  # Normalize input for category
            manager.view_tasks_by_category(category)
        elif choice == '4':
            clear_console()  # Clear console before marking task as completed
            manager.mark_pending_task_completed()
        elif choice == '5':
            clear_console()  # Clear console before removing completed tasks
            manager.remove_completed_tasks()
        elif choice == '6':
            clear_console()  # Clear console before showing categories
            manager.show_categories()  # Call the method to show categories
        elif choice == '7':
            print("Exiting task manager.")
            break
        else:
            clear_console()  # Clear console after invalid choice
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()