"""
Fraud Detection Data Import and Database Setup
This script imports CSV data into PostgreSQL database
"""

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import psycopg2
import os
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FraudDetectionDatabase:
    def __init__(self, db_config):
        """
        Initialize database connection
        
        Args:
            db_config (dict): Database configuration parameters
        """
        self.db_config = db_config
        self.engine = None
        self.connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        
    def create_connection(self):
        """Create database connection"""
        try:
            self.engine = create_engine(self.connection_string)
            logger.info("Database connection established successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to create database connection: {e}")
            return False
    
    def execute_schema(self, schema_file):
        """Execute SQL schema file"""
        try:
            with open(schema_file, 'r') as file:
                schema_sql = file.read()
            
            with self.engine.connect() as conn:
                # Split by semicolon and execute each statement
                statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
                for statement in statements:
                    if statement:
                        conn.execute(sqlalchemy.text(statement))
                conn.commit()
            
            logger.info("Database schema created successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to execute schema: {e}")
            return False
    
    def load_csv_data(self, data_directory):
        """Load all CSV files into database tables"""
        csv_files = {
            'merchant_category': 'merchant_category.csv',
            'card_holder': 'card_holder.csv',
            'merchant': 'merchant.csv',
            'credit_card': 'credit_card.csv',
            'transaction': 'transaction.csv'
        }
        
        try:
            # Load data in dependency order
            for table_name, csv_file in csv_files.items():
                file_path = os.path.join(data_directory, csv_file)
                
                if not os.path.exists(file_path):
                    logger.warning(f"CSV file not found: {file_path}")
                    continue
                
                df = pd.read_csv(file_path)
                
                # Special handling for different tables
                if table_name == 'transaction':
                    # Convert date column to datetime
                    df['date'] = pd.to_datetime(df['date'])
                    # Ensure amount is numeric
                    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
                elif table_name == 'credit_card':
                    # Handle scientific notation in card numbers
                    df['card'] = df['card'].apply(lambda x: f"{x:.0f}" if pd.notnull(x) else x)
                
                # Import to database
                df.to_sql(table_name, self.engine, if_exists='append', index=False, method='multi')
                logger.info(f"Loaded {len(df)} records into {table_name} table")
            
            logger.info("All CSV data loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load CSV data: {e}")
            return False
    
    def validate_data_integrity(self):
        """Validate data integrity and relationships"""
        try:
            with self.engine.connect() as conn:
                # Check for orphaned records
                orphaned_queries = [
                    "SELECT COUNT(*) as orphaned_credit_cards FROM credit_card cc LEFT JOIN card_holder ch ON cc.id_card_holder = ch.id WHERE ch.id IS NULL",
                    "SELECT COUNT(*) as orphaned_merchants FROM merchant m LEFT JOIN merchant_category mc ON m.id_merchant_category = mc.id WHERE mc.id IS NULL",
                    "SELECT COUNT(*) as orphaned_transactions_card FROM transaction t LEFT JOIN credit_card cc ON t.card = cc.card WHERE cc.card IS NULL",
                    "SELECT COUNT(*) as orphaned_transactions_merchant FROM transaction t LEFT JOIN merchant m ON t.id_merchant = m.id WHERE m.id IS NULL"
                ]
                
                for query in orphaned_queries:
                    result = conn.execute(sqlalchemy.text(query)).fetchone()
                    logger.info(f"Integrity check: {query.split('as ')[1].split(' FROM')[0]} = {result[0]}")
                
                # Basic statistics
                stats_queries = [
                    "SELECT COUNT(*) as total_cardholders FROM card_holder",
                    "SELECT COUNT(*) as total_credit_cards FROM credit_card",
                    "SELECT COUNT(*) as total_merchants FROM merchant",
                    "SELECT COUNT(*) as total_categories FROM merchant_category",
                    "SELECT COUNT(*) as total_transactions FROM transaction",
                    "SELECT MIN(date) as earliest_transaction, MAX(date) as latest_transaction FROM transaction",
                    "SELECT MIN(amount) as min_amount, MAX(amount) as max_amount, AVG(amount) as avg_amount FROM transaction"
                ]
                
                for query in stats_queries:
                    result = conn.execute(sqlalchemy.text(query)).fetchone()
                    logger.info(f"Database stats: {result}")
            
            return True
            
        except Exception as e:
            logger.error(f"Data integrity validation failed: {e}")
            return False

def main():
    """Main function to setup database and import data"""
    
    # Database configuration
    # Note: Update these credentials according to your PostgreSQL setup
    db_config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'fraud_detection',
        'user': 'postgres',
        'password': 'your_password_here'  # Update this
    }
    
    # Initialize database handler
    fraud_db = FraudDetectionDatabase(db_config)
    
    # Create connection
    if not fraud_db.create_connection():
        logger.error("Cannot proceed without database connection")
        return False
      # Execute schema
    schema_file = r'c:\Users\guruk\Fraud Detection\sql\schema.sql'
    if not fraud_db.execute_schema(schema_file):
        logger.error("Cannot proceed without proper schema")
        return False
    
    # Load CSV data
    data_directory = r'c:\Users\guruk\Fraud Detection\data'
    if not fraud_db.load_csv_data(data_directory):
        logger.error("Data loading failed")
        return False
    
    # Validate data integrity
    if not fraud_db.validate_data_integrity():
        logger.error("Data integrity validation failed")
        return False
    
    logger.info("Database setup and data import completed successfully!")
    return True

if __name__ == "__main__":
    main()
