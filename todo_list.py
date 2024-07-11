import tkinter as tk
from tkinter import messagebox
import json
import os

# File to store tasks
TASK_FILE = 'tasks.json'

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        self.tasks = self.load_tasks()

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.frame, width=50, height=10, selectmode=tk.SINGLE)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.task_listbox.bind('<Double-1>', self.toggle_task_status)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(pady=10)

        self.task_entry = tk.Entry(self.entry_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5)

        self.priority_var = tk.StringVar(value="Normal")
  
        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.update_button = tk.Button(self.root, text="Update Task", command=self.update_task)
        self.update_button.pack(pady=5)

        self.refresh_tasks()

    def load_tasks(self):
        if os.path.exists(TASK_FILE):
            with open(TASK_FILE, 'r') as file:
                return json.load(file)
        return []

    def save_tasks(self):
        with open(TASK_FILE, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✔️" if task["completed"] else "❌"
            priority = f"({task['priority']})"
            self.task_listbox.insert(tk.END, f"{status} {task['task']} {priority}")

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_var.get()
        if task:
            self.tasks.append({"task": task, "priority": priority, "completed": False})
            self.save_tasks()
            self.task_entry.delete(0, tk.END)
            self.refresh_tasks()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks.pop(selected_task_index[0])
            self.save_tasks()
            self.refresh_tasks()
        else:
            messagebox.showwarning("Warning", "Please select a task to delete")

    def update_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            new_task = self.task_entry.get()
            new_priority = self.priority_var.get()
            if new_task:
                self.tasks[selected_task_index[0]]["task"] = new_task
                self.tasks[selected_task_index[0]]["priority"] = new_priority
                self.save_tasks()
                self.task_entry.delete(0, tk.END)
                self.refresh_tasks()
            else:
                messagebox.showwarning("Warning", "Task cannot be empty")
        else:
            messagebox.showwarning("Warning", "Please select a task to update")

    def toggle_task_status(self, event):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks[selected_task_index[0]]["completed"] = not self.tasks[selected_task_index[0]]["completed"]
            self.save_tasks()
            self.refresh_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
