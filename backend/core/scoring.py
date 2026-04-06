import time
from textblob import TextBlob

class TypingScorer:
    def __init__(self):
        pass
    
    def calculate_wpm(self, typed_text, time_taken):
        """
        Calculate Words Per Minute (WPM)
        Assumes 5 characters per word
        
        Args:
            typed_text (str): Text typed by user
            time_taken (float): Time taken in seconds
            
        Returns:
            float: WPM score
        """
        words_typed = len(typed_text) / 5
        minutes = time_taken / 60
        wpm = words_typed / minutes if minutes > 0 else 0
        return round(wpm, 2)
    
    def calculate_accuracy(self, original_text, typed_text):
        """
        Calculate typing accuracy percentage
        
        Args:
            original_text (str): Original text to type
            typed_text (str): Text typed by user
            
        Returns:
            float: Accuracy percentage
        """
        if not typed_text:
            return 0.0
            
        correct_chars = 0
        min_length = min(len(original_text), len(typed_text))
        
        for i in range(min_length):
            if original_text[i] == typed_text[i]:
                correct_chars += 1
                
        accuracy = (correct_chars / len(typed_text)) * 100 if len(typed_text) > 0 else 0
        return round(accuracy, 2)
    
    def count_mistakes(self, original_text, typed_text):
        """
        Count typing mistakes
        
        Args:
            original_text (str): Original text to type
            typed_text (str): Text typed by user
            
        Returns:
            int: Number of mistakes
        """
        mistakes = 0
        max_length = max(len(original_text), len(typed_text))
        
        for i in range(max_length):
            # If typed text is shorter than original, count missing characters as mistakes
            if i >= len(typed_text):
                mistakes += 1
            # If original text is shorter, extra characters are mistakes
            elif i >= len(original_text):
                mistakes += 1
            # Compare characters
            elif original_text[i] != typed_text[i]:
                mistakes += 1
                
        return mistakes
    
    def analyze_readability(self, text):
        """
        Analyze text readability using TextBlob
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Readability metrics
        """
        blob = TextBlob(text)
        
        # Calculate average sentence length
        sentences = blob.sentences
        if not sentences:
            return {"readability_score": 0, "sentence_count": 0, "avg_sentence_length": 0}
            
        total_words = len(blob.words)
        sentence_count = len(sentences)
        avg_sentence_length = total_words / sentence_count if sentence_count > 0 else 0
        
        # Simple readability score (higher for more complex text)
        # Based on average sentence length and syllable count
        total_syllables = sum([self._count_syllables(word) for word in blob.words])
        avg_syllables_per_word = total_syllables / len(blob.words) if len(blob.words) > 0 else 0
        
        # Simplified readability score (0-100 scale)
        readability_score = min(100, max(0, 
            50 + (avg_sentence_length * 1.5) + (avg_syllables_per_word * 10)))
        
        return {
            "readability_score": round(readability_score, 2),
            "sentence_count": sentence_count,
            "avg_sentence_length": round(avg_sentence_length, 2),
            "avg_syllables_per_word": round(avg_syllables_per_word, 2)
        }
    
    def _count_syllables(self, word):
        """
        Count syllables in a word (simplified approach)
        
        Args:
            word (str): Word to count syllables for
            
        Returns:
            int: Syllable count
        """
        word = word.lower()
        vowels = "aeiouy"
        syllable_count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = is_vowel
            
        # Handle silent 'e' at the end
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
            
        return max(1, syllable_count)

# Example usage
if __name__ == "__main__":
    scorer = TypingScorer()
    
    original = "The quick brown fox jumps over the lazy dog"
    typed = "The quik brown fox jumps over the lazy dog"
    
    wpm = scorer.calculate_wpm(typed, 30)  # 30 seconds
    accuracy = scorer.calculate_accuracy(original, typed)
    mistakes = scorer.count_mistakes(original, typed)
    readability = scorer.analyze_readability(original)
    
    print(f"WPM: {wpm}")
    print(f"Accuracy: {accuracy}%")
    print(f"Mistakes: {mistakes}")
    print(f"Readability: {readability}")