import tkinter as tk
from tkinter import simpledialog
import os

class TaskFrame(tk.Frame):
    def __init__(self, master, title):
        super().__init__(master)
        self.title_label = tk.Label(self, text=title, font=("Arial", 16))
        self.title_label.pack(pady=5)

        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # Список для выбитых чечиков
        self.completed_label = tk.Label(self, text="Эти чечики теперь мои \u2193", font=("Arial", 16))
        self.completed_label.pack(pady=5)

        self.completed_listbox = tk.Listbox(self)
        self.completed_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # Кнопки для работы с чечиками
        self.add_button = tk.Button(self, text="Добавить чечика", command=self.add_task)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(self, text="Удалить чечика", command=self.remove_task)
        self.remove_button.pack(pady=5)

        self.complete_button = tk.Button(self, text="Чечик выбит", command=self.mark_completed)
        self.complete_button.pack(pady=5)

        # Кнопка для добавления сигны (выделения цветом)
        self.diamond_button = tk.Button(self, text="А у меня сигна есть", command=self.add_diamond)
        self.diamond_button.pack(pady=5)

        self.load_tasks(title)

    def add_task(self):
        task = simpledialog.askstring("Новый чечик", "Введите чечика:")
        if task:
            self.listbox.insert(tk.END, task)
            self.save_tasks()

    def remove_task(self):
        # Проверяем, есть ли выбранный чечик в основном списке
        selected_task_index = self.listbox.curselection()
        if selected_task_index:
            self.listbox.delete(selected_task_index)
            self.save_tasks()
        else:
            # Проверяем, есть ли выбранный чечик в списке выполненных задач
            selected_completed_task_index = self.completed_listbox.curselection()
            if selected_completed_task_index:
                self.completed_listbox.delete(selected_completed_task_index)
                self.save_tasks()

    def mark_completed(self):
        selected_task_index = self.listbox.curselection()
        if selected_task_index:
            task = self.listbox.get(selected_task_index)

            # Перемещаем чечика в выбитых
            self.listbox.delete(selected_task_index)
            self.completed_listbox.insert(tk.END, task)
            self.save_tasks()

    def add_diamond(self):
        selected_completed_task_index = self.completed_listbox.curselection()
        if selected_completed_task_index:
            task = self.completed_listbox.get(selected_completed_task_index)

            # Проверяем, выделен ли чечик цветом
            if self.completed_listbox.itemcget(selected_completed_task_index, 'bg') == 'SystemButtonFace':
                # Добавляем выделение цветом
                self.completed_listbox.itemconfig(selected_completed_task_index, bg='light blue')
            else:
                # Убираем выделение цветом
                self.completed_listbox.itemconfig(selected_completed_task_index, bg='SystemButtonFace')
            
            self.save_tasks()

    def load_tasks(self, title):
        # Загружаем чечиков
        if os.path.exists(f"{title}_tasks.txt"):
            with open(f"{title}_tasks.txt", "r") as file:
                for line in file:
                    task = line.strip()
                    self.listbox.insert(tk.END, task)

        # Загружаем выбитых чечиков
        if os.path.exists(f"{title}_completed.txt"):
            with open(f"{title}_completed.txt", "r") as file:
                for line in file:
                    parts = line.strip().split("||")
                    task = parts[0]
                    self.completed_listbox.insert(tk.END, task)
                    if len(parts) > 1 and parts[1] == "highlight":
                        self.completed_listbox.itemconfig(self.completed_listbox.size() - 1, bg='light blue')

    def save_tasks(self):
        title = self.title_label.cget("text")
        # Сохраняем невыбитых чечиков
        with open(f"{title}_tasks.txt", "w") as file:
            for task in self.listbox.get(0, tk.END):
                file.write(task + "\n")
        
        # Сохраняем выбитых чечиков, включая цветовые выделения
        with open(f"{title}_completed.txt", "w") as file:
            for i in range(self.completed_listbox.size()):
                task = self.completed_listbox.get(i)
                if self.completed_listbox.itemcget(i, 'bg') == 'light blue':
                    file.write(f"{task}||highlight\n")
                else:
                    file.write(f"{task}\n")

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Чеклист")

        # Устанавливаем размер окна
        self.root.geometry("900x700")

        # Создаем фреймы для двух игр
        self.frame1 = TaskFrame(self.root, "ГИ")
        self.frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.frame2 = TaskFrame(self.root, "ХСР")
        self.frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Кнопка "я устал, я ухожу"
        self.exit_button = tk.Button(self.root, text="я устал, я ухожу", command=self.root.quit)
        self.exit_button.pack(side=tk.RIGHT, padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    
    # Инициализация приложения
    app = MainApp(root)
    
    root.mainloop()
