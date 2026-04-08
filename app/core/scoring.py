import re

class ScoringEngine:
    @staticmethod
    def calculate_wpm(typed_text, time_seconds):
        """Calculate words per minute (WPM)"""
        # Standard word is 5 characters including spaces and punctuation
        words_typed = len(typed_text) / 5
        minutes = time_seconds / 60
        return round(words_typed / minutes, 1) if minutes > 0 else 0
    
    @staticmethod
    def calculate_accuracy(original_text, typed_text):
        """Calculate typing accuracy percentage"""
        if not original_text or not typed_text:
            return 0.0
        
        correct_chars = 0
        min_len = min(len(original_text), len(typed_text))
        
        for i in range(min_len):
            if original_text[i] == typed_text[i]:
                correct_chars += 1
        
        # Add remaining characters if original is longer
        correct_chars += max(0, len(original_text) - len(typed_text))
        
        total_chars = max(len(original_text), len(typed_text))
        return round((correct_chars / total_chars) * 100, 2) if total_chars > 0 else 0
    
    @staticmethod
    def count_errors(original_text, typed_text):
        """Count the number of errors in typed text"""
        errors = 0
        min_len = min(len(original_text), len(typed_text))
        
        for i in range(min_len):
            if original_text[i] != typed_text[i]:
                errors += 1
        
        # Add extra characters as errors
        errors += abs(len(typed_text) - len(original_text))
        
        return errors
    
    @staticmethod
    def calculate_score(original_text, typed_text, time_seconds):
        """Calculate all metrics for a typing test"""
        wpm = ScoringEngine.calculate_wpm(typed_text, time_seconds)
        accuracy = ScoringEngine.calculate_accuracy(original_text, typed_text)
        errors = ScoringEngine.count_errors(original_text, typed_text)
        
        return {
            'wpm': wpm,
            'accuracy': accuracy,
            'errors': errors,
            'time_taken': time_seconds,
            'text_length': len(original_text)
        }
