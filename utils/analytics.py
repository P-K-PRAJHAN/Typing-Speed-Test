import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from utils.database import DatabaseManager

class AnalyticsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseManager()
        self.window = None
        
    def show_analytics(self):
        # Create analytics window
        self.window = tk.Toplevel(self.parent)
        self.window.title("Performance Analytics")
        self.window.geometry("900x700")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # WPM Over Time Tab
        wpm_frame = ttk.Frame(notebook)
        notebook.add(wpm_frame, text="WPM Over Time")
        self.create_wpm_chart(wpm_frame)
        
        # Accuracy Over Time Tab
        accuracy_frame = ttk.Frame(notebook)
        notebook.add(accuracy_frame, text="Accuracy Over Time")
        self.create_accuracy_chart(accuracy_frame)
        
        # Comparison Tab
        comparison_frame = ttk.Frame(notebook)
        notebook.add(comparison_frame, text="Performance by Difficulty")
        self.create_comparison_chart(comparison_frame)
        
    def create_wpm_chart(self, parent):
        # Get data from database
        history = self.db.get_test_history()
        if not history:
            ttk.Label(parent, text="No data available").pack(pady=20)
            return
            
        dates = [record[1].split('T')[0] for record in history]  # Extract date part
        wpms = [record[3] for record in history]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dates, wpms, marker='o', linewidth=2, markersize=6)
        ax.set_title("Words Per Minute Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("WPM")
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_accuracy_chart(self, parent):
        # Get data from database
        history = self.db.get_test_history()
        if not history:
            ttk.Label(parent, text="No data available").pack(pady=20)
            return
            
        dates = [record[1].split('T')[0] for record in history]  # Extract date part
        accuracies = [record[4] for record in history]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dates, accuracies, marker='s', color='green', linewidth=2, markersize=6)
        ax.set_title("Accuracy Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Accuracy (%)")
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_comparison_chart(self, parent):
        # Get average stats by difficulty
        difficulties = ["easy", "medium", "hard"]
        avg_wpms = []
        avg_accuracies = []
        
        for difficulty in difficulties:
            stats = self.db.get_average_stats(difficulty)
            if stats and stats[0]:  # Check if stats exist and first value is not None
                avg_wpms.append(stats[0])
                avg_accuracies.append(stats[1])
            else:
                avg_wpms.append(0)
                avg_accuracies.append(0)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        x_pos = range(len(difficulties))
        
        # Create bar chart
        bar_width = 0.35
        bars1 = ax.bar([x - bar_width/2 for x in x_pos], avg_wpms, bar_width, 
                      label='WPM', alpha=0.8)
        bars2 = ax.bar([x + bar_width/2 for x in x_pos], avg_accuracies, bar_width, 
                      label='Accuracy (%)', alpha=0.8)
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
                        
        for bar in bars2:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        ax.set_title("Average Performance by Difficulty")
        ax.set_xlabel("Difficulty Level")
        ax.set_ylabel("Value")
        ax.set_xticks(x_pos)
        ax.set_xticklabels(difficulties)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)