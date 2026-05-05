import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library — Библиотека фильмов")
        self.root.geometry("700x500")
        
        self.file_path = "movies.json"
        self.movies = self.load_data()

        # Настройка интерфейса
        self.setup_input_ui()
        self.setup_filter_ui()
        self.setup_table_ui()
        self.refresh_table()

    def setup_input_ui(self):
        frame = tk.LabelFrame(self.root, text="Добавить новый фильм", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        fields = [("Название", 0), ("Жанр", 1), ("Год", 2), ("Рейтинг (0-10)", 3)]
        self.entries = {}

        for label_text, col in fields:
            tk.Label(frame, text=label_text).grid(row=0, column=col)
            entry = tk.Entry(frame)
            entry.grid(row=1, column=col, padx=5)
            self.entries[label_text] = entry

        btn_add = tk.Button(frame, text="Добавить", command=self.add_movie, bg="#4CAF50", fg="white")
        btn_add.grid(row=1, column=4, padx=10)

    def setup_filter_ui(self):
        frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text="Жанр:").grid(row=0, column=0)
        self.filter_genre = tk.Entry(frame)
        self.filter_genre.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Год:").grid(row=0, column=2)
        self.filter_year = tk.Entry(frame)
        self.filter_year.grid(row=0, column=3, padx=5)

        tk.Button(frame, text="Применить", command=self.apply_filters).grid(row=0, column=4, padx=5)
        tk.Button(frame, text="Сброс", command=self.refresh_table).grid(row=0, column=5, padx=5)

    def setup_table_ui(self):
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год выпуска")
        self.tree.heading("rating", text="Рейтинг")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_movie(self):
        data = {k: v.get().strip() for k, v in self.entries.items()}
        
        if not all(data.values()):
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        try:
            year = int(data["Год"])
            rating = float(data["Рейтинг (0-10)"])
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом, а рейтинг от 0 до 10!")
            return

        new_movie = {
            "title": data["Название"],
            "genre": data["Жанр"],
            "year": year,
            "rating": rating
        }
        
        self.movies.append(new_movie)
        self.save_data()
        self.refresh_table()
        
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def apply_filters(self):
        g_crit = self.filter_genre.get().lower()
        y_crit = self.filter_year.get()

        filtered = [
            m for m in self.movies
            if (not g_crit or g_crit in m["genre"].lower()) and
               (not y_crit or y_crit == str(m["year"]))
        ]
        self.refresh_table(filtered)

    def refresh_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        display_list = data if data is not None else self.movies
        for m in display_list:
            self.tree.insert("", "end", values=(m["title"], m["genre"], m["year"], m["rating"]))

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return []
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()