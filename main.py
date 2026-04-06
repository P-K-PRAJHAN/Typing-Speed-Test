import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading
from utils.database import DatabaseManager
from utils.texts import TEXTS
from utils.analytics import AnalyticsWindow

class TypingSpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize database
        self.db = DatabaseManager()
        
        # Game state variables
        self.current_text = ""
        self.start_time = None
        self.timer_running = False
        self.difficulty = "easy"
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="Typing Speed Test", 
                               font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Difficulty selection
        difficulty_frame = ttk.LabelFrame(self.main_frame, text="Select Difficulty", padding="10")
        difficulty_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.difficulty_var = tk.StringVar(value="easy")
        ttk.Radiobutton(difficulty_frame, text="Easy", variable=self.difficulty_var, 
                       value="easy", command=self.set_difficulty).grid(row=0, column=0, padx=10)
        ttk.Radiobutton(difficulty_frame, text="Medium", variable=self.difficulty_var, 
                       value="medium", command=self.set_difficulty).grid(row=0, column=1, padx=10)
        ttk.Radiobutton(difficulty_frame, text="Hard", variable=self.difficulty_var, 
                       value="hard", command=self.set_difficulty).grid(row=0, column=2, padx=10)
        
        # Text display
        text_frame = ttk.LabelFrame(self.main_frame, text="Text to Type", padding="10")
        text_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.text_display = tk.Text(text_frame, height=6, wrap=tk.WORD, 
                                   state=tk.DISABLED, bg="#f0f0f0", font=("Arial", 12))
        self.text_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for text display
        text_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_display.yview)
        text_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.text_display.configure(yscrollcommand=text_scrollbar.set)
        
        # User input
        input_frame = ttk.LabelFrame(self.main_frame, text="Your Typing", padding="10")
        input_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        input_frame.columnconfigure(0, weight=1)
        
        self.user_input = tk.Text(input_frame, height=6, wrap=tk.WORD, 
                                 font=("Arial", 12), undo=True)
        self.user_input.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.user_input.bind("<KeyPress>", self.on_key_press)
        
        # Scrollbar for user input
        input_scrollbar = ttk.Scrollbar(input_frame, orient=tk.VERTICAL, command=self.user_input.yview)
        input_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.user_input.configure(yscrollcommand=input_scrollbar.set)
        
        # Stats frame
        stats_frame = ttk.Frame(self.main_frame)
        stats_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Timer
        self.timer_label = ttk.Label(stats_frame, text="Time: 0s", font=("Arial", 12))
        self.timer_label.grid(row=0, column=0, padx=(0, 20))
        
        # WPM
        self.wpm_label = ttk.Label(stats_frame, text="WPM: 0", font=("Arial", 12))
        self.wpm_label.grid(row=0, column=1, padx=(0, 20))
        
        # Accuracy
        self.accuracy_label = ttk.Label(stats_frame, text="Accuracy: 0%", font=("Arial", 12))
        self.accuracy_label.grid(row=0, column=2, padx=(0, 20))
        
        # Mistakes
        self.mistakes_label = ttk.Label(stats_frame, text="Mistakes: 0", font=("Arial", 12))
        self.mistakes_label.grid(row=0, column=3)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=3, pady=(0, 20))
        
        self.start_button = ttk.Button(buttons_frame, text="Start Test", command=self.start_test)
        self.start_button.grid(row=0, column=0, padx=10)
        
        self.reset_button = ttk.Button(buttons_frame, text="Reset", command=self.reset_test)
        self.reset_button.grid(row=0, column=1, padx=10)
        
        self.history_button = ttk.Button(buttons_frame, text="View History", command=self.show_history)
        self.history_button.grid(row=0, column=2, padx=10)
        
        self.analytics_button = ttk.Button(buttons_frame, text="Analytics", command=self.show_analytics)
        self.analytics_button.grid(row=0, column=3, padx=10)
        
        # Load initial text
        self.load_random_text()
        
    def set_difficulty(self):
        self.difficulty = self.difficulty_var.get()
        if not self.timer_running:
            self.load_random_text()
            
    def load_random_text(self):
        texts = TEXTS[self.difficulty]
        self.current_text = random.choice(texts)
        
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(1.0, self.current_text)
        self.text_display.config(state=tk.DISABLED)
        
    def start_test(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.user_input.delete(1.0, tk.END)
            self.user_input.focus_set()
            self.start_button.config(state=tk.DISABLED)
            self.update_timer()
            
    def reset_test(self):
        self.timer_running = False
        self.start_time = None
        self.start_button.config(state=tk.NORMAL)
        self.timer_label.config(text="Time: 0s")
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 0%")
        self.mistakes_label.config(text="Mistakes: 0")
        self.user_input.delete(1.0, tk.END)
        self.load_random_text()
        
    def on_key_press(self, event):
        if not self.timer_running and event.keysym not in ['Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R']:
            self.start_test()
        elif self.timer_running:
            # Update stats as user types
            self.root.after(100, self.update_stats)
            
    def update_stats(self):
        if not self.timer_running:
            return
            
        user_text = self.user_input.get(1.0, tk.END).strip()
        elapsed_time = time.time() - self.start_time
        
        # Calculate WPM (words per minute)
        # Assuming 5 characters per word
        words_typed = len(user_text) / 5
        minutes = elapsed_time / 60
        wpm = words_typed / minutes if minutes > 0 else 0
        
        # Calculate accuracy
        correct_chars = 0
        mistakes = 0
        for i, char in enumerate(user_text):
            if i < len(self.current_text) and char == self.current_text[i]:
                correct_chars += 1
            else:
                mistakes += 1
        
        total_chars = len(user_text)
        accuracy = (correct_chars / total_chars * 100) if total_chars > 0 else 0
        
        # Update labels
        self.timer_label.config(text=f"Time: {int(elapsed_time)}s")
        self.wpm_label.config(text=f"WPM: {int(wpm)}")
        self.accuracy_label.config(text=f"Accuracy: {int(accuracy)}%")
        self.mistakes_label.config(text=f"Mistakes: {mistakes}")
        
        # Check if test is complete
        if len(user_text) >= len(self.current_text):
            self.finish_test(wpm, accuracy, mistakes, elapsed_time)
            
    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}s")
            self.root.after(1000, self.update_timer)
            
    def finish_test(self, wpm, accuracy, mistakes, duration):
        self.timer_running = False
        self.start_button.config(state=tk.NORMAL)
        
        # Save result to database
        self.db.save_test_result(self.difficulty, wpm, accuracy, mistakes, duration)
        
        # Show result
        messagebox.showinfo("Test Complete", 
                           f"Test completed!\n\n"
                           f"Difficulty: {self.difficulty.capitalize()}\n"
                           f"WPM: {int(wpm)}\n"
                           f"Accuracy: {int(accuracy)}%\n"
                           f"Mistakes: {mistakes}\n"
                           f"Time: {int(duration)}s")
                           
    def show_history(self):
        # Open history window
        history_window = tk.Toplevel(self.root)
        history_window.title("Typing Test History")
        history_window.geometry("800x500")
        
        # Create treeview for history
        columns = ("Date", "Difficulty", "WPM", "Accuracy", "Mistakes", "Duration")
        tree = ttk.Treeview(history_window, columns=columns, show="headings")
        
        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
            
        # Add scrollbar
        scrollbar = ttk.Scrollbar(history_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        # Pack elements
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load history data
        history_data = self.db.get_test_history()
        for record in history_data:
            tree.insert("", tk.END, values=(record[1], record[2], int(record[3]), 
                                          f"{int(record[4])}%", record[5], f"{int(record[6])}s"))

    def show_analytics(self):
        # Open analytics window
        analytics = AnalyticsWindow(self.root)
        analytics.show_analytics()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTestApp(root)
    root.mainloop()