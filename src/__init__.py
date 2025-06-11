# Package initialization for fraud detection system
"""
Fraud Detection with SQL

A comprehensive fraud detection system that analyzes credit card transactions 
using SQL, PostgreSQL, Python, and data visualization techniques.

Author: Data Analysis Team
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Data Analysis Team"
__description__ = "Comprehensive fraud detection system using SQL and Python"

# Import main classes for easy access
from .data_import import FraudDetectionDatabase
from .fraud_analysis import FraudAnalyzer
from .fraud_visualization import FraudVisualizer
from .main_analysis import FraudDetectionPipeline

__all__ = [
    'FraudDetectionDatabase',
    'FraudAnalyzer', 
    'FraudVisualizer',
    'FraudDetectionPipeline'
]
