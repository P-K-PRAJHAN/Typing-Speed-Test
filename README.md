# AI-Enhanced Typing Speed Analyzer with Data Science Insights

A modern, full-stack web application that helps users improve their typing speed and accuracy through AI-powered analytics and personalized feedback. Built with Flask, React, Firebase, and data science libraries.

## 🚀 Features

- **User Authentication**: Secure login/signup with Firebase Authentication
- **AI-Powered Text Generation**: Dynamic text generation using Markov chains for varied practice
- **Real-time Typing Analysis**: Live WPM, accuracy, and error tracking during tests
- **Multi-level Difficulty**: Easy, medium, and hard difficulty settings
- **Comprehensive Analytics**: Data science-powered insights with interactive charts
- **Personalized Feedback**: AI-generated performance feedback and improvement recommendations
- **Progress Tracking**: Historical data storage and trend analysis
- **Responsive Design**: Mobile-friendly interface built with Tailwind CSS

## 🛠️ Tech Stack

### Frontend
- **React.js** with Vite
- **Tailwind CSS** for styling
- **Firebase SDK** for authentication
- **Axios** for API requests
- **Plotly.js** for interactive charts

### Backend
- **Flask** REST API
- **Firebase Admin SDK** for backend authentication
- **Firestore** for data storage
- **Pandas** for data analysis
- **Matplotlib** for chart generation
- **TextBlob** for NLP analysis
- **Scikit-learn** for difficulty prediction
- **Markovify** for AI text generation

## 📁 Project Structure

```
typing-speed-analyzer/
│
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── firebase_config.json   # Firebase service account key
│   ├── core/
│   │   ├── ai_text_generator.py  # AI text generation
│   │   ├── scoring.py           # Typing metrics calculation
│   │   ├── analytics.py         # Data analysis and charting
│   │   └── feedback_engine.py   # AI feedback generation
│   └── charts/                  # Generated chart images
│
├── frontend/
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── index.html             # HTML entry point
│   ├── src/
│   │   ├── main.jsx           # React entry point
│   │   ├── App.jsx            # Main React component
│   │   ├── components/        # Reusable components
│   │   ├── pages/             # Page components
│   │   └── services/          # API and Firebase services
│   ├── src/index.css          # Tailwind CSS imports
│   ├── tailwind.config.js     # Tailwind configuration
│   └── postcss.config.js      # PostCSS configuration
│
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- Firebase account with Authentication and Firestore enabled

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up Firebase:
   - Create a Firebase project at https://console.firebase.google.com/
   - Enable Authentication (Email/Password)
   - Enable Firestore Database
   - Generate a service account key and download the JSON file
   - Rename the file to `firebase_config.json` and place it in the backend directory
   - Update the file with your Firebase project credentials

5. Start the Flask server:
   ```bash
   python app.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Configure Firebase:
   - Go to your Firebase project settings in the Firebase Console
   - Under the "General" tab, find your Firebase SDK configuration
   - Click on the "</>" icon to create a new web app if you haven't already
   - Copy the firebaseConfig object values
   - Update `src/services/firebase.js` with your actual Firebase config values

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open your browser to `http://localhost:3000`

## 🔐 Firebase Configuration

To configure Firebase for this project:

### Frontend Configuration:
1. Create a Firebase project at https://console.firebase.google.com/
2. Enable Authentication and select "Email/Password" sign-in method
3. Enable Firestore Database
4. In Project Settings, click on the "</>" icon to create a new web app
5. Give your app a name (e.g., "typing-test-app") and click "Register"
6. Copy the firebaseConfig object values and update `frontend/src/services/firebase.js`

### Backend Configuration:
1. In the same Firebase Console, go to Project Settings
2. Click on the "Service Accounts" tab
3. Click "Generate new private key"
4. This will download a JSON file with your service account credentials
5. Rename this file to `firebase_config.json` and place it in the `backend/` directory

## 🧪 Usage

1. Register a new account or log in with existing credentials
2. Navigate to the Typing Test page
3. Select a difficulty level (Easy, Medium, Hard)
4. Click "Start Test" and begin typing the displayed text
5. View real-time statistics (WPM, accuracy, errors)
6. See detailed results and AI-generated feedback after completing the test
7. Check the Analytics dashboard for performance trends and insights
8. Review your test history in the History section

## 📊 Analytics Features

The application provides comprehensive analytics including:

- **WPM Trends**: Track your typing speed over time
- **Accuracy Progress**: Monitor improvements in typing accuracy
- **Difficulty Performance**: Compare performance across difficulty levels
- **Error Distribution**: Analyze common mistake patterns
- **WPM vs Accuracy**: Correlation analysis between speed and accuracy
- **Personalized Recommendations**: AI-generated tips for improvement
- **Weakness Analysis**: Identification of specific areas needing attention

## 🤖 AI/NLP Features

- **Markov Chain Text Generation**: AI-generated practice texts for varied challenges
- **Readability Analysis**: Text complexity scoring using NLP techniques
- **Difficulty Matching**: Predictive algorithms to suggest optimal difficulty levels
- **Performance Feedback**: Rule-based AI feedback generation
- **Pattern Recognition**: Identification of common typing mistakes

## 📈 Data Science Implementation

The application leverages several data science techniques:

- **TF-IDF Vectorization**: For text similarity analysis
- **Cosine Similarity**: To match user skill level with appropriate texts
- **Statistical Analysis**: Using Pandas for performance metrics
- **Data Visualization**: Matplotlib-generated charts with statistical insights
- **Machine Learning**: Scikit-learn for predictive modeling

## 🛡️ Security

- Firebase Authentication for secure user management
- Token-based API authentication
- Protected API routes with middleware verification
- Secure storage of sensitive credentials

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all the open-source libraries and tools that made this project possible
- Inspired by the need for better typing practice tools with data-driven insights