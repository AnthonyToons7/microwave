import tkinter as tk
import threading
import os
from Helpers.CurlHelper import (
    get_curl_dir,
    get_curl_files,
    parse_curl_file
)
from Helpers.RequestHelper import execute_request
from tkinter import (
    filedialog, 
    messagebox, 
    simpledialog
)

def show_error(title="Error", message="Something went wrong"):
    messagebox.showerror(title, message)

def confirm(message, title="Confirm"):
    return messagebox.askyesno(title, message)

def ask_filename(title="New file", prompt="Filename:"):
    return simpledialog.askstring(title, prompt)

def select_text_file():
    return filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

def create_modal(parent, title, size="300x200", topmost=True):
    modal = tk.Toplevel(parent)
    modal.title(title)
    modal.geometry(size)
    modal.transient(parent)
    modal.grab_set()

    if topmost:
        modal.attributes("-topmost", True)

    return modal

def open_file_editor(parent, file_path):
    editor = create_modal(parent, f"Editing: {os.path.basename(file_path)}", "600x400")
    editor.resizable(True, True)
    text = tk.Text(editor, wrap="none", undo=True)
    text.pack(fill="both", expand=True)

    with open(file_path, "r", encoding="utf-8") as file:
        text.insert("1.0", file.read())

    def save_file(event=None):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text.get("1.0", "end-1c"))
        editor.destroy()

    def cancel():
        if confirm("Discard changes?", "Cancel"):
            editor.destroy()

    btn_frame = tk.Frame(editor)
    btn_frame.pack(fill="x", pady=5)

    tk.Button(btn_frame, text="Save", command=save_file, bg="#2ecc71").pack(side="right", padx=5)
    tk.Button(btn_frame, text="Cancel", command=cancel).pack(side="right")

    editor.bind("<Control-s>", save_file)

# def create_new():
#     name = ask_filename("New curl", "Filename:")
#     if not name:
#         return

#     path = os.path.join(get_curl_dir(), f"{name}.txt")
#     if os.path.exists(path):
#         show_error("Error", "File already exists")
#         return

#     template = """[META]
# METHOD=POST
# URL=

# [TO_EXECUTE]
# curl -X POST ""

# [ON_UNAUTHENTICATED]
# curl -X POST ""
# """

#     with open(path, "w", encoding="utf-8") as f:
#         f.write(template)

#     open_file_editor(root, path)
#     refresh_dropdown()

def open_choice_modal(root):
    root2 = create_modal(root, "Select curl request", "300x220")
    selected = tk.StringVar()

    label = tk.Label(root2, text="", wraplength=260)
    label.pack(pady=5)

    def refresh_dropdown():
        menu["menu"].delete(0, "end")
        files = get_curl_files()

        if files:
            selected.set(files[0])
            label.config(text=files[0])

            for f in files:
                menu["menu"].add_command(
                    label=f,
                    command=lambda v=f: selected.set(v)
                )
        else:
            selected.set("")
            label.config(text="No curl files found")

    def update_label(*_):
        label.config(text=selected.get())

    selected.trace_add("write", update_label)
    menu = tk.OptionMenu(root2, selected, "")
    menu.pack(pady=5)

    refresh_dropdown()

    def upload_file():
        path = select_text_file()
        if not path:
            return

        dest = os.path.join(get_curl_dir(), os.path.basename(path))

        if os.path.exists(dest):
            show_error("Error", "File already exists")
            return

        with open(path, "r", encoding="utf-8") as src, \
             open(dest, "w", encoding="utf-8") as dst:
            dst.write(src.read())

        refresh_dropdown()

    def create_new():
        name = ask_filename("New curl", "Filename:")
        if not name:
            return

        path = os.path.join(get_curl_dir(), f"{name}.txt")
        if os.path.exists(path):
            show_error("Error", "File already exists")
            return

        template = """[META]
METHOD=POST
URL=

[TO_EXECUTE]
curl -X POST ""

[ON_UNAUTHENTICATED]
curl -X POST ""
"""

        with open(path, "w", encoding="utf-8") as f:
            f.write(template)

        open_file_editor(root, path)
        refresh_dropdown()


    def execute_selected():
        global selected_curl_name

        if not selected.get():
            show_error("Error", "No curl selected")
            return

        selected_curl_name = selected.get()
        bundle = parse_curl_file(selected_curl_name)

        threading.Thread(
            target=execute_request,
            args=(bundle,root,open_choice_modal),
            daemon=True
        ).start()

    tk.Button(root2, text="Execute", command=execute_selected, bg="#2ecc71").pack(pady=10)
    tk.Button(root2, text="Upload .txt", command=upload_file).pack(pady=5)
    tk.Button(root2, text="Create New", command=create_new).pack()