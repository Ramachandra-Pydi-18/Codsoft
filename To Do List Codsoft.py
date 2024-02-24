import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3 as sql

def AddTask():
    task_str = task_field.get().strip()
    if len(task_str) == 0:
        messagebox.showinfo('Task should contain minimum one character !!')
    else:
        tasks.append((task_str, 0))  # Task tuple (task_str, done)
        the_cursor.execute('INSERT INTO tasks VALUES (?, ?)', (task_str, 0))
        Update_list()
        task_field.delete(0, 'end')

def ToggleTask():
    try:
        index = task_listbox.curselection()[0]
        task = tasks[index]
        new_status = 1 - task[1]  # Toggle the 'done' status
        tasks[index] = (task[0], new_status)
        the_cursor.execute('UPDATE tasks SET done = ? WHERE title = ?', (new_status, task[0]))
        Update_list()
    except IndexError:
        messagebox.showinfo('No task selected!! Please select a task.')

def Update_list():
    clear_list()
    for i, (task, done) in enumerate(tasks):
        if done:
            task_listbox.insert('end', '✓ ' + task)
            task_listbox.itemconfig(i, bg="#90EE90")  # Light green background for completed tasks
        else:
            task_listbox.insert('end', task)
            task_listbox.itemconfig(i, bg="#FFFFFF")  # White background for incomplete tasks

def delete_task():
    try:
        index = task_listbox.curselection()[0]
        task = tasks[index]
        the_cursor.execute('DELETE FROM tasks WHERE title = ?', (task[0],))
        tasks.pop(index)
        Update_list()
    except IndexError:
        messagebox.showinfo('No task selected!! Please select a task.')

def delete_all():
    message_box = messagebox.askyesno('Are you sure to delete all tasks?')
    if message_box:
        the_cursor.execute('DELETE FROM tasks')
        tasks.clear()
        Update_list()

def clear_list():
    task_listbox.delete(0, 'end')

def close():
    print(tasks)
    connection.commit()
    connection.close()
    guiWindow.destroy()

def retrive():
    for row in the_cursor.execute('SELECT title, done FROM tasks'):
        tasks.append(row)

if __name__ == "__main__":
    guiWindow = tk.Tk()
    guiWindow.title("TO-DO LIST APPLICATION")
    guiWindow.geometry("600x400+850+350")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#ADD8E6")

    connection = sql.connect('listOfTasks.db')
    the_cursor = connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT, done INTEGER)')
    tasks = []

    header = tk.Frame(guiWindow, bg="#ADD8E6")
    functions_frame = tk.Frame(guiWindow, bg="#ADD8E6")
    listbox_frame = tk.Frame(guiWindow, bg="#ADD8E6")

    header.pack(fill="x")
    functions_frame.pack(side="left", expand=True, fill="both")
    listbox_frame.pack(side="right", expand=True, fill="both")

    header_label = ttk.Label(header, text="TO-DO LIST", font=("Helvetica", "25", "bold"),
                             background="#ADD8E6", foreground="#8B4513")
    header_label.pack(padx=20, pady=20)

    task_label = ttk.Label(functions_frame, text="Enter a Task:", font=("Consolas", "15", "bold"),
                           background="#ADD8E6", foreground="#000000")
    task_label.place(x=30, y=40)

    task_field = ttk.Entry(functions_frame, font=("Consolas", "12"), width=18,
                           background="#FFFFFF", foreground="#000000")
    task_field.place(x=30, y=80)

    add_button = ttk.Button(functions_frame, text="Add Task", width=26, command=AddTask)
    del_button = ttk.Button(functions_frame, text="Delete Task", width=26, command=delete_task)
    delete_all_button = ttk.Button(functions_frame, text="Delete All Tasks", width=26, command=delete_all)
    toggle_button = ttk.Button(functions_frame, text="Toggle Task", width=26, command=ToggleTask)
    exit_button = ttk.Button(functions_frame, text="Exit", width=26, command=close)

    add_button.place(x=30, y=120)
    del_button.place(x=30, y=160)
    delete_all_button.place(x=30, y=200)
    toggle_button.place(x=30, y=240)
    exit_button.place(x=30, y=280)

    task_listbox = tk.Listbox(listbox_frame, width=26, height=15, selectmode='SINGLE',
                              background="#FFFFFF", foreground="#000000", selectbackground="#CD853F",
                              selectforeground="#FFFFFF")
    task_listbox.place(x=10, y=20)

    retrive()
    Update_list()

    guiWindow.mainloop()
