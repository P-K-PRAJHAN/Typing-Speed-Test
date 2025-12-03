from setuptools import setup, find_packages

setup(
    name="typing-speed-test",
    version="1.0.0",
    description="A desktop application to test and improve your typing speed and accuracy",
    author="Developer",
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.5.0",
    ],
    entry_points={
        "console_scripts": [
            "typing-test=main:main",
        ],
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)