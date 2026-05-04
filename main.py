import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random

FILENAME = 'tasks.json'

# Предопределённые задачи
predefined_tasks = [
    {"task": "Прочитать статью", "type": "учёба"},
    {"task": "Сделать зарядку", "type": "спорт"},
    {"task": "Позвонить другу", "type": "личное"},
    {"task": "Написать отчёт", "type": "работа"},
    {"task": "Прогулка на улице", "type": "спорт"},
    {"task": "Изучить тему по математике", "type": "учёба"},
]

# Загрузка истории
def load_history():
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Сохранение истории
def save_history(data):
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.history = load_history()
        self.filtered_history = self.history.copy()

        self.create_widgets()
        self.update_task_list()

    def create_widgets(self):
        # Кнопка генерации
        self.generate_btn = tk.Button(self.root, text="Сгенерировать задачу", command=self.generate_task)
        self.generate_btn.pack(pady=5)

        # Отображение текущей сгенерированной задачи
        self.current_task_label = tk.Label(self.root, text="", font=('Arial', 14))
        self.current_task_label.pack(pady=5)

        # Поле для фильтрации по типу
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр по типу (учёба, спорт, работа):").grid(row=0, column=0, padx=5)

        self.type_filter_entry = tk.Entry(filter_frame)
        self.type_filter_entry.grid(row=0, column=1, padx=5)

        filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.grid(row=0, column=2, padx=5)

        show_all_btn = tk.Button(filter_frame, text="Показать всё", command=self.show_all)
        show_all_btn.grid(row=0, column=3, padx=5)

        # История задач
        self.history_listbox = tk.Listbox(self, height=10, width=50)
        self.history_listbox.pack(pady=10)

        # Возможность ввести новую задачу
        new_task_frame = tk.Frame(self)
        new_task_frame.pack(pady=10)

        tk.Label(new_task_frame, text="Новая задача:").grid(row=0, column=0, padx=5)
        self.new_task_entry = tk.Entry(new_task_frame, width=30)
        self.new_task_entry.grid(row=0, column=1, padx=5)

        tk.Label(new_task_frame, text="Тип:").grid(row=0, column=2, padx=5)
        self.new_task_type_entry = tk.Entry(new_task_frame, width=15)
        self.new_task_type_entry.grid(row=0, column=3, padx=5)

        add_task_btn = tk.Button(new_task_frame, text="Добавить задачу", command=self.add_custom_task)
        add_task_btn.grid(row=0, column=4, padx=5)

    def generate_task(self):
        task = random.choice(predefined_tasks)
        self.current_task_label.config(text=f"{task['task']} ({task['type']})")
        # Добавляем в историю
        self.history.append(task)
        save_history(self.history)
        self.update_task_list()

    def update_task_list(self):
        self.history_listbox.delete(0, tk.END)
        for task in self.history:
            display_text = f"{task['task']} ({task['type']})"
            self.history_listbox.insert(tk.END, display_text)

    def add_custom_task(self):
        task_text = self.new_task_entry.get().strip()
        task_type = self.new_task_type_entry.get().strip()
        if not task_text or not task_type:
            messagebox.showerror("Ошибка", "Поле задачи и типа не должны быть пустыми.")
            return
        task = {"task": task_text, "type": task_type}
        self.history.append(task)
        save_history(self.history)
        self.new_task_entry.delete(0, tk.END)
        self.new_task_type_entry.delete(0, tk.END)
        self.update_task_list()

    def apply_filter(self):
        filter_type = self.type_filter_entry.get().strip().lower()
        if filter_type:
            self.filtered_history = [t for t in self.history if t['type'].lower() == filter_type]
        else:
            self.filtered_history = self.history.copy()
        self.history_listbox.delete(0, tk.END)
        for task in self.filtered_history:
            display_text = f"{task['task']} ({task['type']})"
            self.history_listbox.insert(tk.END, display_text)

    def show_all(self):
        self.type_filter_entry.delete(0, tk.END)
        self.update_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
