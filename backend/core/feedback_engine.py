class FeedbackEngine:
    def __init__(self):
        pass
    
    def generate_performance_feedback(self, wpm, accuracy, difficulty, mistakes):
        """
        Generate AI-powered feedback based on performance metrics
        
        Args:
            wpm (float): Words per minute
            accuracy (float): Accuracy percentage
            difficulty (str): Difficulty level
            mistakes (int): Number of mistakes
            
        Returns:
            dict: Feedback message and suggestions
        """
        feedback = {
            "message": "",
            "suggestions": [],
            "encouragement": ""
        }
        
        # Generate feedback message based on performance
        if wpm >= 60 and accuracy >= 95:
            feedback["message"] = "Excellent performance! You're a typing master."
            feedback["encouragement"] = "Keep up the great work!"
        elif wpm >= 40 and accuracy >= 90:
            feedback["message"] = "Great job! Your typing skills are above average."
            feedback["encouragement"] = "Continue practicing to reach even higher speeds."
        elif wpm >= 30 and accuracy >= 85:
            feedback["message"] = "Good effort! You're making steady progress."
            feedback["encouragement"] = "With more practice, you'll see significant improvement."
        elif wpm >= 20 and accuracy >= 80:
            feedback["message"] = "Decent start! Focus on accuracy to build a strong foundation."
            feedback["encouragement"] = "Regular practice will help you improve steadily."
        else:
            feedback["message"] = "Keep practicing! Everyone starts somewhere."
            feedback["encouragement"] = "Focus on accuracy first, then gradually increase your speed."
        
        # Generate suggestions based on performance
        if accuracy < 85:
            feedback["suggestions"].append("Focus on accuracy before speed. Correct finger placement is crucial.")
        
        if mistakes > 10:
            feedback["suggestions"].append("Practice typing difficult character combinations slowly and accurately.")
        
        if wpm < 30:
            feedback["suggestions"].append("Try typing exercises for 15-20 minutes daily to build muscle memory.")
        
        if difficulty == "easy" and wpm > 50:
            feedback["suggestions"].append("Consider moving to a higher difficulty level to continue challenging yourself.")
        
        if difficulty == "hard" and wpm < 20:
            feedback["suggestions"].append("You might benefit from practicing at a slightly easier level to build confidence.")
        
        # Add general suggestions if none were added
        if not feedback["suggestions"]:
            feedback["suggestions"].append("Maintain proper posture and hand position while typing.")
            feedback["suggestions"].append("Take regular breaks to avoid fatigue and maintain focus.")
            feedback["suggestions"].append("Try to type evenly with all fingers for balanced development.")
        
        return feedback
    
    def generate_improvement_recommendations(self, user_history):
        """
        Generate personalized improvement recommendations based on user history
        
        Args:
            user_history (list): List of user's past test results
            
        Returns:
            list: Personalized recommendations
        """
        if not user_history:
            return ["Start with easy texts to build foundational skills."]
        
        recommendations = []
        
        # Convert to a more manageable format
        recent_tests = user_history[-10:]  # Last 10 tests
        
        # Analyze trends
        avg_wpm = sum(test['wpm'] for test in recent_tests) / len(recent_tests)
        avg_accuracy = sum(test['accuracy'] for test in recent_tests) / len(recent_tests)
        
        # WPM-based recommendations
        if avg_wpm < 30:
            recommendations.append("Focus on building typing speed with dedicated speed drills.")
        elif avg_wpm > 60:
            recommendations.append("Maintain your high speed while continuing to challenge yourself with complex texts.")
        
        # Accuracy-based recommendations
        if avg_accuracy < 85:
            recommendations.append("Prioritize accuracy over speed. Slow, correct typing builds better habits.")
        elif avg_accuracy > 95:
            recommendations.append("Your accuracy is excellent. Consider focusing on increasing speed while maintaining precision.")
        
        # Difficulty progression
        difficulties = [test['difficulty'] for test in recent_tests]
        easy_count = difficulties.count('easy')
        medium_count = difficulties.count('medium')
        hard_count = difficulties.count('hard')
        
        if easy_count > medium_count + hard_count:
            recommendations.append("Try more medium and hard texts to continue progressing.")
        elif hard_count == 0 and medium_count > 3:
            recommendations.append("Challenge yourself with hard texts to push your limits.")
        
        # Consistency
        if len(recent_tests) >= 5:
            recommendations.append("Maintain consistent practice for continuous improvement.")
        else:
            recommendations.append("Try to practice regularly, even if just for a few minutes each day.")
        
        # Add general recommendations if list is short
        if len(recommendations) < 3:
            recommendations.extend([
                "Warm up with simple exercises before attempting complex texts.",
                "Focus on proper finger placement and touch typing techniques.",
                "Track your progress over time to stay motivated."
            ])
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def analyze_weaknesses(self, user_history):
        """
        Analyze user's weaknesses based on test history
        
        Args:
            user_history (list): List of user's past test results
            
        Returns:
            dict: Analysis of weaknesses
        """
        if not user_history:
            return {
                "needs_more_data": True,
                "message": "Complete more tests to get personalized weakness analysis."
            }
        
        analysis = {
            "needs_more_data": False,
            "common_issues": [],
            "strengths": [],
            "areas_for_improvement": []
        }
        
        # Look at recent tests for trends
        recent_tests = user_history[-10:]
        
        # Calculate averages
        avg_wpm = sum(test['wpm'] for test in recent_tests) / len(recent_tests)
        avg_accuracy = sum(test['accuracy'] for test in recent_tests) / len(recent_tests)
        avg_errors = sum(test['total_errors'] for test in recent_tests) / len(recent_tests)
        
        # Identify common issues
        if avg_accuracy < 85:
            analysis["common_issues"].append("Accuracy needs improvement")
        
        if avg_wpm < 30:
            analysis["common_issues"].append("Typing speed is below average")
        
        if avg_errors > 8:
            analysis["common_issues"].append("High error rate suggests technique issues")
        
        # Identify strengths
        if avg_accuracy > 95:
            analysis["strengths"].append("Excellent accuracy")
        
        if avg_wpm > 50:
            analysis["strengths"].append("Above-average typing speed")
        
        # Areas for improvement by difficulty
        difficulty_performance = {}
        for test in recent_tests:
            diff = test['difficulty']
            if diff not in difficulty_performance:
                difficulty_performance[diff] = {'wpm': [], 'accuracy': [], 'errors': []}
            difficulty_performance[diff]['wpm'].append(test['wpm'])
            difficulty_performance[diff]['accuracy'].append(test['accuracy'])
            difficulty_performance[diff]['errors'].append(test['total_errors'])
        
        for difficulty, perf in difficulty_performance.items():
            avg_diff_wpm = sum(perf['wpm']) / len(perf['wpm'])
            avg_diff_accuracy = sum(perf['accuracy']) / len(perf['accuracy'])
            avg_diff_errors = sum(perf['errors']) / len(perf['errors'])
            
            if avg_diff_accuracy < 85:
                analysis["areas_for_improvement"].append(f"Work on accuracy for {difficulty} texts")
            
            if avg_diff_errors > 8:
                analysis["areas_for_improvement"].append(f"Reduce errors when typing {difficulty} texts")
        
        # If no specific issues identified, provide general advice
        if not analysis["common_issues"] and not analysis["areas_for_improvement"]:
            analysis["common_issues"].append("No major issues detected, but continued practice is always beneficial")
        
        return analysis

# Example usage
if __name__ == "__main__":
    engine = FeedbackEngine()
    
    # Generate feedback
    feedback = engine.generate_performance_feedback(45, 92.5, "medium", 3)
    print("Feedback:", feedback)
    
    # Generate recommendations
    sample_history = [
        {"wpm": 35, "accuracy": 88, "difficulty": "easy"},
        {"wpm": 42, "accuracy": 91, "difficulty": "medium"},
        {"wpm": 38, "accuracy": 89, "difficulty": "medium"},
    ]
    recommendations = engine.generate_improvement_recommendations(sample_history)
    print("Recommendations:", recommendations)
    
    # Analyze weaknesses
    weaknesses = engine.analyze_weaknesses(sample_history)
    print("Weaknesses:", weaknesses)