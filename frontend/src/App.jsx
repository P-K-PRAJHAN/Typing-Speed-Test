import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import TypingTest from './pages/TypingTest';
import Analytics from './pages/Analytics';
import History from './pages/History';
import Navbar from './components/Navbar';
import { auth } from './services/firebase';

function App() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const unsubscribe = auth.onAuthStateChanged((user) => {
            setUser(user);
            setLoading(false);
        });

        return unsubscribe;
    }, []);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-screen">
                <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    return (
        <Router>
            <div className="min-h-screen bg-gray-50">
                {user && <Navbar />}
                <Routes>
                    <Route
                        path="/"
                        element={user ? <Dashboard /> : <Navigate to="/login" />}
                    />
                    <Route
                        path="/test"
                        element={user ? <TypingTest /> : <Navigate to="/login" />}
                    />
                    <Route
                        path="/analytics"
                        element={user ? <Analytics /> : <Navigate to="/login" />}
                    />
                    <Route
                        path="/history"
                        element={user ? <History /> : <Navigate to="/login" />}
                    />
                    <Route
                        path="/login"
                        element={user ? <Navigate to="/" /> : <LoginPage />}
                    />
                </Routes>
            </div>
        </Router>
    );
}

export default App;