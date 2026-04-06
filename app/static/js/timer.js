// Global variables
let timer;
let timeLeft = 0;
let isTestRunning = false;
let originalText = "";
let currentCharIndex = 0;
let errors = 0;
let startTime;

// DOM Elements
const timerElement = document.getElementById("timer");
const textDisplay = document.getElementById("text-display");
const typingArea = document.getElementById("typing-area");
const wpmElement = document.getElementById("wpm");
const accuracyElement = document.getElementById("accuracy");
const errorsElement = document.getElementById("errors");
const resultsSection = document.getElementById("results");
const finalWpmElement = document.getElementById("final-wpm");
const finalAccuracyElement = document.getElementById("final-accuracy");
const feedbackElement = document.getElementById("feedback");
const restartButton = document.getElementById("restart-button");
const newTestButton = document.getElementById("new-test-button");

// Event Listeners
document.addEventListener("DOMContentLoaded", () => {
  // Focus the typing area when the page loads
  typingArea.focus();

  // Initialize the test
  initializeTest();

  // Event listeners for buttons
  if (restartButton) {
    restartButton.addEventListener("click", restartTest);
  }

  if (newTestButton) {
    newTestButton.addEventListener("click", () => {
      window.location.href = "/test/medium"; // Default to medium difficulty
    });
  }

  // Typing area event listeners
  typingArea.addEventListener("input", handleTyping);
  typingArea.addEventListener("keydown", (e) => {
    // Prevent tab from moving focus
    if (e.key === "Tab") {
      e.preventDefault();
    }
  });
});

// Initialize the typing test
function initializeTest() {
  // Get the original text from the display without trimming (preserve leading/trailing spaces)
  originalText = textDisplay.textContent;

  // Reset variables
  currentCharIndex = 0;
  errors = 0;
  isTestRunning = false;

  // Clear the typing area
  typingArea.value = "";

  // Hide results section if visible
  if (resultsSection) {
    resultsSection.style.display = "none";
  }

  // Reset stats
  updateStats();

  // Highlight the first character
  highlightCurrentChar();
}

// Handle typing input
function handleTyping(e) {
  // Start the timer on first key press if not already running
  if (!isTestRunning) {
    startTest();
  }

  const typedText = typingArea.value;
  const currentChar = originalText[currentCharIndex];

  // Check if the typed character matches the expected character
  if (typedText[currentCharIndex] === currentChar) {
    // Correct character
    currentCharIndex++;
    updateDisplay();
  } else {
    // Incorrect character
    errors++;
    updateStats();
  }

  // Check if test is complete
  if (currentCharIndex >= originalText.length) {
    finishTest();
  }
}

// Start the test timer
function startTest() {
  isTestRunning = true;
  startTime = new Date().getTime();

  // Update timer every 10ms for smooth display
  timer = setInterval(updateTimer, 10);
}

// Update the timer display
function updateTimer() {
  const currentTime = new Date().getTime();
  const elapsedTime = (currentTime - startTime) / 1000; // in seconds
  timeLeft = Math.max(0, 300 - elapsedTime); // 5 minutes max

  // Format time as MM:SS
  const minutes = Math.floor(timeLeft / 60);
  const seconds = Math.floor(timeLeft % 60);
  const formattedTime = `${minutes.toString().padStart(2, "0")}:${seconds
    .toString()
    .padStart(2, "0")}`;

  if (timerElement) {
    timerElement.textContent = formattedTime;
  }

  // Update WPM and accuracy in real-time
  updateStats();

  // End test if time is up
  if (timeLeft <= 0) {
    finishTest();
  }
}

// Update the display with highlighted text
function updateDisplay() {
  // Clear the display
  textDisplay.innerHTML = "";

  // Add each character with appropriate highlighting
  for (let i = 0; i < originalText.length; i++) {
    const char = originalText[i];
    const span = document.createElement("span");

    if (i < currentCharIndex) {
      // Already typed characters
      span.className = "correct";
    } else if (i === currentCharIndex) {
      // Current character
      span.className = "current";
    }

    // Handle special characters
    if (char === " ") {
      span.innerHTML = "&nbsp;";
    } else if (char === "\n") {
      span.innerHTML = "<br>";
    } else if (char === "\t") {
      span.innerHTML = "&nbsp;&nbsp;&nbsp;&nbsp;";
    } else {
      span.textContent = char;
    }

    textDisplay.appendChild(span);
  }

  // Update stats
  updateStats();
}

// Highlight the current character
function highlightCurrentChar() {
  const spans = textDisplay.getElementsByTagName("span");

  // Remove current class from all spans
  for (const span of spans) {
    span.classList.remove("current");
  }

  // Add current class to the current character
  if (spans[currentCharIndex]) {
    spans[currentCharIndex].classList.add("current");
  }
}

// Update the statistics (WPM, accuracy, errors)
function updateStats() {
  const timeElapsed = (new Date().getTime() - startTime) / 1000 / 60; // in minutes
  const typedChars = currentCharIndex;
  const wordsTyped = typedChars / 5; // Standard word is 5 characters
  const wpm = Math.round((wordsTyped / timeElapsed) * 100) / 100 || 0;

  const totalChars = originalText.length;
  const accuracy = Math.max(0, ((typedChars - errors) / typedChars) * 100) || 0;

  // Update the UI
  if (wpmElement) wpmElement.textContent = wpm.toFixed(1);
  if (accuracyElement) accuracyElement.textContent = accuracy.toFixed(1) + "%";
  if (errorsElement) errorsElement.textContent = errors;

  return { wpm, accuracy, errors };
}

// Finish the test
function finishTest() {
  // Stop the timer
  clearInterval(timer);
  isTestRunning = false;

  // Disable the typing area
  typingArea.disabled = true;

  // Calculate final stats
  const timeElapsed = (new Date().getTime() - startTime) / 1000; // in seconds
  const stats = updateStats();

  // Show results section
  if (resultsSection) {
    resultsSection.style.display = "block";
    finalWpmElement.textContent = stats.wpm.toFixed(1);
    finalAccuracyElement.textContent = stats.accuracy.toFixed(1) + "%";

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: "smooth" });
  }

  // Send results to the server
  submitResults(stats, timeElapsed);
}

// Submit test results to the server
function submitResults(stats, timeElapsed) {
  const formData = new FormData();
  formData.append("typed_text", typingArea.value);

  fetch("/submit_test", {
    method: "POST",
    body: formData,
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken") || "",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success && feedbackElement) {
        // Display feedback from the server
        feedbackElement.textContent = data.feedback;
        feedbackElement.style.display = "block";
      }
    })
    .catch((error) => {
      console.error("Error submitting test results:", error);
    });
}

// Restart the test
function restartTest() {
  // Reset the typing area
  typingArea.value = "";
  typingArea.disabled = false;

  // Hide results
  if (resultsSection) {
    resultsSection.style.display = "none";
  }

  // Re-initialize the test
  initializeTest();

  // Focus the typing area
  typingArea.focus();
}

// Helper function to get cookie value
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Handle window resize
window.addEventListener("resize", () => {
  // Recalculate and adjust layout if needed
});

// Handle page visibility changes
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    // Pause the timer when the tab is not active
    if (isTestRunning) {
      clearInterval(timer);
    }
  } else if (isTestRunning) {
    // Resume the timer when the tab becomes active again
    startTest();
  }
});

// Handle beforeunload event to warn about unsaved changes
window.addEventListener("beforeunload", (e) => {
  if (isTestRunning) {
    e.preventDefault();
    e.returnValue = "You have an ongoing test. Are you sure you want to leave?";
    return e.returnValue;
  }
});
