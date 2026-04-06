import markovify
import random

class AITextGenerator:
    def __init__(self):
        # Sample texts for different difficulty levels
        self.easy_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Python is a versatile programming language.",
            "Typing practice improves your skills over time.",
            "Consistent effort leads to significant improvement.",
            "Simple exercises help build foundational skills."
        ]
        
        self.medium_texts = [
            "Python's syntax is clean and readable, making it ideal for beginners and experts alike.",
            "Object-oriented programming allows developers to create reusable code structures.",
            "Database management systems efficiently store and retrieve large amounts of information.",
            "Web development frameworks simplify the process of building complex applications.",
            "Machine learning algorithms can identify patterns in large datasets automatically."
        ]
        
        self.hard_texts = [
            "The implementation of asynchronous programming paradigms in distributed systems requires careful consideration of concurrency control mechanisms.",
            "Cryptographic protocols ensure secure communication by employing mathematical algorithms that protect data integrity and confidentiality.",
            "Computational linguistics combines computer science and linguistics to process natural language through algorithmic techniques.",
            "Quantum computing leverages quantum mechanical phenomena to perform computations that would be infeasible for classical computers.",
            "Artificial neural networks simulate biological neural structures to enable machine learning through layered computational models."
        ]
        
        # Build Markov models for each difficulty level
        self.easy_model = markovify.Text(" ".join(self.easy_texts))
        self.medium_model = markovify.Text(" ".join(self.medium_texts))
        self.hard_model = markovify.Text(" ".join(self.hard_texts))
    
    def generate_text(self, difficulty="easy", sentences=3):
        """
        Generate text based on difficulty level using Markov chains or template-based approach
        
        Args:
            difficulty (str): Difficulty level ('easy', 'medium', 'hard')
            sentences (int): Number of sentences to generate
            
        Returns:
            str: Generated text
        """
        if difficulty == "easy":
            model = self.easy_model
        elif difficulty == "medium":
            model = self.medium_model
        elif difficulty == "hard":
            model = self.hard_model
        else:
            # Default to easy if invalid difficulty
            model = self.easy_model
            
        # Generate sentences
        generated_sentences = []
        for _ in range(sentences):
            sentence = model.make_sentence()
            if sentence:
                generated_sentences.append(sentence)
                
        # If Markov generation failed, fall back to template-based approach
        if not generated_sentences:
            if difficulty == "easy":
                return random.choice(self.easy_texts)
            elif difficulty == "medium":
                return random.choice(self.medium_texts)
            else:
                return random.choice(self.hard_texts)
                
        return " ".join(generated_sentences)

# Example usage
if __name__ == "__main__":
    generator = AITextGenerator()
    print("Easy:", generator.generate_text("easy"))
    print("Medium:", generator.generate_text("medium"))
    print("Hard:", generator.generate_text("hard"))