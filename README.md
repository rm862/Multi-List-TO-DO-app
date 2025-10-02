# Multi-List-TO-DO-App 📜

A friendly, feature-rich multi-list todo application built with Python's tkinter library. Manage multiple task lists with a warm, peaceful user interface designed for comfortable daily use.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![No Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

## Features 

### Multiple Task Lists
- **Create unlimited lists** - Organize tasks by project, category, or any way you prefer
- **Easy list switching** - Quick dropdown navigation between your lists
- **List management** - Rename or delete lists as your needs change
- **Persistent storage** - All lists are automatically saved and restored

### Task Management
- **Add tasks quickly** - Simple input field with Enter key support
- **Check off completed tasks** - Visual checkbox to mark progress
- **Edit tasks inline** - Update task text anytime with the Edit button
- **Delete tasks** - Remove individual tasks or clear all completed at once
- **Task counter** - Real-time display of completed vs. total tasks

### Customizable Interface
- **Editable list titles** - Click the title to customize each list's name
- **Soft color scheme** - Warm cream and beige palette for comfortable viewing
- **Completed task highlighting** - Soft sage green background for finished tasks
- **Scrollable task view** - Handle any number of tasks without cluttering

### Data Persistence
- **Automatic saving** - Every change is instantly saved to disk
- **JSON storage** - Human-readable data format in `multi_todo_data.json`
- **Remember last session** - App opens to your most recently used list
- **Timestamps** - Each task and list records its creation time

## Installation 

### Prerequisites
- Python 3.6 or higher
- tkinter (included with most Python installations)

### Setup
1. Clone this repository:
```bash
git clone https://github.com/yourusername/Multi-List-TO-DO-app.git
cd Multi-List-TO-DO-app
```

2. Run the application:
```bash
python "to do.py"
```

**Note**: No external dependencies required! The app uses only Python's built-in tkinter library.

## Usage 

### Getting Started
1. Launch the app - it starts with a default "My To-Do List"
2. Type a task in the input field and press Enter or click "Add Task"
3. Check the box when you complete a task
4. Use Edit/Delete buttons to manage individual tasks

### Managing Multiple Lists
- **Create a new list**: Click the "New" button next to the list dropdown
- **Switch between lists**: Select from the dropdown menu
- **Rename a list**: Click "Rename" or edit the title at the top
- **Delete a list**: Click "Delete" (requires at least one list to remain)

### Keyboard Shortcuts
- `Enter` - Add new task (when focused on input field)
- `Enter` - Save title edit (when editing the list title)

### Data Location
All your tasks are saved in `multi_todo_data.json` in the application directory. You can backup this file to preserve your tasks.

## Project Structure 

```
Multi-List-TO-DO-app/
├── to do.py              # Main application file
├── multi_todo_data.json  # Data storage (created automatically)
├── requirements.txt      # Dependency info (none required)
├── README.md            # This file
├── LICENSE              # MIT License
└── .gitignore          # Git ignore rules
```

## Technical Details 

### Architecture
- **Single-file application** - All code in `to do.py` for simplicity
- **Object-oriented design** - `MultiListTodoApp` class encapsulates all functionality
- **Event-driven GUI** - Built on tkinter's event loop

### Data Structure
```json
{
  "current_list": "List Name",
  "task_lists": {
    "List Name": {
      "title": "Custom Title",
      "tasks": [
        {
          "text": "Task description",
          "completed": false,
          "created": "2025-10-02 14:30"
        }
      ],
      "created": "2025-10-02 14:00"
    }
  }
}
```

### Color Scheme
The app uses a carefully selected warm, peaceful palette:
- Background: `#f7f3f0` (Warm cream)
- Secondary: `#e8ddd4` (Light beige)
- Accent: `#d4b5a0` (Soft brown)
- Text: `#5d4e37` (Dark brown)
- Completed: `#a8c4a2` (Soft sage green)

## Contributing 

Contributions are welcome! Feel free to:
- Report bugs by opening an issue
- Suggest new features
- Submit pull requests with improvements

## License 

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Reva Malik

## Acknowledgments 

- Built with Python's tkinter library
- Designed with a focus on simplicity and user comfort
- Inspired by the need for organized, stress-free task management

## Support 

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Enjoy organizing your tasks! **
