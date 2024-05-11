import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkbootstrap import Style
import select_creatives
import move_creatives


def choose_file():
    file_path = filedialog.askopenfilename()
    excel_entry.delete(0, tk.END)
    excel_entry.insert(0, file_path)

def choose_folder():
    folder_path = filedialog.askdirectory()
    dir_entry.delete(0, tk.END)
    dir_entry.insert(0, folder_path)

def sort_by_folders():
    CREATIVE_PATH = rf"{dir_entry.get()}"
    EXCEL_PATH = rf"{excel_entry.get()}"
    move_creatives.main(CREATIVE_PATH, EXCEL_PATH)

def select_videos():
    CREATIVE_PATH = rf"{dir_entry.get()}"
    select_creatives.main(CREATIVE_PATH)


if __name__ == '__main__':

    root = tk.Tk()
    root.title("Скип тупых креативов")

    style = Style(theme="minty")

    frame = ttk.Frame(root, padding="10")
    frame.pack()

    excel_entry = ttk.Entry(frame, width=50)
    excel_entry.grid(row=0, column=0, padx=5, pady=5)

    choose_button1 = ttk.Button(frame, text="Excel", command=choose_file, width=10)
    choose_button1.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    dir_entry = ttk.Entry(frame, width=50)
    dir_entry.grid(row=1, column=0, padx=5, pady=5)

    choose_button2 = ttk.Button(frame, text="Креативы", command=choose_folder, width=10)
    choose_button2.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    sort_button = ttk.Button(frame, text="Раскидать по папкам", command=sort_by_folders)
    sort_button.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

    select_button = ttk.Button(frame, text="Отобрать лучшие", bootstyle="success-outline", command=select_videos)
    select_button.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

    root.mainloop()
