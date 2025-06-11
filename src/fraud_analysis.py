"""
Fraud Detection Analysis Module
This script contains SQL queries and analysis functions for detecting fraudulent transactions
"""

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class FraudAnalyzer:
    def __init__(self, engine):
        """
        Initialize fraud analyzer with database engine
        
        Args:
            engine: SQLAlchemy database engine
        """
        self.engine = engine
    
    def get_top_100_early_morning_transactions(self):
        """
        Find the top 100 highest transactions during early morning hours (7-9 AM)
        
        Returns:
            pandas.DataFrame: Top 100 highest early morning transactions
        """
        query = """
        SELECT 
            t.id,
            t.date,
            t.amount,
            t.card,
            ch.name as cardholder_name,
            m.name as merchant_name,
            mc.name as merchant_category,
            EXTRACT(HOUR FROM t.date) as hour_of_transaction
        FROM transaction t
        JOIN credit_card cc ON t.card = cc.card
        JOIN card_holder ch ON cc.id_card_holder = ch.id
        JOIN merchant m ON t.id_merchant = m.id
        JOIN merchant_category mc ON m.id_merchant_category = mc.id
        WHERE EXTRACT(HOUR FROM t.date) BETWEEN 7 AND 9
        ORDER BY t.amount DESC
        LIMIT 100;
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            logger.info(f"Retrieved {len(df)} early morning high-value transactions")
            return df
        except Exception as e:
            logger.error(f"Error retrieving early morning transactions: {e}")
            return pd.DataFrame()
    
    def count_small_transactions_per_cardholder(self):
        """
        Count transactions less than $2.00 per cardholder to check for hacked cards
        
        Returns:
            pandas.DataFrame: Small transactions count per cardholder
        """
        query = """
        SELECT 
            t.card,
            ch.name as cardholder_name,
            COUNT(*) as small_transaction_count,
            AVG(t.amount) as avg_small_amount,
            MIN(t.amount) as min_amount,
            MAX(t.amount) as max_amount,
            STRING_AGG(DISTINCT mc.name, ', ') as merchant_categories_used
        FROM transaction t
        JOIN credit_card cc ON t.card = cc.card
        JOIN card_holder ch ON cc.id_card_holder = ch.id
        JOIN merchant m ON t.id_merchant = m.id
        JOIN merchant_category mc ON m.id_merchant_category = mc.id
        WHERE t.amount < 2.00
        GROUP BY t.card, ch.name
        ORDER BY small_transaction_count DESC;
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            logger.info(f"Found {len(df)} cardholders with small transactions")
            return df
        except Exception as e:
            logger.error(f"Error retrieving small transactions: {e}")
            return pd.DataFrame()
    
    def identify_top_5_vulnerable_merchants(self):
        """
        Identify the top 5 merchants prone to being hacked with small transactions
        
        Returns:
            pandas.DataFrame: Top 5 merchants with most small transactions
        """
        query = """
        SELECT 
            m.id as merchant_id,
            m.name as merchant_name,
            mc.name as merchant_category,
            COUNT(*) as small_transaction_count,
            AVG(t.amount) as avg_small_amount,
            COUNT(DISTINCT t.card) as unique_cards_affected,
            COUNT(DISTINCT ch.id) as unique_cardholders_affected,
            MIN(t.amount) as min_transaction,
            MAX(t.amount) as max_transaction
        FROM transaction t
        JOIN merchant m ON t.id_merchant = m.id
        JOIN merchant_category mc ON m.id_merchant_category = mc.id
        JOIN credit_card cc ON t.card = cc.card
        JOIN card_holder ch ON cc.id_card_holder = ch.id
        WHERE t.amount < 2.00
        GROUP BY m.id, m.name, mc.name
        ORDER BY small_transaction_count DESC
        LIMIT 5;
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            logger.info(f"Identified top {len(df)} vulnerable merchants")
            return df
        except Exception as e:
            logger.error(f"Error identifying vulnerable merchants: {e}")
            return pd.DataFrame()
    
    def analyze_transaction_patterns_by_hour(self):
        """
        Analyze transaction patterns by hour of day
        
        Returns:
            pandas.DataFrame: Transaction patterns by hour
        """
        query = """
        SELECT 
            EXTRACT(HOUR FROM date) as hour_of_day,
            COUNT(*) as transaction_count,
            AVG(amount) as avg_amount,
            SUM(amount) as total_amount,
            MIN(amount) as min_amount,
            MAX(amount) as max_amount,
            STDDEV(amount) as amount_stddev
        FROM transaction
        GROUP BY EXTRACT(HOUR FROM date)
        ORDER BY hour_of_day;
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            logger.info("Retrieved hourly transaction patterns")
            return df
        except Exception as e:
            logger.error(f"Error analyzing hourly patterns: {e}")
            return pd.DataFrame()
    
    def get_cardholder_spending_patterns(self):
        """
        Get comprehensive spending patterns for each cardholder
        
        Returns:
            pandas.DataFrame: Cardholder spending analysis
        """
        query = """
        SELECT 
            ch.id,
            ch.name as cardholder_name,
            COUNT(t.id) as total_transactions,
            AVG(t.amount) as avg_transaction_amount,
            SUM(t.amount) as total_spent,
            MIN(t.amount) as min_transaction,
            MAX(t.amount) as max_transaction,
            STDDEV(t.amount) as amount_stddev,
            COUNT(DISTINCT m.id) as unique_merchants_used,
            COUNT(DISTINCT mc.name) as unique_categories_used,
            MIN(t.date) as first_transaction,
            MAX(t.date) as last_transaction
        FROM card_holder ch
        JOIN credit_card cc ON ch.id = cc.id_card_holder
        JOIN transaction t ON cc.card = t.card
        JOIN merchant m ON t.id_merchant = m.id
        JOIN merchant_category mc ON m.id_merchant_category = mc.id
        GROUP BY ch.id, ch.name
        ORDER BY total_spent DESC;
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            logger.info(f"Retrieved spending patterns for {len(df)} cardholders")
            return df
        except Exception as e:
            logger.error(f"Error retrieving spending patterns: {e}")
            return pd.DataFrame()
    
    def detect_outlier_transactions(self):
        """
        Detect outlier transactions using statistical methods
        
        Returns:
            pandas.DataFrame: Outlier transactions
        """
        query = """
        WITH transaction_stats AS (
            SELECT 
                AVG(amount) as mean_amount,
                STDDEV(amount) as stddev_amount,
                PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY amount) as q1,
                PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY amount) as q3
            FROM transaction
        ),
        outlier_bounds AS (
            SELECT 
                mean_amount,
                stddev_amount,
                q1,
                q3,
                q1 - 1.5 * (q3 - q1) as iqr_lower_bound,
                q3 + 1.5 * (q3 - q1) as iqr_upper_bound,
                mean_amount - 3 * stddev_amount as zscore_lower_bound,
                mean_amount + 3 * stddev_amount as zscore_upper_bound
            FROM transaction_stats
        )
        SELECT 
            t.id,
            t.date,
            t.amount,
            t.card,
            ch.name as cardholder_name,
            m.name as merchant_name,
            mc.name as merchant_category,
            CASE 
                WHEN t.amount < ob.iqr_lower_bound OR t.amount > ob.iqr_upper_bound THEN 'IQR_Outlier'
                WHEN t.amount < ob.zscore_lower_bound OR t.amount > ob.zscore_upper_bound THEN 'ZScore_Outlier'
                ELSE 'Normal'
            END as outlier_type,
            ob.mean_amount,
            ob.stddev_amount,
            ABS(t.amount - ob.mean_amount) / NULLIF(ob.stddev_amount, 0) as z_score,
            EXTRACT(HOUR FROM t.date) as hour_of_transaction,
            EXTRACT(DOW FROM t.date) as day_of_week
        FROM transaction t
        JOIN credit_card cc ON t.card = cc.card
        JOIN card_holder ch ON cc.id_card_holder = ch.id
        JOIN merchant m ON t.id_merchant = m.id
        JOIN merchant_category mc ON m.id_merchant_category = mc.id
        CROSS JOIN outlier_bounds ob
        WHERE t.amount < ob.iqr_lower_bound 
           OR t.amount > ob.iqr_upper_bound 
           OR t.amount < ob.zscore_lower_bound 
           OR t.amount > ob.zscore_upper_bound
        ORDER BY ABS(t.amount - ob.mean_amount) / NULLIF(ob.stddev_amount, 0) DESC;
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            logger.info(f"Detected {len(df)} outlier transactions")
            return df
        except Exception as e:
            logger.error(f"Error detecting outliers: {e}")
            return pd.DataFrame()
    
    def analyze_rapid_transactions(self, time_window_minutes=5, min_transaction_count=3):
        """
        Detect rapid successive transactions that might indicate fraud
        
        Args:
            time_window_minutes (int): Time window in minutes to look for rapid transactions
            min_transaction_count (int): Minimum number of transactions in time window to flag
            
        Returns:
            pandas.DataFrame: Rapid transaction patterns
        """
        query = f"""
        WITH transaction_with_lag AS (
            SELECT 
                t.*,
                ch.name as cardholder_name,
                m.name as merchant_name,
                mc.name as merchant_category,
                LAG(t.date) OVER (PARTITION BY t.card ORDER BY t.date) as prev_transaction_date,
                LEAD(t.date) OVER (PARTITION BY t.card ORDER BY t.date) as next_transaction_date
            FROM transaction t
            JOIN credit_card cc ON t.card = cc.card
            JOIN card_holder ch ON cc.id_card_holder = ch.id
            JOIN merchant m ON t.id_merchant = m.id
            JOIN merchant_category mc ON m.id_merchant_category = mc.id
        ),
        rapid_transactions AS (
            SELECT 
                *,
                CASE 
                    WHEN prev_transaction_date IS NOT NULL 
                    THEN EXTRACT(EPOCH FROM (date - prev_transaction_date))/60 
                    ELSE NULL 
                END as minutes_since_prev,
                CASE 
                    WHEN next_transaction_date IS NOT NULL 
                    THEN EXTRACT(EPOCH FROM (next_transaction_date - date))/60 
                    ELSE NULL 
                END as minutes_to_next
            FROM transaction_with_lag
        )
        SELECT *
        FROM rapid_transactions
        WHERE (minutes_since_prev IS NOT NULL AND minutes_since_prev <= {time_window_minutes})
           OR (minutes_to_next IS NOT NULL AND minutes_to_next <= {time_window_minutes})
        ORDER BY card, date;
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            logger.info(f"Found {len(df)} rapid transactions")
            return df
        except Exception as e:
            logger.error(f"Error analyzing rapid transactions: {e}")
            return pd.DataFrame()
    
    def generate_fraud_summary_report(self):
        """
        Generate a comprehensive fraud summary report
        
        Returns:
            dict: Summary statistics and findings
        """
        try:
            # Get basic statistics
            basic_stats_query = """
            SELECT 
                COUNT(*) as total_transactions,
                COUNT(DISTINCT card) as unique_cards,
                COUNT(DISTINCT id_merchant) as unique_merchants,
                AVG(amount) as avg_transaction_amount,
                MIN(amount) as min_amount,
                MAX(amount) as max_amount,
                SUM(amount) as total_volume,
                MIN(date) as date_range_start,
                MAX(date) as date_range_end
            FROM transaction;
            """
            
            basic_stats = pd.read_sql_query(basic_stats_query, self.engine).iloc[0]
            
            # Get fraud indicators
            small_transactions = self.count_small_transactions_per_cardholder()
            outliers = self.detect_outlier_transactions()
            early_morning = self.get_top_100_early_morning_transactions()
            vulnerable_merchants = self.identify_top_5_vulnerable_merchants()
            
            summary = {
                'basic_statistics': {
                    'total_transactions': int(basic_stats['total_transactions']),
                    'unique_cards': int(basic_stats['unique_cards']),
                    'unique_merchants': int(basic_stats['unique_merchants']),
                    'avg_transaction_amount': float(basic_stats['avg_transaction_amount']),
                    'min_amount': float(basic_stats['min_amount']),
                    'max_amount': float(basic_stats['max_amount']),
                    'total_volume': float(basic_stats['total_volume']),
                    'date_range': f"{basic_stats['date_range_start']} to {basic_stats['date_range_end']}"
                },
                'fraud_indicators': {
                    'cards_with_small_transactions': len(small_transactions),
                    'total_small_transactions': int(small_transactions['small_transaction_count'].sum()) if len(small_transactions) > 0 else 0,
                    'outlier_transactions': len(outliers),
                    'suspicious_early_morning_transactions': len(early_morning),
                    'vulnerable_merchants': len(vulnerable_merchants)
                },
                'risk_assessment': {
                    'high_risk_cards': len(small_transactions[small_transactions['small_transaction_count'] >= 10]) if len(small_transactions) > 0 else 0,
                    'extreme_outliers': len(outliers[outliers['z_score'] > 5]) if len(outliers) > 0 else 0,
                    'early_morning_high_value': len(early_morning[early_morning['amount'] > 100]) if len(early_morning) > 0 else 0
                }
            }
            
            logger.info("Generated comprehensive fraud summary report")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary report: {e}")
            return {}
