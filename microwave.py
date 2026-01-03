import tkinter as tk

# IMPORT HELPERS
from Helpers.PopupHelper import open_choice_modal
from Helpers.LabelHelper import create_label
from Helpers.ImageHelper import create_image_model
from Helpers.RequestHelper import on_click

options = []
selected_curl_name = None

root = tk.Tk()
root.title("")
root.attributes("-topmost", True)
root.resizable(False, False)
microwave_img = create_image_model("../img/microwave.png")
label = create_label(root, microwave_img)
label.bind("<Button-1>", lambda e: on_click(label, root, open_choice_modal))
root.mainloop()