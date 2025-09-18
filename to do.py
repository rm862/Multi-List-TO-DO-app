import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

class MultiListTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("550x650")
        self.root.resizable(True, True)
        
        # Soft, peaceful color scheme
        self.colors = {
            'bg': '#f7f3f0',           # Warm cream
            'secondary': '#e8ddd4',     # Light beige
            'accent': '#d4b5a0',       # Soft brown
            'text': '#5d4e37',         # Dark brown
            'button': '#c4a484',       # Medium brown
            'completed': '#a8c4a2'      # Soft sage green
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Task storage and app settings
        self.task_lists = {}  # Dictionary to store multiple lists
        self.current_list_name = "Default"
        self.load_all_data()
        
        # Set initial window title
        self.update_window_title()
        
        self.setup_gui()
        self.refresh_task_list()
        
    def setup_gui(self):
        # List selection frame
        list_frame = tk.Frame(self.root, bg=self.colors['bg'])
        list_frame.pack(pady=(10, 5), padx=20, fill='x')
        
        tk.Label(
            list_frame,
            text="Task List:",
            font=("Comic Sans MS", 12, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(side='left')
        
        # List dropdown
        self.list_var = tk.StringVar(value=self.current_list_name)
        self.list_dropdown = ttk.Combobox(
            list_frame,
            textvariable=self.list_var,
            values=list(self.task_lists.keys()),
            state='readonly',
            font=("Comic Sans MS", 10)
        )
        self.list_dropdown.pack(side='left', padx=(10, 5), fill='x', expand=True)
        self.list_dropdown.bind('<<ComboboxSelected>>', self.switch_list)
        
        # List management buttons
        new_list_btn = tk.Button(
            list_frame,
            text="New",
            command=self.create_new_list,
            bg=self.colors['button'],
            fg='white',
            font=("Comic Sans MS", 9),
            relief='flat',
            cursor='hand2'
        )
        new_list_btn.pack(side='right', padx=2)
        
        rename_list_btn = tk.Button(
            list_frame,
            text="Rename",
            command=self.rename_current_list,
            bg=self.colors['accent'],
            fg='white',
            font=("Comic Sans MS", 9),
            relief='flat',
            cursor='hand2'
        )
        rename_list_btn.pack(side='right', padx=2)
        
        delete_list_btn = tk.Button(
            list_frame,
            text="Delete",
            command=self.delete_current_list,
            bg='#d4a5a5',
            fg='white',
            font=("Comic Sans MS", 9),
            relief='flat',
            cursor='hand2'
        )
        delete_list_btn.pack(side='right', padx=2)
        
        # Current list title (editable)
        self.title_var = tk.StringVar(value=self.get_current_list_title())
        title_entry = tk.Entry(
            self.root,
            textvariable=self.title_var,
            font=("Comic Sans MS", 18, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            relief='flat',
            justify='center',
            bd=0
        )
        title_entry.pack(pady=(10, 5))
        title_entry.bind('<Return>', self.update_title)
        title_entry.bind('<FocusOut>', self.update_title)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root, 
            text="edit title",
            font=("Comic Sans MS", 10, "italic"),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Input frame
        input_frame = tk.Frame(self.root, bg=self.colors['bg'])
        input_frame.pack(pady=10, padx=20, fill='x')
        
        # Task entry
        self.task_entry = tk.Entry(
            input_frame,
            font=("Comic Sans MS", 12),
            bg='white',
            fg=self.colors['text'],
            relief='flat',
            bd=5
        )
        self.task_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        # Add button
        add_btn = tk.Button(
            input_frame,
            text="Add Task",
            command=self.add_task,
            bg=self.colors['button'],
            fg='white',
            font=("Comic Sans MS", 10, "bold"),
            relief='flat',
            padx=15,
            cursor='hand2'
        )
        add_btn.pack(side='right')
        
        # Task list frame with scrollbar
        task_list_frame = tk.Frame(self.root, bg=self.colors['bg'])
        task_list_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(
            task_list_frame, 
            bg=self.colors['bg'],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(task_list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bottom buttons frame
        button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        button_frame.pack(pady=10, padx=20, fill='x')
        
        # Clear completed button
        clear_btn = tk.Button(
            button_frame,
            text="Clear Completed",
            command=self.clear_completed,
            bg=self.colors['accent'],
            fg='white',
            font=("Comic Sans MS", 10),
            relief='flat',
            cursor='hand2'
        )
        clear_btn.pack(side='left')
        
        # Task counter
        self.counter_label = tk.Label(
            button_frame,
            text="",
            font=("Comic Sans MS", 10),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.counter_label.pack(side='right')
        
    def get_current_list_title(self):
        if self.current_list_name in self.task_lists:
            return self.task_lists[self.current_list_name].get('title', self.current_list_name)
        return self.current_list_name
        
    def get_current_tasks(self):
        if self.current_list_name in self.task_lists:
            return self.task_lists[self.current_list_name].get('tasks', [])
        return []
        
    def update_window_title(self):
        self.root.title(f"Multi-List Todo - {self.current_list_name}")
        
    def create_new_list(self):
        new_name = simpledialog.askstring(
            "New List",
            "Enter name for the new list:",
            initialvalue="New List"
        )
        
        if new_name and new_name.strip():
            new_name = new_name.strip()
            if new_name in self.task_lists:
                messagebox.showwarning("List Exists", "A list with this name already exists!")
                return
                
            self.task_lists[new_name] = {
                'title': new_name,
                'tasks': [],
                'created': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            self.current_list_name = new_name
            self.list_dropdown['values'] = list(self.task_lists.keys())
            self.list_var.set(new_name)
            self.title_var.set(new_name)
            
            self.update_window_title()
            self.refresh_task_list()
            self.save_all_data()
            
    def rename_current_list(self):
        if len(self.task_lists) <= 1:
            messagebox.showinfo("Cannot Rename", "You must have at least one list!")
            return
            
        new_name = simpledialog.askstring(
            "Rename List",
            "Enter new name for the list:",
            initialvalue=self.current_list_name
        )
        
        if new_name and new_name.strip() and new_name.strip() != self.current_list_name:
            new_name = new_name.strip()
            if new_name in self.task_lists:
                messagebox.showwarning("List Exists", "A list with this name already exists!")
                return
                
            # Move data to new key
            self.task_lists[new_name] = self.task_lists[self.current_list_name]
            self.task_lists[new_name]['title'] = new_name
            del self.task_lists[self.current_list_name]
            
            self.current_list_name = new_name
            self.list_dropdown['values'] = list(self.task_lists.keys())
            self.list_var.set(new_name)
            self.title_var.set(self.task_lists[new_name]['title'])
            
            self.update_window_title()
            self.save_all_data()
            
    def delete_current_list(self):
        if len(self.task_lists) <= 1:
            messagebox.showinfo("Cannot Delete", "You must have at least one list!")
            return
            
        if messagebox.askyesno("Delete List", f"Are you sure you want to delete '{self.current_list_name}'?"):
            del self.task_lists[self.current_list_name]
            
            # Switch to first available list
            self.current_list_name = list(self.task_lists.keys())[0]
            self.list_dropdown['values'] = list(self.task_lists.keys())
            self.list_var.set(self.current_list_name)
            self.title_var.set(self.get_current_list_title())
            
            self.update_window_title()
            self.refresh_task_list()
            self.save_all_data()
            
    def switch_list(self, event=None):
        selected_list = self.list_var.get()
        if selected_list in self.task_lists:
            self.current_list_name = selected_list
            self.title_var.set(self.get_current_list_title())
            self.update_window_title()
            self.refresh_task_list()
        
    def update_title(self, event=None):
        new_title = self.title_var.get().strip()
        if new_title and self.current_list_name in self.task_lists:
            self.task_lists[self.current_list_name]['title'] = new_title
            self.save_all_data()
        
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Empty Task", "Please enter a task!")
            return
            
        task = {
            'text': task_text,
            'completed': False,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        if self.current_list_name not in self.task_lists:
            self.task_lists[self.current_list_name] = {'title': self.current_list_name, 'tasks': []}
            
        self.task_lists[self.current_list_name]['tasks'].append(task)
        self.task_entry.delete(0, tk.END)
        self.refresh_task_list()
        self.save_all_data()
        
    def toggle_task(self, index):
        tasks = self.get_current_tasks()
        if 0 <= index < len(tasks):
            tasks[index]['completed'] = not tasks[index]['completed']
            self.refresh_task_list()
            self.save_all_data()
            
    def edit_task(self, index):
        tasks = self.get_current_tasks()
        if 0 <= index < len(tasks):
            current_text = tasks[index]['text']
            new_text = simpledialog.askstring(
                "Edit Task",
                "Edit your task:",
                initialvalue=current_text
            )
            
            if new_text and new_text.strip():
                tasks[index]['text'] = new_text.strip()
                self.refresh_task_list()
                self.save_all_data()
                
    def delete_task(self, index):
        tasks = self.get_current_tasks()
        if 0 <= index < len(tasks):
            if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
                del tasks[index]
                self.refresh_task_list()
                self.save_all_data()
                
    def clear_completed(self):
        tasks = self.get_current_tasks()
        completed_count = sum(1 for task in tasks if task['completed'])
        if completed_count == 0:
            messagebox.showinfo("No Completed Tasks", "No completed tasks to clear!")
            return
            
        if messagebox.askyesno("Clear Completed", f"Clear {completed_count} completed tasks?"):
            remaining_tasks = [task for task in tasks if not task['completed']]
            self.task_lists[self.current_list_name]['tasks'] = remaining_tasks
            self.refresh_task_list()
            self.save_all_data()
            
    def refresh_task_list(self):
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        tasks = self.get_current_tasks()
        
        if not tasks:
            # Show cute empty state
            empty_label = tk.Label(
                self.scrollable_frame,
                text="No tasks yet! Add one above to get started",
                font=("Comic Sans MS", 12, "italic"),
                bg=self.colors['bg'],
                fg=self.colors['text'],
                pady=50
            )
            empty_label.pack()
        else:
            # Display tasks
            for i, task in enumerate(tasks):
                task_frame = tk.Frame(
                    self.scrollable_frame,
                    bg=self.colors['completed'] if task['completed'] else self.colors['secondary'],
                    relief='flat',
                    bd=1
                )
                task_frame.pack(fill='x', pady=2, padx=5)
                
                # Checkbox
                checkbox_var = tk.BooleanVar(value=task['completed'])
                checkbox = tk.Checkbutton(
                    task_frame,
                    variable=checkbox_var,
                    command=lambda idx=i: self.toggle_task(idx),
                    bg=self.colors['completed'] if task['completed'] else self.colors['secondary'],
                    activebackground=self.colors['completed'] if task['completed'] else self.colors['secondary'],
                    fg='#2d5016',  # Dark green for checkmark
                    selectcolor='white',  # White background for checkbox when checked
                    activeforeground='#2d5016',  # Keep checkmark dark green when active
                    font=("Comic Sans MS", 12, "bold"),  # Make checkmark bigger and bold
                    cursor='hand2'
                )
                checkbox.pack(side='left', padx=5)
                
                # Task text
                text_style = ("Comic Sans MS", 11, "overstrike" if task['completed'] else "normal")
                task_label = tk.Label(
                    task_frame,
                    text=task['text'],
                    font=text_style,
                    bg=self.colors['completed'] if task['completed'] else self.colors['secondary'],
                    fg=self.colors['text'] if not task['completed'] else '#6b7a69',
                    anchor='w',
                    wraplength=250
                )
                task_label.pack(side='left', fill='x', expand=True, padx=5, pady=8)
                
                # Action buttons
                button_frame = tk.Frame(
                    task_frame, 
                    bg=self.colors['completed'] if task['completed'] else self.colors['secondary']
                )
                button_frame.pack(side='right', padx=5)
                
                # Edit button
                edit_btn = tk.Button(
                    button_frame,
                    text="Edit",
                    command=lambda idx=i: self.edit_task(idx),
                    bg=self.colors['button'],
                    fg='white',
                    relief='flat',
                    width=5,
                    cursor='hand2'
                )
                edit_btn.pack(side='left', padx=2)
                
                # Delete button
                delete_btn = tk.Button(
                    button_frame,
                    text="Delete",
                    command=lambda idx=i: self.delete_task(idx),
                    bg='#d4a5a5',
                    fg='white',
                    relief='flat',
                    width=5,
                    cursor='hand2'
                )
                delete_btn.pack(side='left', padx=2)
        
        # Update counter
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task['completed'])
        self.counter_label.config(
            text=f"{completed_tasks}/{total_tasks} completed"
        )
        
    def save_all_data(self):
        try:
            data = {
                'current_list': self.current_list_name,
                'task_lists': self.task_lists
            }
            with open('multi_todo_data.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
            
    def load_all_data(self):
        try:
            if os.path.exists('multi_todo_data.json'):
                with open('multi_todo_data.json', 'r') as f:
                    data = json.load(f)
                    self.current_list_name = data.get('current_list', 'Default')
                    self.task_lists = data.get('task_lists', {})
                    
            # Ensure we have at least one list
            if not self.task_lists:
                self.task_lists['Default'] = {
                    'title': 'My To-Do List',
                    'tasks': [],
                    'created': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
            # Ensure current list exists
            if self.current_list_name not in self.task_lists:
                self.current_list_name = list(self.task_lists.keys())[0]
                
        except Exception as e:
            print(f"Error loading data: {e}")
            self.task_lists = {
                'Default': {
                    'title': 'My To-Do List',
                    'tasks': [],
                    'created': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
            }
            self.current_list_name = 'Default'

def main():
    root = tk.Tk()
    app = MultiListTodoApp(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (550 // 2)
    y = (root.winfo_screenheight() // 2) - (650 // 2)
    root.geometry(f"550x650+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()