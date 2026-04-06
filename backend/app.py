import os
import json
import firebase_admin
from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_admin import credentials, auth, firestore
from core.ai_text_generator import AITextGenerator
from core.scoring import TypingScorer
from core.analytics import AnalyticsEngine
from core.feedback_engine import FeedbackEngine
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    firebase_initialized = True
except Exception as e:
    print(f"Firebase initialization failed: {e}")
    firebase_initialized = False
    # Create a mock database for development
    mock_db = {}

# Initialize components
text_generator = AITextGenerator()
scorer = TypingScorer()
analytics_engine = AnalyticsEngine()
feedback_engine = FeedbackEngine()

def verify_firebase_token(token):
    """
    Verify Firebase ID token
    
    Args:
        token (str): Firebase ID token
        
    Returns:
        dict: Decoded token or None if invalid
    """
    if not firebase_initialized:
        # Mock verification for development
        return {"uid": "mock_user_id", "email": "mock@example.com"}
    
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None

def require_auth(f):
    """
    Decorator to require Firebase authentication
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization header missing"}), 401
        
        try:
            # Extract token from "Bearer <token>" format
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({"error": "Invalid authorization header format"}), 401
        
        decoded_token = verify_firebase_token(token)
        if not decoded_token:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Add user info to request context
        request.user = decoded_token
        return f(*args, **kwargs)
    
    return decorated_function

@app.route('/api/generate-text', methods=['POST'])
def generate_text():
    """
    Generate typing text based on difficulty level
    """
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 'easy')
        sentences = data.get('sentences', 3)
        
        # Generate text using AI
        generated_text = text_generator.generate_text(difficulty, sentences)
        
        return jsonify({
            "success": True,
            "text": generated_text,
            "difficulty": difficulty
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/submit-test', methods=['POST'])
@require_auth
def submit_test():
    """
    Submit typing test results
    """
    try:
        data = request.get_json()
        user_id = request.user['uid']
        
        # Extract test data
        original_text = data.get('originalText', '')
        typed_text = data.get('typedText', '')
        time_taken = data.get('timeTaken', 0)
        difficulty = data.get('difficulty', 'easy')
        
        # Calculate scores
        wpm = scorer.calculate_wpm(typed_text, time_taken)
        accuracy = scorer.calculate_accuracy(original_text, typed_text)
        total_errors = scorer.count_mistakes(original_text, typed_text)
        readability = scorer.analyze_readability(original_text)
        
        # Prepare document for Firestore
        test_result = {
            'user_id': user_id,
            'difficulty': difficulty,
            'wpm': wpm,
            'accuracy': accuracy,
            'total_errors': total_errors,
            'time_taken': time_taken,
            'text_length': len(original_text),
            'timestamp': firestore.SERVER_TIMESTAMP,
            'original_text': original_text,
            'typed_text': typed_text,
            'readability_score': readability.get('readability_score', 0)
        }
        
        # Save to Firestore
        if firebase_initialized:
            doc_ref = db.collection('typing_tests').document()
            doc_ref.set(test_result)
        else:
            # Mock storage for development
            if 'typing_tests' not in mock_db:
                mock_db['typing_tests'] = []
            mock_db['typing_tests'].append(test_result)
        
        # Generate feedback
        feedback = feedback_engine.generate_performance_feedback(
            wpm, accuracy, difficulty, total_errors
        )
        
        return jsonify({
            "success": True,
            "result": {
                "wpm": wpm,
                "accuracy": accuracy,
                "total_errors": total_errors,
                "time_taken": time_taken,
                "feedback": feedback
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/user-history', methods=['GET'])
@require_auth
def get_user_history():
    """
    Get user's typing test history
    """
    try:
        user_id = request.user['uid']
        
        # Fetch from Firestore
        if firebase_initialized:
            docs = db.collection('typing_tests') \
                     .where('user_id', '==', user_id) \
                     .limit(50) \
                     .stream()
            
            history = []
            for doc in docs:
                test_data = doc.to_dict()
                test_data['id'] = doc.id
                # Convert timestamp to string for JSON serialization
                if 'timestamp' in test_data and hasattr(test_data['timestamp'], '_seconds'):
                    test_data['timestamp'] = test_data['timestamp'].isoformat()
                history.append(test_data)
            
            # Sort by timestamp descending (newest first)
            history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        else:
            # Mock data for development
            history = mock_db.get('typing_tests', [])[:50]
            # Sort by timestamp descending (newest first)
            history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return jsonify({
            "success": True,
            "history": history
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
@require_auth
def get_analytics():
    """
    Generate analytics charts and insights
    """
    try:
        user_id = request.user['uid']
        
        # Fetch user history
        if firebase_initialized:
            docs = db.collection('typing_tests') \
                     .where('user_id', '==', user_id) \
                     .limit(100) \
                     .stream()
            
            history = []
            for doc in docs:
                test_data = doc.to_dict()
                test_data['id'] = doc.id
                # Convert timestamp to string for JSON serialization
                if 'timestamp' in test_data and hasattr(test_data['timestamp'], '_seconds'):
                    test_data['timestamp'] = test_data['timestamp'].isoformat()
                history.append(test_data)
            
            # Sort by timestamp descending (newest first)
            history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        else:
            # Mock data for development
            history = mock_db.get('typing_tests', [])[:100]
            # Sort by timestamp descending (newest first)
            history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        # Generate charts with error handling
        # Always try to generate charts even with minimal data
        wpm_chart = None
        accuracy_chart = None
        difficulty_chart = None
        error_chart = None
        scatter_chart = None
        
        try:
            wpm_chart = analytics_engine.generate_wpm_trend_chart(history, user_id)
        except Exception as e:
            print(f"Error generating WPM chart: {e}")
            
        try:
            accuracy_chart = analytics_engine.generate_accuracy_chart(history, user_id)
        except Exception as e:
            print(f"Error generating accuracy chart: {e}")
            
        try:
            difficulty_chart = analytics_engine.generate_difficulty_comparison_chart(history, user_id)
        except Exception as e:
            print(f"Error generating difficulty chart: {e}")
            
        try:
            error_chart = analytics_engine.generate_error_distribution_chart(history, user_id)
        except Exception as e:
            print(f"Error generating error chart: {e}")
            
        try:
            scatter_chart = analytics_engine.generate_wpm_vs_accuracy_scatter(history, user_id)
        except Exception as e:
            print(f"Error generating scatter chart: {e}")
        
        # Generate insights with error handling
        try:
            patterns = analytics_engine.analyze_mistake_patterns(history)
        except Exception as e:
            print(f"Error analyzing patterns: {e}")
            patterns = {}
            
        try:
            recommendations = feedback_engine.generate_improvement_recommendations(history)
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            recommendations = []
            
        try:
            weaknesses = feedback_engine.analyze_weaknesses(history)
        except Exception as e:
            print(f"Error analyzing weaknesses: {e}")
            weaknesses = {}
        
        # Convert chart paths to URLs
        base_url = request.url_root.rstrip('/')
        chart_urls = {
            "wpm_trend": f"{base_url}/charts/{os.path.basename(wpm_chart)}" if wpm_chart else None,
            "accuracy_trend": f"{base_url}/charts/{os.path.basename(accuracy_chart)}" if accuracy_chart else None,
            "difficulty_comparison": f"{base_url}/charts/{os.path.basename(difficulty_chart)}" if difficulty_chart else None,
            "error_distribution": f"{base_url}/charts/{os.path.basename(error_chart)}" if error_chart else None,
            "wpm_vs_accuracy": f"{base_url}/charts/{os.path.basename(scatter_chart)}" if scatter_chart else None
        }
        
        return jsonify({
            "success": True,
            "charts": chart_urls,
            "patterns": patterns,
            "recommendations": recommendations,
            "weaknesses": weaknesses
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/predict-difficulty', methods=['POST'])
@require_auth
def predict_difficulty():
    """
    Predict optimal difficulty level for user
    """
    try:
        user_id = request.user['uid']
        data = request.get_json()
        text = data.get('text', '')
        
        # Fetch user history
        if firebase_initialized:
            docs = db.collection('typing_tests') \
                     .where('user_id', '==', user_id) \
                     .limit(20) \
                     .stream()
            
            history = [doc.to_dict() for doc in docs]
            # Sort by timestamp descending (newest first)
            history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        else:
            # Mock data for development
            history = mock_db.get('typing_tests', [])[:20]
            # Sort by timestamp descending (newest first)
            history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        # Predict difficulty match
        prediction = analytics_engine.predict_difficulty_match(text, history)
        
        return jsonify({
            "success": True,
            "prediction": prediction
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/user-profile', methods=['GET'])
@require_auth
def get_user_profile():
    """
    Get user profile information
    """
    try:
        user_id = request.user['uid']
        email = request.user.get('email', 'Unknown')
        
        # Fetch user stats
        if firebase_initialized:
            docs = db.collection('typing_tests') \
                     .where('user_id', '==', user_id) \
                     .stream()
            
            history = [doc.to_dict() for doc in docs]
        else:
            # Mock data for development
            history = mock_db.get('typing_tests', [])
        
        # Calculate stats
        total_tests = len(history)
        if total_tests > 0:
            avg_wpm = sum(test['wpm'] for test in history) / total_tests
            avg_accuracy = sum(test['accuracy'] for test in history) / total_tests
            best_wpm = max(test['wpm'] for test in history)
            best_accuracy = max(test['accuracy'] for test in history)
        else:
            avg_wpm = 0
            avg_accuracy = 0
            best_wpm = 0
            best_accuracy = 0
        
        return jsonify({
            "success": True,
            "profile": {
                "user_id": user_id,
                "email": email,
                "stats": {
                    "total_tests": total_tests,
                    "average_wpm": round(avg_wpm, 2),
                    "average_accuracy": round(avg_accuracy, 2),
                    "best_wpm": best_wpm,
                    "best_accuracy": best_accuracy
                }
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        "status": "healthy",
        "service": "AI-Enhanced Typing Speed Analyzer API"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)