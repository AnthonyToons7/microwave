from Helpers.EffectHelper import start_shake
from Helpers.ImageHelper import create_image_model
from Helpers.LabelHelper import (
    create_label,
    destroy_labels
)
import threading
from Helpers.AudioHelper import AudioPlayer
from Helpers.CurlHelper import execute_curl_bundle
import traceback

def on_done(audio, done_wave):
    audio.play(done_wave)

def on_click(label, root, open_choice_modal):
    destroy_labels(root)

    microwave_img = create_image_model("../img/microwave-open.png")
    label = create_label(root, microwave_img)
    label.bind("<Button-1>", lambda e: open_choice_modal(root))

def execute_request(bundle, root, open_choice_modal):
    global audio
    audio = AudioPlayer()

    microwave_wave = audio.load_audio_file("./sfx/mmmmmmmmmmmmmm.wav", volume=0.1)
    done_wave = audio.load_audio_file("./sfx/beepbeep.wav", volume=0.09)

    shake_window = threading.Event()
    destroy_labels(root)

    microwave_img = create_image_model("../img/microwave.png")
    fresh_label = create_label(root, microwave_img)

    try:
        root.after(0, start_shake, root, shake_window)
        audio.play_loop(microwave_wave)

        result = execute_curl_bundle(bundle)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

    except Exception:
        traceback.print_exc()

    finally:
        shake_window.clear()
        fresh_label.bind(
            "<Button-1>",
            lambda e: on_click(fresh_label, root, open_choice_modal)
        )
        audio.stop()
        root.after(0, lambda: on_done(audio, done_wave))
