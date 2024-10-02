import tkinter as tk
from tkinter import simpledialog
import os

class TaskFrame(tk.Frame):
    def __init__(self, master, title):
        super().__init__(master)
        self.title_label = tk.Label(self, text=title, font=("Arial", 14))
        self.title_label.pack(pady=5)

        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # Список для выполненных задач
        self.completed_label = tk.Label(self, text="Выполненные задачи", font=("Arial", 12))
        self.completed_label.pack(pady=5)

        self.completed_listbox = tk.Listbox(self)
        self.completed_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # Кнопки для работы с задачами
        self.add_button = tk.Button(self, text="Добавить чечика", command=self.add_task)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(self, text="Удалить чечика", command=self.remove_task)
        self.remove_button.pack(pady=5)

        self.complete_button = tk.Button(self, text="Чечик выбит", command=self.mark_completed)
        self.complete_button.pack(pady=5)

        self.load_tasks(title)

    def add_task(self):
        task = simpledialog.askstring("Новый чечик", "Введите чечика:")
        if task:
            self.listbox.insert(tk.END, task)
            self.save_tasks()

    def remove_task(self):
        selected_task_index = self.listbox.curselection()
        if selected_task_index:
            self.listbox.delete(selected_task_index)
            self.save_tasks()

    def mark_completed(self):
        selected_task_index = self.listbox.curselection()
        if selected_task_index:
            task = self.listbox.get(selected_task_index)

            # Перемещаем задачу в выполненные задачи
            self.listbox.delete(selected_task_index)
            self.completed_listbox.insert(tk.END, task)
            self.save_tasks()

    def load_tasks(self, title):
        # Загружаем задачи
        if os.path.exists(f"{title}_tasks.txt"):
            with open(f"{title}_tasks.txt", "r") as file:
                for line in file:
                    task = line.strip()
                    self.listbox.insert(tk.END, task)

        # Загружаем выполненные задачи
        if os.path.exists(f"{title}_completed.txt"):
            with open(f"{title}_completed.txt", "r") as file:
                for line in file:
                    completed_task = line.strip()
                    self.completed_listbox.insert(tk.END, completed_task)

    def save_tasks(self):
        title = self.title_label.cget("text")
        # Сохраняем невыполненные задачи
        with open(f"{title}_tasks.txt", "w") as file:
            for task in self.listbox.get(0, tk.END):
                file.write(task + "\n")
        
        # Сохраняем выполненные задачи
        with open(f"{title}_completed.txt", "w") as file:
            for task in self.completed_listbox.get(0, tk.END):
                file.write(task + "\n")

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Чеклист")

        # Устанавливаем размер окна по умолчанию
        self.root.geometry("800x600")

        # Создаем фреймы для двух списков задач
        self.frame1 = TaskFrame(self.root, "ГИ")
        self.frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.frame2 = TaskFrame(self.root, "ХСР")
        self.frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Кнопка "Выйти"
        self.exit_button = tk.Button(self.root, text="Выйти", command=self.root.quit)
        self.exit_button.pack(side=tk.RIGHT, padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    
    # Инициализация приложения
    app = MainApp(root)
    
    root.mainloop()
