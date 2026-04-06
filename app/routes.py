from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from app.models import User, TestResult
from app.core.ai_text_generator import AITextGenerator
from app.core.scoring import ScoringEngine
from app.core.feedback_engine import FeedbackEngine
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from sqlalchemy import func

# Create blueprint
main = Blueprint('main', __name__)

# Home route
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

# Authentication routes
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('main.register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('main.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('main.register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Dashboard
@main.route('/dashboard')
@login_required
def dashboard():
    # Get recent test results
    recent_tests = TestResult.query.filter_by(user_id=current_user.id)\
        .order_by(TestResult.created_at.desc()).limit(5).all()
    
    # Get best WPM
    best_wpm = db.session.query(func.max(TestResult.wpm))\
        .filter_by(user_id=current_user.id).scalar() or 0
    
    # Get total tests taken
    total_tests = TestResult.query.filter_by(user_id=current_user.id).count()
    
    # Get average accuracy
    avg_accuracy = db.session.query(func.avg(TestResult.accuracy))\
        .filter_by(user_id=current_user.id).scalar() or 0
    
    return render_template('dashboard.html',
                         recent_tests=recent_tests,
                         best_wpm=round(best_wpm, 1),
                         total_tests=total_tests,
                         avg_accuracy=round(avg_accuracy, 1))

# Typing test
@main.route('/test/<difficulty>')
@login_required
def typing_test(difficulty):
    if difficulty not in ['easy', 'medium', 'hard']:
        flash('Invalid difficulty level', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Generate text based on difficulty and sanitize whitespace characters
    raw_text = AITextGenerator.generate_text(difficulty)
    # Replace tabs with four spaces and normalize CRLF to LF
    text = raw_text.replace('\t', '    ').replace('\r\n', '\n').replace('\r', '\n')
    session['test_text'] = text  # Store in session for validation
    session['test_difficulty'] = difficulty
    session['test_start_time'] = datetime.utcnow().timestamp()
    
    return render_template('test.html', text=text, difficulty=difficulty.capitalize())

@main.route('/submit_test', methods=['POST'])
@login_required
def submit_test():
    if 'test_text' not in session:
        flash('No active test found', 'danger')
        return redirect(url_for('main.dashboard'))
    
    typed_text = request.form.get('typed_text', '')
    original_text = session.pop('test_text', '')
    difficulty = session.pop('test_difficulty', 'medium')
    start_time = session.pop('test_start_time', 0)
    
    # Calculate time taken
    time_taken = max(1, int(datetime.utcnow().timestamp() - start_time))
    
    # Calculate scores
    scores = ScoringEngine.calculate_score(original_text, typed_text, time_taken)
    
    # Save test result
    test_result = TestResult(
        user_id=current_user.id,
        difficulty=difficulty,
        wpm=scores['wpm'],
        accuracy=scores['accuracy'],
        errors=scores['errors'],
        time_taken=time_taken,
        text_length=scores['text_length']
    )
    db.session.add(test_result)
    db.session.commit()
    
    # Get previous results for feedback
    previous_results = TestResult.query\
        .filter_by(user_id=current_user.id)\
        .order_by(TestResult.created_at.desc())\
        .limit(5)\
        .all()
    
    # Generate feedback
    feedback = FeedbackEngine.generate_feedback(test_result, previous_results)
    
    return jsonify({
        'success': True,
        'wpm': scores['wpm'],
        'accuracy': scores['accuracy'],
        'errors': scores['errors'],
        'time_taken': time_taken,
        'feedback': feedback
    })

# Analytics
@main.route('/analytics')
@login_required
def analytics():
    # Get all test results for the user
    test_results = TestResult.query\
        .filter_by(user_id=current_user.id)\
        .order_by(TestResult.created_at)\
        .all()
    
    if not test_results:
        return render_template('analytics.html', 
                             wpm_chart=None, 
                             accuracy_chart=None,
                             difficulty_chart=None,
                             wpm_vs_accuracy_chart=None)
    
    # Prepare data for charts
    dates = [result.created_at.strftime('%Y-%m-%d') for result in test_results]
    wpm_values = [result.wpm for result in test_results]
    accuracy_values = [result.accuracy for result in test_results]
    difficulties = [result.difficulty for result in test_results]
    
    # Create WPM trend chart
    plt.figure(figsize=(10, 5))
    plt.plot(dates, wpm_values, 'b-o')
    plt.title('WPM Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('WPM')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save WPM chart to base64
    wpm_chart = save_plot_to_base64(plt)
    plt.close()
    
    # Create Accuracy trend chart
    plt.figure(figsize=(10, 5))
    plt.plot(dates, accuracy_values, 'g-o')
    plt.title('Accuracy Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Accuracy (%)')
    plt.ylim(0, 105)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    accuracy_chart = save_plot_to_base64(plt)
    plt.close()
    
    # Create difficulty distribution chart
    difficulty_counts = {
        'Easy': len([d for d in difficulties if d.lower() == 'easy']),
        'Medium': len([d for d in difficulties if d.lower() == 'medium']),
        'Hard': len([d for d in difficulties if d.lower() == 'hard'])
    }
    
    plt.figure(figsize=(8, 6))
    plt.pie(difficulty_counts.values(), 
            labels=difficulty_counts.keys(), 
            autopct='%1.1f%%',
            colors=['#66b3ff', '#99ff99', '#ff9999'])
    plt.title('Test Difficulty Distribution')
    
    difficulty_chart = save_plot_to_base64(plt)
    plt.close()
    
    # Create WPM vs Accuracy scatter plot
    plt.figure(figsize=(8, 6))
    colors = {'easy': 'green', 'medium': 'orange', 'hard': 'red'}
    for result in test_results:
        plt.scatter(result.wpm, result.accuracy, 
                   color=colors.get(result.difficulty.lower(), 'blue'),
                   alpha=0.6)
    
    plt.title('WPM vs Accuracy')
    plt.xlabel('WPM')
    plt.ylabel('Accuracy (%)')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Easy',
               markerfacecolor='green', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Medium',
               markerfacecolor='orange', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Hard',
               markerfacecolor='red', markersize=10)
    ]
    plt.legend(handles=legend_elements, title='Difficulty')
    
    wpm_vs_accuracy_chart = save_plot_to_base64(plt)
    plt.close()
    
    return render_template('analytics.html',
                         wpm_chart=wpm_chart,
                         accuracy_chart=accuracy_chart,
                         difficulty_chart=difficulty_chart,
                         wpm_vs_accuracy_chart=wpm_vs_accuracy_chart)

def save_plot_to_base64(plt):
    """Save matplotlib plot to base64 encoded string"""
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')
