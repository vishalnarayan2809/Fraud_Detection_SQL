# Fraud Detection with SQL

A comprehensive fraud detection system that analyzes credit card transactions using SQL, PostgreSQL, Python, and data visualization techniques.

## Overview

This project implements a complete fraud detection pipeline that:
- Creates a normalized database schema for credit card transaction data
- Imports and validates data from CSV files
- Performs sophisticated fraud detection analysis using SQL
- Generates interactive visualizations and comprehensive reports
- Identifies potentially fraudulent patterns using statistical methods

## Features

### Database Schema
- **Card Holders**: Customer information
- **Credit Cards**: Card details linked to cardholders
- **Merchants**: Business information with categorization
- **Merchant Categories**: Business type classifications
- **Transactions**: Complete transaction records with relationships

### Fraud Detection Capabilities
1. **Early Morning Suspicious Transactions**: Identifies high-value transactions between 7-9 AM
2. **Small Transaction Analysis**: Detects potential card testing fraud (<$2 transactions)
3. **Merchant Vulnerability Assessment**: Identifies merchants prone to fraud
4. **Statistical Outlier Detection**: Uses IQR and Z-score methods
5. **Rapid Transaction Analysis**: Detects suspicious velocity patterns
6. **Comprehensive Risk Assessment**: Multi-dimensional fraud scoring

### Visualizations
- Transaction amount distributions
- Hourly transaction patterns
- Merchant vulnerability analysis
- Cardholder risk assessment
- Outlier transaction plots
- Interactive dashboards

## Project Structure

```
Fraud Detection/
├── card_holder.csv              # Cardholder data
├── credit_card.csv              # Credit card data
├── merchant.csv                 # Merchant data
├── merchant_category.csv        # Merchant categories
├── transaction.csv              # Transaction data
├── schema.sql                   # Database schema and views
├── data_import.py              # Data import and setup module
├── fraud_analysis.py           # Fraud detection analysis module
├── fraud_visualization.py      # Visualization module
├── main_analysis.py            # Main orchestration script
├── fraud_detection_queries.sql # Standalone SQL queries
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── reports/                    # Generated reports and visualizations
    ├── fraud_detection_report.json
    ├── *.csv                   # Individual analysis results
    └── *.html                  # Interactive visualizations
```

## Prerequisites

### Software Requirements
- PostgreSQL 12 or higher
- Python 3.8 or higher
- pip (Python package manager)

### Python Libraries
Install required packages using:
```bash
pip install -r requirements.txt
```

Required packages:
- pandas (data manipulation)
- sqlalchemy (database connectivity)
- psycopg2-binary (PostgreSQL adapter)
- plotly (interactive visualizations)
- numpy (numerical computations)

## Setup Instructions

### 1. Database Setup
1. Install PostgreSQL and create a new database:
   ```sql
   CREATE DATABASE fraud_detection;
   ```

2. Update database credentials in `data_import.py` and `main_analysis.py`:
   ```python
   db_config = {
       'host': 'localhost',
       'port': '5432',
       'database': 'fraud_detection',
       'user': 'your_username',
       'password': 'your_password'
   }
   ```

### 2. Data Import
Run the complete analysis pipeline:
```bash
python main_analysis.py
```

Or run individual components:
```bash
# Import data only
python data_import.py

# Run analysis only (after data import)
python -c "from main_analysis import FraudDetectionPipeline; pipeline = FraudDetectionPipeline(db_config); pipeline.run_fraud_analysis()"
```

### 3. Manual SQL Analysis
You can also run individual SQL queries directly in PostgreSQL:
```bash
psql -d fraud_detection -f fraud_detection_queries.sql
```

## Key Fraud Detection Queries

### 1. Early Morning High-Value Transactions
```sql
SELECT t.id, t.date, t.amount, ch.name as cardholder_name
FROM transaction t
JOIN credit_card cc ON t.card = cc.card
JOIN card_holder ch ON cc.id_card_holder = ch.id
WHERE EXTRACT(HOUR FROM t.date) BETWEEN 7 AND 9
ORDER BY t.amount DESC
LIMIT 100;
```

### 2. Small Transaction Analysis
```sql
SELECT t.card, ch.name, COUNT(*) as small_transaction_count
FROM transaction t
JOIN credit_card cc ON t.card = cc.card
JOIN card_holder ch ON cc.id_card_holder = ch.id
WHERE t.amount < 2.00
GROUP BY t.card, ch.name
ORDER BY small_transaction_count DESC;
```

### 3. Statistical Outlier Detection
Uses both IQR (Interquartile Range) and Z-score methods to identify anomalous transactions.

## Output and Reports

### Generated Files
- **fraud_detection_report.json**: Comprehensive analysis summary
- **Individual CSV files**: Detailed results for each analysis
- **Interactive HTML visualizations**: Plotly-based charts and dashboards
- **fraud_detection.log**: Execution logs

### Key Metrics Tracked
- Total transactions analyzed
- Number of potentially fraudulent patterns
- Risk assessment scores
- Merchant vulnerability rankings
- Cardholder risk profiles

## Fraud Detection Techniques

### 1. Temporal Analysis
- **Early Morning Transactions**: Flags high-value transactions during off-hours
- **Rapid Transactions**: Identifies suspicious velocity patterns
- **Hourly Patterns**: Analyzes transaction distribution across time

### 2. Statistical Methods
- **Z-Score Analysis**: Identifies transactions beyond 3 standard deviations
- **Interquartile Range (IQR)**: Detects outliers using quartile-based methods
- **Pattern Recognition**: Analyzes spending behavior patterns

### 3. Behavioral Analysis
- **Small Transaction Testing**: Detects card validation attempts
- **Merchant Vulnerability**: Identifies high-risk merchant locations
- **Spending Pattern Analysis**: Tracks unusual cardholder behavior

## Risk Assessment Framework

### Risk Levels
- **Low Risk**: Normal transaction patterns
- **Medium Risk**: Minor anomalies requiring monitoring
- **High Risk**: Multiple fraud indicators present
- **Critical Risk**: Extreme outliers or rapid fraud patterns

### Indicators
- Number of small transactions
- Statistical outlier scores
- Temporal anomalies
- Merchant risk factors
- Transaction velocity

## Best Practices and Recommendations

### Immediate Actions
1. Monitor transactions flagged as extreme outliers (Z-score > 5)
2. Review cards with >10 small transactions in 24 hours
3. Investigate early morning high-value transactions
4. Enhanced monitoring for vulnerable merchants

### Ongoing Monitoring
1. Regular pattern analysis updates
2. Threshold adjustment based on false positive rates
3. Merchant risk assessment reviews
4. Customer communication for high-risk activities

## Visualization Features

### Interactive Dashboards
- Real-time fraud metrics
- Drill-down capabilities
- Interactive filtering
- Export functionality

### Chart Types
- Distribution histograms
- Time series analysis
- Scatter plots for outlier detection
- Bar charts for categorical analysis
- Heat maps for pattern recognition

## Database Views

The system creates several PostgreSQL views for easy querying:
- `early_morning_high_transactions`
- `small_transactions`
- `merchant_small_transaction_analysis`
- `hourly_transaction_patterns`
- `cardholder_transaction_summary`
- `outlier_transactions`

## Troubleshooting

### Common Issues
1. **Database Connection**: Verify PostgreSQL is running and credentials are correct
2. **Missing Dependencies**: Run `pip install -r requirements.txt`
3. **Data Import Errors**: Check CSV file formats and paths
4. **Memory Issues**: For large datasets, consider processing in chunks

### Performance Optimization
- Database indexes are automatically created for key columns
- Views are optimized for common queries
- Large result sets are limited in reports
- Batch processing for data imports

## Contributing

To extend the fraud detection capabilities:
1. Add new analysis methods in `fraud_analysis.py`
2. Create corresponding visualizations in `fraud_visualization.py`
3. Update SQL queries in `fraud_detection_queries.sql`
4. Test with sample data and validate results

## License

This project is for educational and research purposes. Please ensure compliance with data privacy regulations when working with real financial data.

## Future Enhancements

### Planned Features
- Machine learning integration
- Real-time streaming analysis
- API endpoints for external systems
- Advanced behavioral modeling
- Geographic analysis capabilities
- Network analysis for connected fraud patterns

### Technical Improvements
- Docker containerization
- Automated testing suite
- Configuration management
- Enhanced error handling
- Performance monitoring
- Scalability improvements

## Contact and Support

For questions, issues, or contributions, please refer to the project documentation or create an issue in the repository.
