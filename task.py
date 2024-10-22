# task.py
from datetime import datetime
import pytz

class Task:
    def __init__(self, description, category, priority=1, completed=False, created_at=None):
        self.description = description
        self.category = category.lower()  # Store categories in lowercase
        self.priority = priority
        self.completed = completed
        self.created_at = created_at if created_at else self.get_local_time()

    def get_local_time(self):
        """Return the current local time formatted as a string."""
        local_timezone = pytz.timezone('Asia/Calcutta')  # Replace with your local timezone, e.g., 'America/New_York'
        return datetime.now(local_timezone).strftime('%d/%m/%y %H:%M:%S')

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