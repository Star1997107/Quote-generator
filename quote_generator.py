import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import random
import requests


class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("500x400")

        # Загрузка цитат
        self.quotes = self.load_quotes()
        self.history = []

        # Интерфейс
        self.create_widgets()

    def create_widgets(self):
        # Кнопка генерации
        self.generate_btn = tk.Button(
            self.root,
            text="Получить случайную цитату",
            command=self.generate_quote
        )
        self.generate_btn.pack(pady=10)

        # Поле вывода цитаты
        self.quote_text = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=60,
            height=10
        )
        self.quote_text.pack(pady=10, padx=10)
        self.quote_text.config(state=tk.DISABLED)

        # История цитат
        self.history_label = tk.Label(self.root, text="История цитат:")
        self.history_label.pack(anchor="w", padx=10)

        self.history_text = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=60,
            height=8
        )
        self.history_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        self.history_text.config(state=tk.DISABLED)

    def load_quotes(self):
        """Загрузка цитат из файла или API"""
        try:
            with open('quotes.json', 'r', encoding='utf-8') as f:
                quotes = json.load(f)
            if not isinstance(quotes, list) or not quotes:
                raise ValueError("Некорректный формат JSON")
            return quotes
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            # Резервные цитаты
            return [
                "Знание — сила. — Фрэнсис Бэкон",
                "Быть или не быть, вот в чём вопрос. — Уильям Шекспир",
                "Мыслю, следовательно, существую. — Рене Декарт"
            ]

    def generate_quote(self):
        """Генерация случайной цитаты"""
        if not self.quotes:
            messagebox.showerror("Ошибка", "Нет доступных цитат")
            return

        quote = random.choice(self.quotes)
        self.display_quote(quote)
        self.add_to_history(quote)

    def display_quote(self, quote):
        """Отображение цитаты в интерфейсе"""
        self.quote_text.config(state=tk.NORMAL)
        self.quote_text.delete(1.0, tk.END)
        self.quote_text.insert(tk.END, quote)
        self.quote_text.config(state=tk.DISABLED)

    def add_to_history(self, quote):
        """Добавление цитаты в историю и сохранение"""
        self.history.append(quote)
        if len(self.history) > 10:  # Ограничение истории
            self.history.pop(0)

        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        for i, q in enumerate(self.history, 1):
            self.history_text.insert(tk.END, f"{i}. {q}\n")
        self.history_text.config(state=tk.DISABLED)

        # Сохранение истории
        with open('history.json', 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)



if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()
