import random

class AITextGenerator:
    @staticmethod
    def generate_text(level="medium"):
        """Generate sample text based on difficulty level"""
        easy_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Pack my box with five dozen liquor jugs.",
            "How vexingly quick daft zebras jump!",
            "Bright vixens jump; dozy fowl quack.",
            "The five boxing wizards jump quickly."
        ]
        
        medium_texts = [
            "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. How vexingly quick daft zebras jump! Bright vixens jump; dozy fowl quack. The five boxing wizards jump quickly.",
            "The journey of a thousand miles begins with a single step. Success is not final, failure is not fatal: It is the courage to continue that counts. The only way to do great work is to love what you do. In the middle of every difficulty lies opportunity.",
            "To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune, or to take arms against a sea of troubles and by opposing end them.",
            "The only thing necessary for the triumph of evil is for good men to do nothing. The best way to predict the future is to invent it. In three words I can sum up everything I've learned about life: it goes on."
        ]
        
        hard_texts = [
            "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. How vexingly quick daft zebras jump! Bright vixens jump; dozy fowl quack. The five boxing wizards jump quickly. The journey of a thousand miles begins with a single step. Success is not final, failure is not fatal: It is the courage to continue that counts. The only way to do great work is to love what you do. In the middle of every difficulty lies opportunity. To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune, or to take arms against a sea of troubles and by opposing end them. The only thing necessary for the triumph of evil is for good men to do nothing. The best way to predict the future is to invent it. In three words I can sum up everything I've learned about life: it goes on.",
            "The concept of artificial intelligence dates back to classical antiquity, with myths, stories, and rumors of artificial beings endowed with intelligence or consciousness by master craftsmen. The seeds of modern AI were planted by classical philosophers who attempted to describe the process of human thinking as the mechanical manipulation of symbols. This work culminated in the invention of the programmable digital computer in the 1940s, a machine based on the abstract essence of mathematical reasoning. This device and the ideas behind it inspired a handful of scientists to begin seriously discussing the possibility of building an electronic brain.",
            "Quantum mechanics is a fundamental theory in physics that provides a description of the physical properties of nature at the scale of atoms and subatomic particles. It is the foundation of all quantum physics including quantum chemistry, quantum field theory, quantum technology, and quantum information science. Classical physics, the description of physics that existed before the theory of relativity and quantum mechanics, describes many aspects of nature at an ordinary (macroscopic) scale, while quantum mechanics explains the aspects of nature at small (atomic and subatomic) scales."
        ]
        
        if level.lower() == "easy":
            return random.choice(easy_texts)
        elif level.lower() == "hard":
            return random.choice(hard_texts)
        else:  # medium
            return random.choice(medium_texts)
