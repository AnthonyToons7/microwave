import threading
import simpleaudio as sa
import wave
import audioop

class AudioPlayer:
    def __init__(self):
        self._stop_event = threading.Event()
        self._current = None

    def load_audio_file(self, path, volume=0.3):
        with wave.open(path, 'rb') as wave_file:
            params = wave_file.getparams()
            frames = wave_file.readframes(wave_file.getnframes())

        frames = audioop.mul(frames, params.sampwidth, volume)
        return sa.WaveObject(frames, params.nchannels, params.sampwidth, params.framerate)

    def play(self, wave):
        self.stop()
        if wave:
            self._current = wave.play()

    def play_loop(self, wave):
        self.stop()
        self._stop_event.clear()

        def loop():
            while not self._stop_event.is_set():
                self._current = wave.play()
                self._current.wait_done()

        threading.Thread(target=loop, daemon=True).start()

    def stop(self):
        self._stop_event.set()
        if self._current:
            self._current.stop()
            self._current = None
