import random

class FeedbackEngine:
    @staticmethod
    def generate_feedback(test_result, previous_results):
        """Generate feedback based on test results"""
        feedback = []
        
        # Basic feedback
        if test_result.accuracy >= 95:
            feedback.append("Excellent accuracy! Your typing precision is top-notch.")
        elif test_result.accuracy >= 85:
            feedback.append("Good accuracy! You're doing well, but there's still room for improvement.")
        else:
            feedback.append("Focus on accuracy. Try to reduce errors for better performance.")
        
        # WPM feedback
        if test_result.wpm > 60:
            feedback.append("Impressive speed! You're typing faster than average.")
        elif test_result.wpm > 40:
            feedback.append("Good speed! With practice, you can go even faster.")
        else:
            feedback.append("Keep practicing to improve your typing speed. Speed will come with time.")
        
        # Compare with previous results if available
        if previous_results:
            if len(previous_results) >= 2:
                last_result = previous_results[-1]
                prev_result = previous_results[-2]
                
                wpm_diff = last_result.wpm - prev_result.wpm
                accuracy_diff = last_result.accuracy - prev_result.accuracy
                
                if wpm_diff > 5:
                    feedback.append(f"Great progress! Your speed improved by {wpm_diff:.1f} WPM since your last test.")
                elif wpm_diff < -2:
                    feedback.append(f"Your speed decreased by {abs(wpm_diff):.1f} WPM. Try to maintain a steady pace.")
                
                if accuracy_diff > 5:
                    feedback.append(f"Your accuracy improved by {accuracy_diff:.1f}%! Keep it up!")
                elif accuracy_diff < -2:
                    feedback.append(f"Your accuracy dropped by {abs(accuracy_diff):.1f}%. Focus on precision.")
        
        # Difficulty-specific tips
        if test_result.difficulty.lower() == "easy":
            feedback.append("Ready to try a medium difficulty test? Challenge yourself!")
        elif test_result.difficulty.lower() == "medium":
            if test_result.accuracy > 90 and test_result.wpm > 50:
                feedback.append("You're doing great with medium difficulty! Consider trying a hard test next.")
        else:  # hard
            if test_result.accuracy < 80:
                feedback.append("Hard difficulty is challenging! You might want to practice more on medium difficulty.")
        
        # Random tip
        tips = [
            "Try to maintain a consistent rhythm while typing.",
            "Take breaks to prevent fatigue and maintain accuracy.",
            "Focus on accuracy first, speed will naturally improve with practice.",
            "Use all your fingers for more efficient typing.",
            "Keep your wrists straight and fingers slightly curved for better typing posture."
        ]
        feedback.append(f"💡 Tip: {random.choice(tips)}")
        
        return " ".join(feedback)
