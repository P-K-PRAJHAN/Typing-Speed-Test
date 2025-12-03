// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getAnalytics } from "firebase/analytics";

// TODO: Replace with your Firebase project configuration
const firebaseConfig = {
  apiKey: "AIzaSyD25wCPS-LW--qGaarfMWGuHkE879hNMpU",
  authDomain: "typetest-b061f.firebaseapp.com",
  projectId: "typetest-b061f",
  storageBucket: "typetest-b061f.firebasestorage.app",
  messagingSenderId: "636222197722",
  appId: "1:636222197722:web:4d864a930ef1266c1efae3",
  measurementId: "G-3DL7LK00MK"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);

export default app;