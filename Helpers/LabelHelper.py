import tkinter as tk

def destroy_labels(root):
    for widget in list(root.children.values()):
        widget.destroy()

def create_label(root, image):
    label = tk.Label(root, image=image, borderwidth=0, cursor="hand2")
    label.image = image
    label.pack()
    return label
