import os
import wave
import time
import threading

import tkinter as tk
import pyaudio
from tkinter import filedialog


class VoiceRecorder:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.resizable(False, False)

        self.button_record = tk.Button(text="🎤", font=(
            "Arial", 120, "bold"), command=self.toggle_recording)
        self.button_record.pack()

        self.button_upload = tk.Button(text="Upload Recording", font=(
            "Arial", 16), command=self.upload_recording)
        self.button_upload.pack()

        self.button_analyze = tk.Button(text="Analyze Recording", font=(
            "Arial", 16), command=self.analyze_recording)
        self.button_analyze.pack()
        self.button_analyze.pack_forget()

        self.label = tk.Label(text="00:00:00")
        self.label.pack()

        self.recording = False
        self.audio_frames = []
        self.root.mainloop()

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recording = True
        self.button_record.config(fg="red")
        threading.Thread(target=self.record).start()

    def stop_recording(self):
        self.recording = False
        self.button_record.config(fg='black')

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1,
                            rate=44100, input=True, frames_per_buffer=1024)

        start = time.time()

        # Record for 10 seconds
        while self.recording and (time.time() - start) <= 10:
            data = stream.read(1024)
            self.audio_frames.append(data)

            passed = time.time() - start
            seconds = passed % 60
            minutes = passed // 60
            hours = minutes // 60

            self.label.config(
                text=f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        if self.recording:
            self.stop_recording()
            self.show_analyze_button()

    def upload_recording(self):
        file_path = filedialog.askopenfilename(
            title="Select a recording file", filetypes=[("Wave files", "*.wav")])
        if file_path:
            self.audio_frames = []
            self.label.config(text="00:00:00")
            self.button_analyze.pack_forget()
            self.process_uploaded_recording(file_path)

    def process_uploaded_recording(self, file_path):
        sound_file = wave.open(file_path, "rb")
        self.audio_frames = sound_file.readframes(sound_file.getnframes())
        sound_file.close()
        duration = sound_file.getnframes() / sound_file.getframerate()

        seconds = int(duration % 60)
        minutes = int((duration // 60) % 60)
        hours = int(duration // 3600)

        self.label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.show_analyze_button()

    def analyze_recording(self):
        # Implement the function to handle the analysis of the recorded audio
        pass

    def show_analyze_button(self):
        self.button_analyze.pack()


VoiceRecorder()
