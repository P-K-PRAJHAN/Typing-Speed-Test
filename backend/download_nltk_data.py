#!/usr/bin/env python3
"""
Script to download required NLTK data
"""
import nltk
import sys

def download_nltk_data():
    print("Downloading required NLTK data...")
    
    # List of required NLTK resources
    resources = [
        'punkt',
        'punkt_tab',
        'averaged_perceptron_tagger',
        'stopwords'
    ]
    
    for resource in resources:
        try:
            print(f"Downloading {resource}...")
            nltk.download(resource, quiet=True)
            print(f"Successfully downloaded {resource}")
        except Exception as e:
            print(f"Failed to download {resource}: {e}")
    
    print("NLTK data download completed!")

if __name__ == "__main__":
    download_nltk_data()