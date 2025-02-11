import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import pygame
import threading
from ttkthemes import ThemedTk

class AlarmClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Horloge, Réveil, Chronomètre et Minuteur")
        self.root.geometry('400x500')

        self.alarm_time = tk.StringVar()
        self.alarm_time.set("00:00")
        self.current_time = tk.StringVar()
        self.current_time.set(datetime.now().strftime('%H:%M:%S'))

        self.ringtone_options = [
            r"C:\Users\LATITUDE 5500\Downloads\Wave to mp3 maker plus 2.3 (Keygen music).mp3",
            r"C:\Users\LATITUDE 5500\Downloads\iPhone Marimba.mp3",
            r"C:\Users\LATITUDE 5500\Downloads\Taxi 4.mp3",
        ]
        self.selected_ringtone = tk.StringVar()
        self.selected_ringtone.set(self.ringtone_options[0])

        self.alarm_thread = None
        self.alarm_active = False

        self.chrono_active = False
        self.chrono_start_time = None
        self.chrono_time_var = tk.StringVar()
        self.chrono_time_var.set("00:00:00")

        self.timer_active = False
        self.timer_start_time = None
        self.timer_end_time = None
        self.timer_duration = tk.StringVar()
        self.timer_duration.set("00:00:00")

        pygame.init()

        self.create_ui()

    def create_ui(self):
        ttk.Style().configure('TButton', font=('calibri', 12, 'bold'))

        self.root.option_add('*TButton*highlightBackground', 'lightgray')
        self.root.option_add('*TButton*highlightColor', 'lightgray')

        self.create_alarm_frame()
        self.create_chrono_frame()
        self.create_timer_frame()

        self.update_current_time()
        self.update_chrono()
        self.update_timer()

    def create_alarm_frame(self):

        alarm_frame = ttk.Frame(self.root, padding=10)
        alarm_frame.pack(pady=10, fill='both', expand=True)

        ttk.Label(alarm_frame, text="Réveil", font=('calibri', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(alarm_frame, text="Heure du réveil (HH:MM):").grid(row=1, column=0, pady=5)
        ttk.Entry(alarm_frame, textvariable=self.alarm_time, font=('calibri', 14, 'bold')).grid(row=1, column=1, pady=5)

        ttk.Label(alarm_frame, text="Sonnerie:").grid(row=2, column=0, pady=5)
        ringtone_menu = ttk.Combobox(alarm_frame, textvariable=self.selected_ringtone, values=self.ringtone_options)
        ringtone_menu.grid(row=2, column=1, pady=5)

        ttk.Button(alarm_frame, text="Démarrer Réveil", command=self.start_alarm).grid(row=3, column=0, pady=10, padx=5)
        ttk.Button(alarm_frame, text="Arrêter Réveil", command=self.stop_alarm).grid(row=3, column=1, pady=10, padx=5)

        ttk.Button(alarm_frame, text="Play Sonnerie", command=self.play_ringtone).grid(row=5, column=0, pady=10, padx=5)
        ttk.Button(alarm_frame, text="Stop Sonnerie", command=self.stop_ringtone).grid(row=5, column=1, pady=10, padx=5)

        ttk.Label(alarm_frame, text="Heure actuelle:").grid(row=4, column=0, pady=5)
        ttk.Label(alarm_frame, textvariable=self.current_time, font=('calibri', 12, 'italic')).grid(row=4, column=1, pady=5)

    def create_chrono_frame(self):
        chrono_frame = ttk.Frame(self.root, padding=10)
        chrono_frame.pack(pady=10, fill='both', expand=True)

        ttk.Label(chrono_frame, text="Chronomètre", font=('calibri', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(chrono_frame, text="Chronomètre:").grid(row=1, column=0, pady=5)
        ttk.Label(chrono_frame, textvariable=self.chrono_time_var, font=('calibri', 14, 'bold')).grid(row=1, column=1, pady=5)

        ttk.Button(chrono_frame, text="Démarrer Chrono", command=self.start_chrono).grid(row=2, column=0, pady=10, padx=5)
        ttk.Button(chrono_frame, text="Arrêter Chrono", command=self.stop_chrono).grid(row=2, column=1, pady=10, padx=5)

        ttk.Label(chrono_frame, text="Heure actuelle:").grid(row=3, column=0, pady=5)
        ttk.Label(chrono_frame, textvariable=self.current_time, font=('calibri', 12, 'italic')).grid(row=3, column=1, pady=5)

    def create_timer_frame(self):
        timer_frame = ttk.Frame(self.root, padding=10)
        timer_frame.pack(pady=10, fill='both', expand=True)

        ttk.Label(timer_frame, text="Minuteur", font=('calibri', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(timer_frame, text="Durée Minuteur (MM:SS):").grid(row=1, column=0, pady=5)
        ttk.Entry(timer_frame, textvariable=self.timer_duration, font=('calibri', 14, 'bold')).grid(row=1, column=1, pady=5)

        ttk.Button(timer_frame, text="Démarrer Minuteur", command=self.start_timer).grid(row=2, column=0, pady=10, padx=5)
        ttk.Button(timer_frame, text="Arrêter Minuteur", command=self.stop_timer).grid(row=2, column=1, pady=10, padx=5)

        ttk.Label(timer_frame, text="Heure actuelle:").grid(row=3, column=0, pady=5)
        ttk.Label(timer_frame, textvariable=self.current_time, font=('calibri', 12, 'italic')).grid(row=3, column=1, pady=5)

    def update_current_time(self):
        current_time = datetime.now().strftime('%H:%M:%S')
        self.current_time.set(current_time)
        if self.alarm_active and datetime.now().time() >= self.alarm_time_obj.time():
            self.play_ringtone()
            self.alarm_active = False
            self.stop_alarm()
        self.root.after(1000, self.update_current_time)

    def start_alarm(self):
        alarm_time_str = self.alarm_time.get()

        try:
            self.alarm_time_obj = datetime.strptime(alarm_time_str, '%H:%M')
            current_time = datetime.now().time()

            if current_time < self.alarm_time_obj.time():
                messagebox.showinfo("Réveil", f"Réveil programmé à {alarm_time_str}.")
                self.alarm_active = True
                self.alarm_thread = threading.Thread(target=self.monitor_alarm)
                self.alarm_thread.start()
            else:
                messagebox.showwarning("Réveil", "L'heure du réveil doit être dans le futur.")

        except ValueError:
            messagebox.showerror("Erreur", "Format d'heure invalide. Utilisez HH:MM.")

    def monitor_alarm(self):
        while self.alarm_active:
            if datetime.now().time() >= self.alarm_time_obj.time():
                self.play_ringtone()
                self.alarm_active = False
                self.stop_alarm()

    def stop_alarm(self):
        messagebox.showinfo("Réveil", "Réveil arrêté.")

    def play_ringtone(self):
        selected_ringtone = self.selected_ringtone.get()
        pygame.mixer.music.load(selected_ringtone)
        pygame.mixer.music.play()

    def stop_ringtone(self):
        pygame.mixer.music.stop()

    def start_chrono(self):
        if not self.chrono_active:
            self.chrono_start_time = datetime.now()
            self.chrono_active = True
            self.update_chrono()

    def stop_chrono(self):
        if self.chrono_active:
            self.chrono_active = False

    def update_chrono(self):
        if self.chrono_active:
            elapsed_time = datetime.now() - self.chrono_start_time
            chrono_str = str(timedelta(seconds=int(elapsed_time.total_seconds())))
            self.chrono_time_var.set(chrono_str)
            self.root.after(1000, self.update_chrono)
        else:
            self.chrono_time_var.set("00:00:00")

    def start_timer(self):
        if not self.timer_active:
            timer_duration_str = self.timer_duration.get()

            try:
                timer_duration = timedelta(minutes=int(timer_duration_str[:2]), seconds=int(timer_duration_str[3:]))
                self.timer_start_time = datetime.now()
                self.timer_end_time = self.timer_start_time + timer_duration
                self.timer_active = True
                self.update_timer()

            except ValueError:
                messagebox.showerror("Erreur", "Format de minuteur invalide. Utilisez MM:SS.")

    def stop_timer(self):
        if self.timer_active:
            self.timer_active = False

    def update_timer(self):
        if self.timer_active:
            remaining_time = self.timer_end_time - datetime.now()
            timer_str = str(remaining_time).split('.')[0]
            self.timer_duration.set(timer_str)
            if remaining_time <= timedelta(0):
                self.timer_active = False
                self.play_ringtone()
                messagebox.showinfo("Minuteur", "Minuteur terminé.")
                self.timer_duration.set("00:00:00")
            else:
                self.root.after(1000, self.update_timer)
        else:
            self.timer_duration.set("00:00:00")

if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = AlarmClockApp(root)
    root.mainloop()
