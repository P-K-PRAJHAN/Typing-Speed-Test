# AI-Enhanced Typing Speed Analyzer

![Typing Speed Analyzer](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-blue)

A web-based typing speed analyzer that helps users improve their typing skills through AI-generated tests, real-time feedback, and performance analytics.

## 🚀 Features

- User authentication (register, login, logout)
- Customizable typing tests with three difficulty levels
- Real-time typing speed and accuracy tracking
- Detailed performance analytics and progress tracking
- AI-generated text for typing practice
- Responsive design for all devices
- Performance visualization with charts
- Personalized feedback and improvement tips

## 🛠 Tech Stack

### Backend
- **Framework**: Flask 2.0+
- **Database**: SQLite (with SQLAlchemy ORM)
- **Authentication**: Flask-Login
- **Templates**: Jinja2
- **Data Visualization**: Matplotlib

### Frontend
- **CSS Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **Charts**: Chart.js
- **JavaScript**: Vanilla JS for interactive features

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/typing-speed-analyzer.git
   cd typing-speed-analyzer
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   ```

## 🏃‍♂️ Running the Application

1. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

2. **Run the development server**
   ```bash
   flask run
   ```

3. **Access the application**
   Open your browser and navigate to: `http://127.0.0.1:5000/`

## 📊 Default Admin Account

- **Username**: admin
- **Password**: admin123

## 🧪 Running Tests

```bash
pytest tests/
```

## 📂 Project Structure

```
typing_speed_ai/
├── app/
│   ├── __init__.py         # Application factory
│   ├── models.py          # Database models
│   ├── routes.py          # Application routes
│   ├── core/              # Core functionality
│   │   ├── __init__.py
│   │   ├── ai_text_generator.py
│   │   ├── feedback_engine.py
│   │   └── scoring.py
│   ├── static/            # Static files
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── timer.js
│   └── templates/         # HTML templates
│       ├── base.html
│       ├── dashboard.html
│       ├── login.html
│       ├── register.html
│       ├── test.html
│       └── results.html
├── instance/              # Database and instance files
├── tests/                 # Test files
├── .env                  # Environment variables
├── .gitignore
├── config.py             # Configuration
├── requirements.txt      # Project dependencies
└── run.py               # Application entry point
```

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [Chart.js](https://www.chartjs.org/)

---

<div align="center">
  Made with ❤️ by Your Name
</div>
