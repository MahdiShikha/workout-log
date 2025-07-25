# Workout Log GUI with Stopwatch
# Provides simple interface to enter exercise, sets, reps and start/stop stopwatch.

import tkinter as tk
from tkinter import ttk, messagebox
import time


class Stopwatch:
    """Simple stopwatch timer."""

    def __init__(self, label: tk.Label):
        self.label = label
        self.running = False
        self.start_time = 0.0
        self.elapsed = 0.0
        self._update_job = None

    def _update(self):
        if self.running:
            self.elapsed = time.time() - self.start_time
            self.label.config(text=f"Time: {self.elapsed:.1f} s")
            self._update_job = self.label.after(100, self._update)

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed
            self.running = True
            self._update()

    def stop(self):
        if self.running:
            self.running = False
            if self._update_job:
                self.label.after_cancel(self._update_job)
                self._update_job = None

    def reset(self):
        self.stop()
        self.elapsed = 0.0
        self.label.config(text="Time: 0.0 s")


class WorkoutLogApp(tk.Tk):
    """Tkinter based GUI for logging workouts."""

    def __init__(self):
        super().__init__()
        self.title("Workout Log")

        # Layout
        self.timer_label = ttk.Label(self, text="Time: 0.0 s", font=("Arial", 14))
        self.timer_label.grid(row=0, column=0, columnspan=3, pady=5)

        self.stopwatch = Stopwatch(self.timer_label)

        ttk.Button(self, text="Start", command=self.stopwatch.start).grid(row=1, column=0, padx=5)
        ttk.Button(self, text="Stop", command=self.stopwatch.stop).grid(row=1, column=1, padx=5)
        ttk.Button(self, text="Reset", command=self.stopwatch.reset).grid(row=1, column=2, padx=5)

        # Exercise entry
        ttk.Label(self, text="Exercise").grid(row=2, column=0, pady=5)
        ttk.Label(self, text="Sets").grid(row=2, column=1)
        ttk.Label(self, text="Reps per set\n(comma separated)").grid(row=2, column=2)

        self.exercise_var = tk.StringVar()
        self.sets_var = tk.StringVar()
        self.reps_var = tk.StringVar()

        ttk.Entry(self, textvariable=self.exercise_var).grid(row=3, column=0, padx=5)
        ttk.Entry(self, textvariable=self.sets_var, width=5).grid(row=3, column=1, padx=5)
        ttk.Entry(self, textvariable=self.reps_var, width=5).grid(row=3, column=2, padx=5)

        ttk.Button(self, text="Add Entry", command=self.add_entry).grid(row=4, column=0, columnspan=3, pady=5)

        # Log display
        self.log_text = tk.Text(self, height=10, width=40)
        self.log_text.grid(row=5, column=0, columnspan=3, pady=5)

    def add_entry(self):
        exercise = self.exercise_var.get().strip()
        sets_text = self.sets_var.get().strip()
        reps_text = self.reps_var.get().strip()

        if not (exercise and sets_text and reps_text):
            return

        try:
            sets = int(sets_text)
        except ValueError:
            messagebox.showerror("Invalid Sets", "Sets must be a number")
            return

        reps_list = [r.strip() for r in reps_text.split(',') if r.strip()]
        if len(reps_list) != sets:
            messagebox.showerror(
                "Mismatch",
                "Number of reps values must match number of sets",
            )
            return

        entry = f"{exercise}: " + \
            ", ".join(f"Set {i+1}: {rep} reps" for i, rep in enumerate(reps_list)) + "\n"
        self.log_text.insert(tk.END, entry)

        self.exercise_var.set("")
        self.sets_var.set("")
        self.reps_var.set("")


if __name__ == "__main__":
    app = WorkoutLogApp()
    app.mainloop()
