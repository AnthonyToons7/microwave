import tkinter as tk
import threading
import simpleaudio as sa
import traceback
import os

from tkinter import (
    filedialog, 
    messagebox, 
    simpledialog
)
from PIL import (
    Image,
    ImageTk
)

# IMPORT HELPERS
from Helpers.CurlHelper import (
    get_curl_dir,
    get_curl_files,
    parse_curl_file,
    execute_curl_bundle,
    update_bearer_token,
    extract_token
)
from Helpers.PopupHelper import (
    show_error,
    confirm,
    ask_filename,
    select_text_file,
    create_modal,
    open_file_editor,
    open_choice_modal
)
from Helpers.LabelHelper import (
    create_label,
    destroy_labels
)
from Helpers.ImageHelper import create_image_model
from Helpers.AudioHelper import AudioPlayer
from Helpers.RequestHelper import on_click

# GLOBALS
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