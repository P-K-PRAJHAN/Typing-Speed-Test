import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AnalyticsEngine:
    def __init__(self, charts_dir="charts"):
        self.charts_dir = charts_dir
        # Create charts directory if it doesn't exist
        if not os.path.exists(charts_dir):
            os.makedirs(charts_dir)
    
    def generate_wpm_trend_chart(self, test_data, user_id):
        """
        Generate WPM trend chart over time
        
        Args:
            test_data (list): List of test results
            user_id (str): User identifier
            
        Returns:
            str: Path to generated chart
        """
        try:
            # Convert to DataFrame
            df = pd.DataFrame(test_data if test_data else [{'timestamp': datetime.now(), 'wpm': 0}])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Create the plot
            plt.figure(figsize=(10, 6))
            plt.plot(df['timestamp'], df['wpm'], marker='o', linewidth=2, markersize=6)
            plt.title("Words Per Minute Over Time")
            plt.xlabel("Date")
            plt.ylabel("WPM")
            plt.grid(True, alpha=0.3)
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45, ha="right")
            
            # Save chart
            filename = f"wpm_trend_{user_id}_{int(datetime.now().timestamp())}.png"
            filepath = os.path.join(self.charts_dir, filename)
            plt.tight_layout()
            plt.savefig(filepath)
            plt.close()
            
            return filepath
        except Exception as e:
            print(f"Error generating WPM trend chart: {e}")
            # Close any open figures to prevent memory leaks
            plt.close('all')
            return None
    
    def generate_accuracy_chart(self, test_data, user_id):
        """
        Generate accuracy trend chart
        
        Args:
            test_data (list): List of test results
            user_id (str): User identifier
            
        Returns:
            str: Path to generated chart
        """
        try:
            # Convert to DataFrame
            df = pd.DataFrame(test_data if test_data else [{'timestamp': datetime.now(), 'accuracy': 0}])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Create the plot
            plt.figure(figsize=(10, 6))
            plt.plot(df['timestamp'], df['accuracy'], marker='s', color='green', linewidth=2, markersize=6)
            plt.title("Accuracy Over Time")
            plt.xlabel("Date")
            plt.ylabel("Accuracy (%)")
            plt.grid(True, alpha=0.3)
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45, ha="right")
            
            # Save chart
            filename = f"accuracy_trend_{user_id}_{int(datetime.now().timestamp())}.png"
            filepath = os.path.join(self.charts_dir, filename)
            plt.tight_layout()
            plt.savefig(filepath)
            plt.close()
            
            return filepath
        except Exception as e:
            print(f"Error generating accuracy chart: {e}")
            # Close any open figures to prevent memory leaks
            plt.close('all')
            return None
    
    def generate_difficulty_comparison_chart(self, test_data, user_id):
        """
        Generate performance comparison by difficulty
        
        Args:
            test_data (list): List of test results
            user_id (str): User identifier
            
        Returns:
            str: Path to generated chart
        """
        try:
            # Convert to DataFrame
            df = pd.DataFrame(test_data if test_data else [
                {'difficulty': 'Easy', 'wpm': 0, 'accuracy': 0},
                {'difficulty': 'Medium', 'wpm': 0, 'accuracy': 0},
                {'difficulty': 'Hard', 'wpm': 0, 'accuracy': 0}
            ])
            
            # Calculate averages by difficulty
            difficulty_stats = df.groupby('difficulty').agg({
                'wpm': 'mean',
                'accuracy': 'mean'
            }).reset_index()
            
            # Create the plot
            fig, ax = plt.subplots(figsize=(10, 6))
            x_pos = np.arange(len(difficulty_stats))
            bar_width = 0.35
            
            bars1 = ax.bar(x_pos - bar_width/2, difficulty_stats['wpm'], bar_width, 
                          label='WPM', alpha=0.8)
            bars2 = ax.bar(x_pos + bar_width/2, difficulty_stats['accuracy'], bar_width, 
                          label='Accuracy (%)', alpha=0.8)
            
            # Add value labels on bars
            for bar in bars1:
                height = bar.get_height()
                ax.annotate(f'{height:.1f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom')
                            
            for bar in bars2:
                height = bar.get_height()
                ax.annotate(f'{height:.1f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom')
            
            ax.set_title("Average Performance by Difficulty")
            ax.set_xlabel("Difficulty Level")
            ax.set_ylabel("Value")
            ax.set_xticks(x_pos)
            ax.set_xticklabels(difficulty_stats['difficulty'])
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Save chart
            filename = f"difficulty_comparison_{user_id}_{int(datetime.now().timestamp())}.png"
            filepath = os.path.join(self.charts_dir, filename)
            plt.tight_layout()
            plt.savefig(filepath)
            plt.close()
            
            return filepath
        except Exception as e:
            print(f"Error generating difficulty comparison chart: {e}")
            # Close any open figures to prevent memory leaks
            plt.close('all')
            return None
    
    def generate_error_distribution_chart(self, test_data, user_id):
        """
        Generate error distribution chart
        
        Args:
            test_data (list): List of test results
            user_id (str): User identifier
            
        Returns:
            str: Path to generated chart
        """
        try:
            # Convert to DataFrame
            df = pd.DataFrame(test_data if test_data else [{'total_errors': 0}])
            
            # Create the plot
            plt.figure(figsize=(10, 6))
            plt.hist(df['total_errors'], bins=10, color='red', alpha=0.7, edgecolor='black')
            plt.title("Error Distribution")
            plt.xlabel("Number of Errors")
            plt.ylabel("Frequency")
            plt.grid(True, alpha=0.3)
            
            # Save chart
            filename = f"error_distribution_{user_id}_{int(datetime.now().timestamp())}.png"
            filepath = os.path.join(self.charts_dir, filename)
            plt.tight_layout()
            plt.savefig(filepath)
            plt.close()
            
            return filepath
        except Exception as e:
            print(f"Error generating error distribution chart: {e}")
            # Close any open figures to prevent memory leaks
            plt.close('all')
            return None
    
    def generate_wpm_vs_accuracy_scatter(self, test_data, user_id):
        """
        Generate scatter plot of WPM vs Accuracy
        
        Args:
            test_data (list): List of test results
            user_id (str): User identifier
            
        Returns:
            str: Path to generated chart
        """
        try:
            # Convert to DataFrame
            df = pd.DataFrame(test_data if test_data else [{'wpm': 0, 'accuracy': 0}])
            
            # Create the plot
            plt.figure(figsize=(10, 6))
            plt.scatter(df['wpm'], df['accuracy'], alpha=0.7, s=60)
            plt.title("WPM vs Accuracy")
            plt.xlabel("Words Per Minute (WPM)")
            plt.ylabel("Accuracy (%)")
            plt.grid(True, alpha=0.3)
            
            # Save chart
            filename = f"wpm_vs_accuracy_{user_id}_{int(datetime.now().timestamp())}.png"
            filepath = os.path.join(self.charts_dir, filename)
            plt.tight_layout()
            plt.savefig(filepath)
            plt.close()
            
            return filepath
        except Exception as e:
            print(f"Error generating WPM vs accuracy scatter chart: {e}")
            # Close any open figures to prevent memory leaks
            plt.close('all')
            return None
    
    def analyze_mistake_patterns(self, test_data):
        """
        Analyze common mistake patterns
        
        Args:
            test_data (list): List of test results
            
        Returns:
            dict: Analysis results
        """
        try:
            # Handle case with no test data
            if not test_data:
                return {
                    "average_wpm": 0,
                    "average_accuracy": 0,
                    "average_errors": 0,
                    "wpm_trend": "no data",
                    "accuracy_trend": "no data",
                    "total_tests": 0
                }
                
            # Convert to DataFrame
            df = pd.DataFrame(test_data)
            
            # Calculate average metrics
            avg_wpm = df['wpm'].mean() if not df.empty else 0
            avg_accuracy = df['accuracy'].mean() if not df.empty else 0
            avg_errors = df['total_errors'].mean() if not df.empty else 0
            
            # Identify trends
            recent_tests = df.tail(5)  # Last 5 tests
            if len(recent_tests) > 1:
                wpm_trend = "improving" if recent_tests['wpm'].iloc[-1] > recent_tests['wpm'].iloc[0] else "declining"
                accuracy_trend = "improving" if recent_tests['accuracy'].iloc[-1] > recent_tests['accuracy'].iloc[0] else "declining"
            else:
                wpm_trend = "insufficient data"
                accuracy_trend = "insufficient data"
            
            return {
                "average_wpm": round(avg_wpm, 2),
                "average_accuracy": round(avg_accuracy, 2),
                "average_errors": round(avg_errors, 2),
                "wpm_trend": wpm_trend,
                "accuracy_trend": accuracy_trend,
                "total_tests": len(test_data)
            }
        except Exception as e:
            print(f"Error analyzing mistake patterns: {e}")
            return {
                "average_wpm": 0,
                "average_accuracy": 0,
                "average_errors": 0,
                "wpm_trend": "error",
                "accuracy_trend": "error",
                "total_tests": 0
            }
    
    def predict_difficulty_match(self, text, user_history):
        """
        Predict how well a text matches a user's skill level using TF-IDF and cosine similarity
        
        Args:
            text (str): Text to evaluate
            user_history (list): User's test history
            
        Returns:
            dict: Prediction results
        """
        try:
            if not user_history:
                return {"match_score": 0.5, "recommended_difficulty": "medium"}
            
            # Extract texts from user history
            historical_texts = [test.get('text', '') for test in user_history if test.get('text')]
            if not historical_texts:
                return {"match_score": 0.5, "recommended_difficulty": "medium"}
            
            # Combine all texts for TF-IDF
            all_texts = historical_texts + [text]
            
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
            tfidf_matrix = vectorizer.fit_transform(all_texts)
            
            # Calculate cosine similarity between the new text and historical texts
            similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
            
            # Average similarity score
            avg_similarity = np.mean(similarity_scores)
            
            # Map similarity to difficulty recommendation
            if avg_similarity > 0.7:
                recommended_difficulty = "easy"
            elif avg_similarity > 0.4:
                recommended_difficulty = "medium"
            else:
                recommended_difficulty = "hard"
            
            return {
                "match_score": round(float(avg_similarity), 4),
                "recommended_difficulty": recommended_difficulty
            }
        except Exception as e:
            print(f"Error predicting difficulty match: {e}")
            return {"match_score": 0.5, "recommended_difficulty": "medium"}

# Example usage
if __name__ == "__main__":
    # Sample test data
    sample_data = [
        {
            "user_id": "user123",
            "difficulty": "easy",
            "wpm": 45,
            "accuracy": 92.5,
            "total_errors": 3,
            "timestamp": "2023-01-01T10:00:00Z"
        },
        {
            "user_id": "user123",
            "difficulty": "medium",
            "wpm": 38,
            "accuracy": 87.2,
            "total_errors": 7,
            "timestamp": "2023-01-02T10:00:00Z"
        },
        {
            "user_id": "user123",
            "difficulty": "hard",
            "wpm": 32,
            "accuracy": 81.8,
            "total_errors": 12,
            "timestamp": "2023-01-03T10:00:00Z"
        }
    ]
    
    analytics = AnalyticsEngine()
    
    # Generate charts
    wpm_chart = analytics.generate_wpm_trend_chart(sample_data, "user123")
    accuracy_chart = analytics.generate_accuracy_chart(sample_data, "user123")
    difficulty_chart = analytics.generate_difficulty_comparison_chart(sample_data, "user123")
    error_chart = analytics.generate_error_distribution_chart(sample_data, "user123")
    scatter_chart = analytics.generate_wpm_vs_accuracy_scatter(sample_data, "user123")
    
    print(f"WPM Chart: {wpm_chart}")
    print(f"Accuracy Chart: {accuracy_chart}")
    print(f"Difficulty Chart: {difficulty_chart}")
    print(f"Error Chart: {error_chart}")
    print(f"Scatter Chart: {scatter_chart}")
    
    # Analyze patterns
    patterns = analytics.analyze_mistake_patterns(sample_data)
    print(f"Patterns: {patterns}")