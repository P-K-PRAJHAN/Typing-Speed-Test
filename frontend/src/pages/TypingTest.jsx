import React, { useState, useEffect, useRef } from 'react';
import { generateText, submitTest } from '../services/api';

const TypingTest = () => {
    const [difficulty, setDifficulty] = useState('easy');
    const [text, setText] = useState('');
    const [userInput, setUserInput] = useState('');
    const [timeLeft, setTimeLeft] = useState(60);
    const [isTestActive, setIsTestActive] = useState(false);
    const [startTime, setStartTime] = useState(null);
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const textareaRef = useRef(null);

    // Generate text when difficulty changes
    useEffect(() => {
        const fetchText = async () => {
            try {
                setLoading(true);
                const response = await generateText(difficulty);
                if (response.success) {
                    setText(response.text);
                } else {
                    setError(response.error || 'Failed to generate text');
                }
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchText();
    }, [difficulty]);

    // Timer effect
    useEffect(() => {
        let timer;
        if (isTestActive && timeLeft > 0) {
            timer = setInterval(() => {
                setTimeLeft(prev => prev - 1);
            }, 1000);
        } else if (timeLeft === 0 && isTestActive) {
            finishTest();
        }
        return () => clearInterval(timer);
    }, [isTestActive, timeLeft]);

    // Focus textarea when test starts
    useEffect(() => {
        if (isTestActive && textareaRef.current) {
            textareaRef.current.focus();
        }
    }, [isTestActive]);

    const startTest = () => {
        setIsTestActive(true);
        setStartTime(Date.now());
        setTimeLeft(60);
        setUserInput('');
        setResults(null);
        setError('');
    };

    const resetTest = () => {
        setIsTestActive(false);
        setTimeLeft(60);
        setUserInput('');
        setResults(null);
        setError('');
    };

    const finishTest = async () => {
        if (!isTestActive) return;

        setIsTestActive(false);
        const endTime = Date.now();
        const timeTaken = (endTime - startTime) / 1000; // in seconds

        try {
            const response = await submitTest({
                originalText: text,
                typedText: userInput,
                timeTaken: timeTaken,
                difficulty: difficulty
            });

            if (response.success) {
                setResults(response.result);
            } else {
                setError(response.error || 'Failed to submit test');
            }
        } catch (err) {
            setError(err.message);
        }
    };

    const handleInputChange = (e) => {
        const value = e.target.value;
        setUserInput(value);

        // Auto-finish when user completes the text
        if (value.length >= text.length && isTestActive) {
            finishTest();
        }
    };

    const handleKeyDown = (e) => {
        if (!isTestActive && e.key !== 'Tab') {
            startTest();
        }

        // Finish test when user presses Enter and test is active
        if (isTestActive && e.key === 'Enter') {
            e.preventDefault();
            finishTest();
        }
    };

    // Calculate live stats
    const calculateStats = () => {
        if (!userInput || !isTestActive) return { wpm: 0, accuracy: 0, errors: 0 };

        const timeElapsed = (Date.now() - startTime) / 1000 / 60; // in minutes
        const wordsTyped = userInput.length / 5;
        const wpm = timeElapsed > 0 ? Math.round(wordsTyped / timeElapsed) : 0;

        let correctChars = 0;
        let errors = 0;
        for (let i = 0; i < userInput.length; i++) {
            if (i < text.length && userInput[i] === text[i]) {
                correctChars++;
            } else {
                errors++;
            }
        }

        const accuracy = userInput.length > 0 ? Math.round((correctChars / userInput.length) * 100) : 0;

        return { wpm, accuracy, errors };
    };

    const { wpm, accuracy, errors } = calculateStats();

    // Highlight text based on user input
    const renderHighlightedText = () => {
        return text.split('').map((char, index) => {
            let className = 'text-gray-700';

            if (index < userInput.length) {
                if (userInput[index] === char) {
                    className = 'text-green-600 bg-green-100';
                } else {
                    className = 'text-red-600 bg-red-100';
                }
            }

            return (
                <span key={index} className={className}>
                    {char}
                </span>
            );
        });
    };

    return (
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-6">Typing Test</h1>

            <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
                <div className="px-4 py-5 sm:px-6">
                    <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                        <h2 className="text-lg leading-6 font-medium text-gray-900">Test Your Typing Skills</h2>
                        <div className="mt-4 flex space-x-4 md:mt-0">
                            <select
                                value={difficulty}
                                onChange={(e) => setDifficulty(e.target.value)}
                                disabled={isTestActive}
                                className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                            >
                                <option value="easy">Easy</option>
                                <option value="medium">Medium</option>
                                <option value="hard">Hard</option>
                            </select>

                            {!isTestActive ? (
                                <button
                                    onClick={startTest}
                                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                >
                                    Start Test
                                </button>
                            ) : (
                                <button
                                    onClick={resetTest}
                                    className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                >
                                    Reset
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-6" role="alert">
                    <strong className="font-bold">Error! </strong>
                    <span className="block sm:inline">{error}</span>
                </div>
            )}

            {loading ? (
                <div className="flex justify-center items-center h-64">
                    <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
                </div>
            ) : (
                <>
                    {/* Stats Bar */}
                    <div className="grid grid-cols-1 gap-6 sm:grid-cols-4 mb-6">
                        <div className="bg-white overflow-hidden shadow rounded-lg">
                            <div className="px-4 py-5 sm:p-6">
                                <div className="text-sm font-medium text-gray-500">Time Left</div>
                                <div className="mt-1 text-3xl font-semibold text-gray-900">{timeLeft}s</div>
                            </div>
                        </div>

                        <div className="bg-white overflow-hidden shadow rounded-lg">
                            <div className="px-4 py-5 sm:p-6">
                                <div className="text-sm font-medium text-gray-500">WPM</div>
                                <div className="mt-1 text-3xl font-semibold text-gray-900">{wpm}</div>
                            </div>
                        </div>

                        <div className="bg-white overflow-hidden shadow rounded-lg">
                            <div className="px-4 py-5 sm:p-6">
                                <div className="text-sm font-medium text-gray-500">Accuracy</div>
                                <div className="mt-1 text-3xl font-semibold text-gray-900">{accuracy}%</div>
                            </div>
                        </div>

                        <div className="bg-white overflow-hidden shadow rounded-lg">
                            <div className="px-4 py-5 sm:p-6">
                                <div className="text-sm font-medium text-gray-500">Errors</div>
                                <div className="mt-1 text-3xl font-semibold text-gray-900">{errors}</div>
                            </div>
                        </div>
                    </div>

                    {/* Text Display */}
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
                        <div className="px-4 py-5 sm:p-6">
                            <div className="border border-gray-300 rounded-md p-6 min-h-[150px]">
                                <div className="text-lg leading-relaxed font-mono">
                                    {renderHighlightedText()}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* User Input */}
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
                        <div className="px-4 py-5 sm:p-6">
                            <label htmlFor="typing-input" className="block text-sm font-medium text-gray-700 mb-2">
                                Type the text above
                            </label>
                            <textarea
                                ref={textareaRef}
                                id="typing-input"
                                rows={6}
                                value={userInput}
                                onChange={handleInputChange}
                                onKeyDown={handleKeyDown}
                                disabled={!isTestActive && !text}
                                placeholder={isTestActive ? "" : "Click Start Test to begin..."}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm font-mono"
                            />
                        </div>
                    </div>

                    {/* Results */}
                    {results && (
                        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                            <div className="px-4 py-5 sm:p-6">
                                <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Test Results</h3>
                                <div className="grid grid-cols-1 gap-6 sm:grid-cols-3 mb-6">
                                    <div className="border border-gray-200 rounded-lg p-4 text-center">
                                        <div className="text-3xl font-bold text-indigo-600">{results.wpm}</div>
                                        <div className="text-sm text-gray-500 mt-1">Words Per Minute</div>
                                    </div>
                                    <div className="border border-gray-200 rounded-lg p-4 text-center">
                                        <div className="text-3xl font-bold text-green-600">{results.accuracy}%</div>
                                        <div className="text-sm text-gray-500 mt-1">Accuracy</div>
                                    </div>
                                    <div className="border border-gray-200 rounded-lg p-4 text-center">
                                        <div className="text-3xl font-bold text-red-600">{results.total_errors}</div>
                                        <div className="text-sm text-gray-500 mt-1">Errors</div>
                                    </div>
                                </div>

                                {results.feedback && (
                                    <div className="border-l-4 border-indigo-500 bg-indigo-50 p-4">
                                        <div className="flex">
                                            <div className="flex-shrink-0">
                                                <svg className="h-5 w-5 text-indigo-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                                                </svg>
                                            </div>
                                            <div className="ml-3">
                                                <h3 className="text-sm font-medium text-indigo-800">{results.feedback.message}</h3>
                                                <div className="mt-2 text-sm text-indigo-700">
                                                    <ul className="list-disc pl-5 space-y-1">
                                                        {results.feedback.suggestions.map((suggestion, index) => (
                                                            <li key={index}>{suggestion}</li>
                                                        ))}
                                                    </ul>
                                                </div>
                                                <p className="mt-2 text-sm text-indigo-700">
                                                    <strong>{results.feedback.encouragement}</strong>
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default TypingTest;