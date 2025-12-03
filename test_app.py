#!/usr/bin/env python3
"""
Test script to verify all components of the Typing Speed Test application
"""

import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database():
    """Test database functionality"""
    print("Testing database functionality...")
    try:
        from utils.database import DatabaseManager
        db = DatabaseManager()
        print("✓ Database manager initialized successfully")
        
        # Test saving a sample result
        db.save_test_result("easy", 50.5, 95.2, 3, 60.0)
        print("✓ Sample test result saved successfully")
        
        # Test retrieving history
        history = db.get_test_history()
        print(f"✓ Retrieved {len(history)} test records from database")
        
        # Test getting average stats
        avg_stats = db.get_average_stats()
        print(f"✓ Average stats retrieved: {avg_stats}")
        
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_texts():
    """Test text samples"""
    print("\nTesting text samples...")
    try:
        from utils.texts import TEXTS
        print(f"✓ Text samples loaded successfully")
        print(f"✓ Found {len(TEXTS)} difficulty levels: {list(TEXTS.keys())}")
        
        for level, samples in TEXTS.items():
            print(f"✓ {level.capitalize()} level has {len(samples)} text samples")
            
        return True
    except Exception as e:
        print(f"✗ Text samples test failed: {e}")
        return False

def test_analytics():
    """Test analytics module"""
    print("\nTesting analytics module...")
    try:
        from utils.analytics import AnalyticsWindow
        print("✓ Analytics module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Analytics test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Running Typing Speed Test Application Tests\n")
    
    tests = [
        test_database,
        test_texts,
        test_analytics
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print(f"\nTest Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The application is ready to use.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())