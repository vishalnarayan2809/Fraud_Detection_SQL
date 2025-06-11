"""
Main Fraud Detection Analysis Script
This script orchestrates the complete fraud detection analysis
"""

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import logging
import os
from datetime import datetime
import json
from pathlib import Path

# Import our custom modules
from .data_import import FraudDetectionDatabase
from .fraud_analysis import FraudAnalyzer
from .fraud_visualization import FraudVisualizer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fraud_detection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FraudDetectionPipeline:
    def __init__(self, db_config):
        """
        Initialize the fraud detection pipeline
        
        Args:
            db_config (dict): Database configuration
        """
        self.db_config = db_config
        self.engine = None
        self.analyzer = None
        self.visualizer = FraudVisualizer()
        
    def setup_database(self):
        """Setup database connection and schema"""
        logger.info("Setting up database connection...")
        
        # Initialize database handler
        fraud_db = FraudDetectionDatabase(self.db_config)
          # Create connection
        if not fraud_db.create_connection():
            logger.error("Failed to create database connection")
            return False
        
        self.engine = fraud_db.engine
        
        # Execute schema
        schema_file = Path(__file__).parent.parent / 'sql' / 'schema.sql'
        if not fraud_db.execute_schema(schema_file):
            logger.error("Failed to execute database schema")
            return False
        
        # Load CSV data
        data_directory = Path(__file__).parent.parent / 'data'
        if not fraud_db.load_csv_data(data_directory):
            logger.error("Failed to load CSV data")
            return False
        
        # Validate data integrity
        if not fraud_db.validate_data_integrity():
            logger.error("Data integrity validation failed")
            return False
        
        # Initialize analyzer
        self.analyzer = FraudAnalyzer(self.engine)
        
        logger.info("Database setup completed successfully")
        return True
    
    def run_fraud_analysis(self):
        """Run comprehensive fraud analysis"""
        logger.info("Starting fraud analysis...")
        
        if not self.analyzer:
            logger.error("Analyzer not initialized. Please setup database first.")
            return None
        
        results = {}
        
        try:
            # 1. Top 100 early morning high-value transactions
            logger.info("Analyzing early morning transactions...")
            results['early_morning_transactions'] = self.analyzer.get_top_100_early_morning_transactions()
            
            # 2. Small transactions per cardholder
            logger.info("Analyzing small transactions per cardholder...")
            results['small_transactions'] = self.analyzer.count_small_transactions_per_cardholder()
            
            # 3. Top 5 vulnerable merchants
            logger.info("Identifying vulnerable merchants...")
            results['vulnerable_merchants'] = self.analyzer.identify_top_5_vulnerable_merchants()
            
            # 4. Hourly transaction patterns
            logger.info("Analyzing hourly transaction patterns...")
            results['hourly_patterns'] = self.analyzer.analyze_transaction_patterns_by_hour()
            
            # 5. Cardholder spending patterns
            logger.info("Analyzing cardholder spending patterns...")
            results['spending_patterns'] = self.analyzer.get_cardholder_spending_patterns()
            
            # 6. Outlier detection
            logger.info("Detecting outlier transactions...")
            results['outliers'] = self.analyzer.detect_outlier_transactions()
            
            # 7. Rapid transaction analysis
            logger.info("Analyzing rapid transactions...")
            results['rapid_transactions'] = self.analyzer.analyze_rapid_transactions()
            
            # 8. Generate summary report
            logger.info("Generating fraud summary report...")
            results['summary'] = self.analyzer.generate_fraud_summary_report()
            
            logger.info("Fraud analysis completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error during fraud analysis: {e}")
            return None
    
    def create_visualizations(self, analysis_results):
        """Create visualizations from analysis results"""
        logger.info("Creating visualizations...")
        
        try:
            # Get all transactions for distribution analysis
            all_transactions_query = """
            SELECT 
                t.*,
                ch.name as cardholder_name,
                m.name as merchant_name,
                mc.name as merchant_category
            FROM transaction t
            JOIN credit_card cc ON t.card = cc.card
            JOIN card_holder ch ON cc.id_card_holder = ch.id
            JOIN merchant m ON t.id_merchant = m.id
            JOIN merchant_category mc ON m.id_merchant_category = mc.id
            """
            
            all_transactions = pd.read_sql_query(all_transactions_query, self.engine)
            
            # Create dashboard
            dashboard_plots = self.visualizer.create_fraud_summary_dashboard(
                summary_data=analysis_results['summary'],
                transactions_df=all_transactions,
                hourly_data=analysis_results['hourly_patterns'],
                vulnerable_merchants=analysis_results['vulnerable_merchants'],
                small_transactions=analysis_results['small_transactions'],
                outliers=analysis_results['outliers']
            )
            
            # Save plots to HTML files
            self.visualizer.save_plots_to_html(dashboard_plots)
            
            logger.info("Visualizations created and saved successfully")
            return dashboard_plots
            
        except Exception as e:
            logger.error(f"Error creating visualizations: {e}")
            return {}
    
    def generate_report(self, analysis_results, output_file="fraud_detection_report.json"):
        """Generate comprehensive fraud detection report"""
        logger.info("Generating comprehensive report...")
        
        try:            # Create output directory
            reports_dir = Path(__file__).parent.parent / 'reports'
            reports_dir.mkdir(exist_ok=True)
            
            # Prepare report data
            report = {
                'report_metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'analysis_type': 'Comprehensive Fraud Detection Analysis',
                    'database_connection': f"{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
                },
                'executive_summary': analysis_results['summary'],
                'detailed_findings': {
                    'early_morning_suspicious_transactions': {
                        'count': len(analysis_results['early_morning_transactions']),
                        'description': 'High-value transactions occurring between 7-9 AM, potentially indicating unauthorized access',
                        'top_5_amounts': analysis_results['early_morning_transactions']['amount'].nlargest(5).tolist() if len(analysis_results['early_morning_transactions']) > 0 else []
                    },
                    'small_transaction_fraud_indicators': {
                        'affected_cards': len(analysis_results['small_transactions']),
                        'description': 'Cards with multiple small transactions (<$2), indicating potential card testing fraud',
                        'highest_risk_cards': analysis_results['small_transactions']['small_transaction_count'].nlargest(5).tolist() if len(analysis_results['small_transactions']) > 0 else []
                    },
                    'vulnerable_merchants': {
                        'count': len(analysis_results['vulnerable_merchants']),
                        'description': 'Merchants most susceptible to small transaction fraud',
                        'top_merchants': analysis_results['vulnerable_merchants']['merchant_name'].tolist() if len(analysis_results['vulnerable_merchants']) > 0 else []
                    },
                    'statistical_outliers': {
                        'count': len(analysis_results['outliers']),
                        'description': 'Transactions identified as statistical outliers using IQR and Z-score methods',
                        'extreme_outliers': len(analysis_results['outliers'][analysis_results['outliers']['z_score'] > 5]) if len(analysis_results['outliers']) > 0 else 0
                    }
                },
                'recommendations': [
                    'Implement real-time monitoring for transactions between 7-9 AM with amounts above average',
                    'Set up alerts for cards with more than 5 transactions under $2.00 within a 24-hour period',
                    'Review and enhance security measures for merchants identified as vulnerable',
                    'Investigate all transactions flagged as extreme statistical outliers (Z-score > 5)',
                    'Consider implementing velocity checks for rapid successive transactions',
                    'Regular review of transaction patterns to identify emerging fraud trends'
                ]
            }
            
            # Convert DataFrames to dictionaries for JSON serialization
            def convert_df_to_dict(df):
                if isinstance(df, pd.DataFrame) and len(df) > 0:
                    return df.head(10).to_dict('records')  # Limit to top 10 for report size
                return []
            
            report['detailed_data'] = {
                'top_early_morning_transactions': convert_df_to_dict(analysis_results['early_morning_transactions']),
                'top_small_transaction_cards': convert_df_to_dict(analysis_results['small_transactions']),
                'most_vulnerable_merchants': convert_df_to_dict(analysis_results['vulnerable_merchants']),
                'top_outlier_transactions': convert_df_to_dict(analysis_results['outliers']),
                'hourly_patterns': convert_df_to_dict(analysis_results['hourly_patterns'])
            }
            
            # Save report
            report_file = os.path.join(reports_dir, output_file)
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            # Also save individual CSV files for detailed analysis
            for key, df in analysis_results.items():
                if isinstance(df, pd.DataFrame) and len(df) > 0:
                    csv_file = os.path.join(reports_dir, f"{key}.csv")
                    df.to_csv(csv_file, index=False)
                    logger.info(f"Saved {key} data to {csv_file}")
            
            logger.info(f"Comprehensive report saved to {report_file}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return None
    
    def run_complete_analysis(self):
        """Run the complete fraud detection pipeline"""
        logger.info("Starting complete fraud detection analysis...")
        
        # Step 1: Setup database
        if not self.setup_database():
            logger.error("Database setup failed. Stopping analysis.")
            return False
        
        # Step 2: Run fraud analysis
        analysis_results = self.run_fraud_analysis()
        if not analysis_results:
            logger.error("Fraud analysis failed. Stopping pipeline.")
            return False
        
        # Step 3: Create visualizations
        visualizations = self.create_visualizations(analysis_results)
        
        # Step 4: Generate report
        report = self.generate_report(analysis_results)
        
        if report:
            logger.info("Complete fraud detection analysis finished successfully!")
            
            # Print summary to console
            print("\n" + "="*60)
            print("FRAUD DETECTION ANALYSIS SUMMARY")
            print("="*60)
            print(f"Total Transactions Analyzed: {report['executive_summary']['basic_statistics']['total_transactions']:,}")
            print(f"Unique Cards: {report['executive_summary']['basic_statistics']['unique_cards']:,}")
            print(f"Unique Merchants: {report['executive_summary']['basic_statistics']['unique_merchants']:,}")
            print(f"Total Transaction Volume: ${report['executive_summary']['basic_statistics']['total_volume']:,.2f}")
            print("\nFRAUD INDICATORS:")
            print(f"- Cards with Small Transactions: {report['executive_summary']['fraud_indicators']['cards_with_small_transactions']}")
            print(f"- Outlier Transactions: {report['executive_summary']['fraud_indicators']['outlier_transactions']}")
            print(f"- Suspicious Early Morning Transactions: {report['executive_summary']['fraud_indicators']['suspicious_early_morning_transactions']}")
            print(f"- Vulnerable Merchants: {report['executive_summary']['fraud_indicators']['vulnerable_merchants']}")
            print("\nRISK ASSESSMENT:")
            print(f"- High Risk Cards: {report['executive_summary']['risk_assessment']['high_risk_cards']}")
            print(f"- Extreme Outliers: {report['executive_summary']['risk_assessment']['extreme_outliers']}")
            print(f"- High-Value Early Morning Transactions: {report['executive_summary']['risk_assessment']['early_morning_high_value']}")
            print("="*60)
            
            return True
        else:
            logger.error("Report generation failed.")
            return False

def main():
    """Main function to run fraud detection analysis"""
    
    # Database configuration
    # Note: Update these credentials according to your PostgreSQL setup
    db_config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'fraud_detection',
        'user': 'postgres',
        'password': 'your_password_here'  # Update this with your actual password
    }
    
    # Initialize and run pipeline
    pipeline = FraudDetectionPipeline(db_config)
    success = pipeline.run_complete_analysis()
    
    if success:
        print("\nFraud detection analysis completed successfully!")
        print("Check the 'reports' folder for detailed results and visualizations.")
    else:
        print("\nFraud detection analysis failed. Check logs for details.")

if __name__ == "__main__":
    main()
