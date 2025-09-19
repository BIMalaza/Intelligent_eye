"""
Setup script for the Intelligent Eye for the Blind system
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="intelligent-eye-blind",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A modular wearable assistive system for visually impaired individuals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/intelligent-eye-blind",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "intelligent-eye=intelligent_eye_system:main",
            "test-eye=test_system:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json", "*.txt", "*.md"],
    },
    keywords="assistive technology, computer vision, ultrasonic sensing, accessibility, visually impaired, navigation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/intelligent-eye-blind/issues",
        "Source": "https://github.com/yourusername/intelligent-eye-blind",
        "Documentation": "https://github.com/yourusername/intelligent-eye-blind/wiki",
    },
)