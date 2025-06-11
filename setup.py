"""
Setup script for the Fraud Detection System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="fraud-detection-sql",
    version="1.0.0",
    author="Data Analysis Team",
    author_email="data-team@company.com",
    description="A comprehensive fraud detection system using SQL and Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/company/fraud-detection-sql",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: SQL",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.812",
        ],
    },
    entry_points={
        "console_scripts": [
            "fraud-detection=src.main_analysis:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.sql", "*.md"],
    },
    project_urls={
        "Bug Reports": "https://github.com/company/fraud-detection-sql/issues",
        "Source": "https://github.com/company/fraud-detection-sql",
        "Documentation": "https://github.com/company/fraud-detection-sql/docs",
    },
)
