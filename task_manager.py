import json
import os
import platform
from datetime import datetime
import pytz

class Task:
    def __init__(self, description, category, priority=1, completed=False, created_at=None):
        self.description = description
        self.category = category.lower()  # Store categories in lowercase
        self.priority = priority
        self.completed = completed
        self.created_at = created_at if created_at else datetime.now(pytz.timezone('Asia/Calcutta')).strftime('%d/%m/%y %H:%M:%S')

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
        self.total_tasks_added = len(self.tasks)  # Count of tasks added all time
        self.total_tasks_completed = sum(task.completed for task in self.tasks)  # Count of completed tasks

    def add_task(self, description, category, priority):
        task = Task(description, category, priority)
        self.tasks.append(task)
        self.total_tasks_added += 1  # Increment total tasks added
        self.save_tasks()
        print(f"Task added: {description} to {category} category with priority {priority}")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks for today!")
        else:
            print("\nToday's Tasks:")
            for i, task in enumerate(self.tasks, 1):
                print(f"{i}. {task}")
            print(f"\nTotal tasks added: {self.total_tasks_added}")
            print(f"Total tasks completed: {self.total_tasks_completed}")

    def view_pending_tasks(self):
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
        return list(set(task.category for task in self.tasks))

    def show_categories(self):
        categories = self.get_categories()
        if categories:
            print("\nExisting categories:")
            for index, category in enumerate(categories, 1):
                print(f"{index}. {category}")
        else:
            print("No categories available.")

    def select_category(self):
        self.show_categories()
        existing_categories = {cat.lower(): cat for cat in self.get_categories()}

        try:
            category_choice = int(input("Select a category by number (or enter 0 to create a new one): "))
            if category_choice == 0:
                new_category = input("Enter the new category name (in lowercase): ").lower()
                if new_category in existing_categories:
                    print(f"Category '{new_category}' already exists. Adding task to that category.")
                    return new_category
                return new_category
            elif 1 <= category_choice <= len(existing_categories):
                return existing_categories[list(existing_categories.keys())[category_choice - 1]]
            else:
                print("Invalid choice! Would you like to create a new category? (y/n): ")
                if input().lower() == 'y':
                    new_category = input("Enter the new category name (in lowercase): ").lower()
                    if new_category in existing_categories:
                        print(f"Category '{new_category}' already exists. Adding task to that category.")
                        return new_category
                    return new_category
                else:
                    return None
        except ValueError:
            print("Please enter a valid number.")
            return None

    def mark_task_completed(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1].mark_completed()
            self.total_tasks_completed += 1  # Increment total completed tasks
            self.save_tasks()
            print(f"Task {task_number} marked as completed.")
        else:
            print("Invalid task number!")

    def mark_pending_task_completed(self):
        pending_tasks = self.view_pending_tasks()
        if not pending_tasks:
            return  # No pending tasks to mark as completed

        try:
            task_number = int(input("Enter task number to mark as completed: "))
            if 0 < task_number <= len(pending_tasks):
                selected_task = pending_tasks[task_number - 1]
                self.tasks[self.tasks.index(selected_task)].mark_completed()
                self.total_tasks_completed += 1  # Increment total completed tasks
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
        with open(self.filename, 'w') as f:
            tasks_as_dict = [task.to_dict() for task in self.tasks]
            json.dump(tasks_as_dict, f, indent=4)
        print(f"Tasks saved to {self.filename}")

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                tasks_as_dict = json.load(f)
                self.tasks = [Task.from_dict(task) for task in tasks_as_dict]
            self.total_tasks_added = len(self.tasks)  # Update total tasks added on load
            self.total_tasks_completed = sum(task.completed for task in self.tasks)  # Update completed count
            print(f"Tasks loaded from {self.filename}")
        else:
            print("No existing tasks found, starting fresh.")