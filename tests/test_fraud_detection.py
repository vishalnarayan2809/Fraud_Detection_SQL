"""
Unit Tests for Fraud Detection System
"""

import unittest
import pandas as pd
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fraud_analysis import FraudAnalyzer
from fraud_visualization import FraudVisualizer

class TestFraudDetection(unittest.TestCase):
    """Test cases for fraud detection functionality"""
    
    def setUp(self):
        """Set up test data"""
        # Create sample transaction data
        self.sample_transactions = pd.DataFrame({
            'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'date': [
                '2018-01-01 08:30:00',  # Early morning
                '2018-01-01 14:30:00',  # Normal
                '2018-01-01 07:15:00',  # Early morning
                '2018-01-01 20:30:00',  # Normal
                '2018-01-01 08:45:00',  # Early morning
                '2018-01-01 12:30:00',  # Normal
                '2018-01-01 09:00:00',  # Early morning
                '2018-01-01 16:30:00',  # Normal
                '2018-01-01 07:30:00',  # Early morning
                '2018-01-01 22:30:00'   # Normal
            ],
            'amount': [1.50, 25.00, 1.75, 45.00, 1.25, 35.00, 1.80, 55.00, 1.95, 2500.00],
            'card': ['1234', '5678', '1234', '9012', '1234', '5678', '1234', '9012', '1234', '3456'],
            'cardholder_name': ['John', 'Jane', 'John', 'Bob', 'John', 'Jane', 'John', 'Bob', 'John', 'Alice'],
            'merchant_name': ['Coffee Shop', 'Restaurant', 'Coffee Shop', 'Gas Station', 'Coffee Shop', 'Restaurant', 'Coffee Shop', 'Gas Station', 'Coffee Shop', 'Jewelry Store'],
            'merchant_category': ['coffee shop', 'restaurant', 'coffee shop', 'gas station', 'coffee shop', 'restaurant', 'coffee shop', 'gas station', 'coffee shop', 'jewelry']
        })
        
        self.sample_transactions['date'] = pd.to_datetime(self.sample_transactions['date'])
        
    def test_early_morning_detection(self):
        """Test early morning transaction detection"""
        early_morning = self.sample_transactions[
            self.sample_transactions['date'].dt.hour.between(7, 9)
        ]
        
        # Should find 5 early morning transactions
        self.assertEqual(len(early_morning), 5)
        
        # All should be between 7-9 AM
        for _, transaction in early_morning.iterrows():
            hour = transaction['date'].hour
            self.assertGreaterEqual(hour, 7)
            self.assertLessEqual(hour, 9)
            
    def test_small_transaction_detection(self):
        """Test small transaction detection"""
        small_transactions = self.sample_transactions[
            self.sample_transactions['amount'] < 2.00
        ]
        
        # Should find transactions under $2
        self.assertGreater(len(small_transactions), 0)
        
        # All amounts should be under $2
        for _, transaction in small_transactions.iterrows():
            self.assertLess(transaction['amount'], 2.00)
            
    def test_card_pattern_analysis(self):
        """Test card transaction pattern analysis"""
        # Group by card and count small transactions
        small_tx_by_card = self.sample_transactions[
            self.sample_transactions['amount'] < 2.00
        ].groupby('card').size()
        
        # Card '1234' should have multiple small transactions
        self.assertIn('1234', small_tx_by_card.index)
        self.assertGreater(small_tx_by_card['1234'], 1)
        
    def test_outlier_detection(self):
        """Test statistical outlier detection"""
        amounts = self.sample_transactions['amount']
        mean_amount = amounts.mean()
        std_amount = amounts.std()
        
        # Calculate Z-scores
        z_scores = abs(amounts - mean_amount) / std_amount
        outliers = self.sample_transactions[z_scores > 2]
        
        # Should detect the $2500 transaction as outlier
        self.assertGreater(len(outliers), 0)
        self.assertIn(2500.00, outliers['amount'].values)
        
    def test_fraud_visualizer_initialization(self):
        """Test fraud visualizer can be initialized"""
        visualizer = FraudVisualizer()
        self.assertIsNotNone(visualizer)
        self.assertIsNotNone(visualizer.color_palette)
        
    def test_data_validation(self):
        """Test data validation functions"""
        # Check required columns exist
        required_columns = ['id', 'date', 'amount', 'card']
        for col in required_columns:
            self.assertIn(col, self.sample_transactions.columns)
            
        # Check data types
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.sample_transactions['date']))
        self.assertTrue(pd.api.types.is_numeric_dtype(self.sample_transactions['amount']))
        
    def test_risk_scoring(self):
        """Test basic risk scoring logic"""
        # Simple risk score based on small transactions and early morning activity
        for _, transaction in self.sample_transactions.iterrows():
            risk_score = 0
            
            # Small transaction risk
            if transaction['amount'] < 2.00:
                risk_score += 0.3
                
            # Early morning risk
            if 7 <= transaction['date'].hour <= 9:
                risk_score += 0.2
                
            # High amount risk
            if transaction['amount'] > 1000:
                risk_score += 0.5
                
            # Risk score should be between 0 and 1
            self.assertGreaterEqual(risk_score, 0)
            self.assertLessEqual(risk_score, 1)
            
class TestDataIntegrity(unittest.TestCase):
    """Test data integrity and file structure"""
    
    def setUp(self):
        self.project_root = Path(__file__).parent.parent
        
    def test_required_directories(self):
        """Test that all required directories exist"""
        required_dirs = ['src', 'data', 'sql', 'config', 'docs', 'tests', 'scripts']
        
        for directory in required_dirs:
            dir_path = self.project_root / directory
            self.assertTrue(dir_path.exists(), f"Directory {directory} should exist")
            self.assertTrue(dir_path.is_dir(), f"{directory} should be a directory")
            
    def test_required_files(self):
        """Test that all required files exist"""
        required_files = [
            'src/__init__.py',
            'config/database.yaml',
            'config/fraud_rules.yaml',
            'requirements.txt',
            'setup.py',
            '.gitignore'
        ]
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            self.assertTrue(full_path.exists(), f"File {file_path} should exist")
            self.assertTrue(full_path.is_file(), f"{file_path} should be a file")
            
    def test_csv_data_files(self):
        """Test that CSV data files exist and have content"""
        csv_files = [
            'data/card_holder.csv',
            'data/credit_card.csv', 
            'data/merchant.csv',
            'data/merchant_category.csv',
            'data/transaction.csv'
        ]
        
        for csv_file in csv_files:
            file_path = self.project_root / csv_file
            self.assertTrue(file_path.exists(), f"CSV file {csv_file} should exist")
            
            # Check file has content
            self.assertGreater(file_path.stat().st_size, 0, f"{csv_file} should not be empty")

def run_tests():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestFraudDetection))
    test_suite.addTest(unittest.makeSuite(TestDataIntegrity))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return success status
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
