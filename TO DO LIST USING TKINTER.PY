import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os

# ---------------- Task Class ----------------
class Task:
    def __init__(self, title, description, category, completed=False, important=False):
        self.title = title
        self.description = description
        self.category = category
        self.completed = completed
        self.important = important

    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "completed": self.completed,
            "important": self.important
        }

# ---------------- File Handling ----------------
FILE_NAME = "tasks.json"

def save_tasks(tasks):
    with open(FILE_NAME, 'w') as f:
        json.dump([task.to_dict() for task in tasks], f, indent=4)

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, 'r') as f:
        data = json.load(f)
        return [Task(**item) for item in data]

# ---------------- Tkinter GUI ----------------
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Personal To-Do List Application")
        self.root.geometry("850x550")
        self.root.config(bg="#f8f9fa")  # professional light theme

        self.tasks = load_tasks()

        # ---------------- Title ----------------
        title_label = tk.Label(root, text="Personal To-Do List ✅",
                               font=("Segoe UI", 20, "bold"),
                               bg="#f8f9fa", fg="#2c3e50")
        title_label.pack(pady=10)

        # ---------------- Filter Dropdown ----------------
        filter_frame = tk.Frame(root, bg="#f8f9fa")
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Filter by Category:", 
                 font=("Segoe UI", 12), bg="#f8f9fa").grid(row=0, column=0, padx=5)

        self.filter_var = tk.StringVar(value="All")
        self.filter_dropdown = ttk.Combobox(filter_frame, textvariable=self.filter_var, state="readonly",
                                            values=["All", "Work", "Personal", "Urgent"])
        self.filter_dropdown.grid(row=0, column=1, padx=5)
        self.filter_dropdown.bind("<<ComboboxSelected>>", lambda e: self.refresh_task_list())

        # ---------------- Listbox + Scrollbar ----------------
        list_frame = tk.Frame(root, bg="#f8f9fa")
        list_frame.pack(pady=10)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)

        self.task_listbox = tk.Listbox(list_frame, width=95, height=15,
                                       font=("Segoe UI", 12),
                                       yscrollcommand=scrollbar.set,
                                       selectbackground="#007bff", 
                                       selectforeground="white",
                                       bg="white", fg="black",
                                       borderwidth=2, relief="groove")
        self.task_listbox.grid(row=0, column=0)
        scrollbar.config(command=self.task_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # ---------------- Buttons ----------------
        button_frame = tk.Frame(root, bg="#f8f9fa")
        button_frame.pack(pady=15)

        button_style = {
            "font": ("Segoe UI", 11, "bold"),
            "width": 16,
            "height": 2,
            "bd": 0,
            "relief": "ridge"
        }

        tk.Button(button_frame, text="➕ Add Task", command=self.add_task,
                  bg="#28a745", fg="white", **button_style).grid(row=0, column=0, padx=8)
        tk.Button(button_frame, text="👁 View Details", command=self.view_task,
                  bg="#17a2b8", fg="white", **button_style).grid(row=0, column=1, padx=8)
        tk.Button(button_frame, text="✔ Mark Completed", command=self.mark_task_completed,
                  bg="#ffc107", fg="white", **button_style).grid(row=0, column=2, padx=8)
        tk.Button(button_frame, text="🗑 Delete Task", command=self.delete_task,
                  bg="#dc3545", fg="white", **button_style).grid(row=0, column=3, padx=8)
        tk.Button(button_frame, text="💾 Save & Exit", command=self.save_and_exit,
                  bg="#6f42c1", fg="white", **button_style).grid(row=0, column=4, padx=8)

        self.refresh_task_list()

    # ---------------- Functions ----------------
    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        filter_cat = self.filter_var.get()

        for i, task in enumerate(self.tasks, start=1):
            if filter_cat != "All" and task.category != filter_cat:
                continue
            status = "✔ Completed" if task.completed else "❌ Pending"
            important_marker = "⭐ " if task.important else ""
            display_text = f"{i}. {important_marker}{task.title} [{task.category}] - {status}"

            self.task_listbox.insert(tk.END, display_text)

            # Highlight Important Tasks
            if task.important:
                self.task_listbox.itemconfig(tk.END, {'fg': 'red', 'font': ('Segoe UI', 12, 'bold')})

    def add_task(self):
        title = simpledialog.askstring("Task Title", "Enter task title:")
        if not title:
            return
        description = simpledialog.askstring("Task Description", "Enter task description:")
        category = simpledialog.askstring("Task Category", "Enter task category (Work/Personal/Urgent):")
        important = messagebox.askyesno("Important Task", "Do you want to mark this task as Important?")

        self.tasks.append(Task(title, description, category, important=important))
        self.refresh_task_list()

    def view_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            task = self.tasks[index]
            messagebox.showinfo("📌 Task Details",
                                f"Title: {task.title}\n"
                                f"Description: {task.description}\n"
                                f"Category: {task.category}\n"
                                f"Important: {'Yes ⭐' if task.important else 'No'}\n"
                                f"Status: {'Completed' if task.completed else 'Pending'}")
        except IndexError:
            messagebox.showwarning("⚠ Warning", "Please select a task to view!")

    def mark_task_completed(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.tasks[index].mark_completed()
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("⚠ Warning", "Please select a task!")

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            removed = self.tasks.pop(index)
            messagebox.showinfo("🗑 Deleted", f"Task '{removed.title}' deleted!")
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("⚠ Warning", "Please select a task!")

    def save_and_exit(self):
        save_tasks(self.tasks)
        messagebox.showinfo("💾 Saved", "Tasks saved successfully!")
        self.root.destroy()

# ---------------- Run App ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
