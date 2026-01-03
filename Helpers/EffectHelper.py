def start_shake(root, shake_window, intensity=20, delay=1):
    shake_window.set()
    x = root.winfo_x()
    y = root.winfo_y()

    offsets = [
        (-intensity, 0),
        (intensity, 0),
        (0, -intensity),
        (0, intensity),
        (-intensity, intensity),
        (intensity, -intensity),
    ]

    def _shake(i=0):
        if not shake_window.is_set():
            root.geometry(f"+{x}+{y}")
            return

        dx, dy = offsets[i % len(offsets)]
        root.geometry(f"+{x + dx}+{y + dy}")
        root.after(delay, _shake, i + 1)

    _shake()
