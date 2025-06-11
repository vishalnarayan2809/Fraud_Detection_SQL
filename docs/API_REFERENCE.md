# API Reference - Fraud Detection System

## Overview

This document provides comprehensive API documentation for the Fraud Detection System modules.

## Core Classes

### FraudDetectionDatabase (`src/data_import.py`)

Handles database connection, schema creation, and data import.

#### Constructor
```python
FraudDetectionDatabase(db_config: dict)
```

**Parameters:**
- `db_config`: Dictionary containing database connection parameters
  - `host`: Database host (default: 'localhost')
  - `port`: Database port (default: '5432')
  - `database`: Database name
  - `user`: Database username
  - `password`: Database password

#### Methods

##### `create_connection() -> bool`
Establishes connection to PostgreSQL database.

**Returns:** `True` if successful, `False` otherwise

##### `execute_schema(schema_file: str) -> bool`
Executes SQL schema file to create tables and views.

**Parameters:**
- `schema_file`: Path to SQL schema file

**Returns:** `True` if successful, `False` otherwise

##### `load_csv_data(data_directory: str) -> bool`
Loads all CSV files into database tables.

**Parameters:**
- `data_directory`: Path to directory containing CSV files

**Returns:** `True` if successful, `False` otherwise

##### `validate_data_integrity() -> bool`
Validates data relationships and integrity.

**Returns:** `True` if validation passes, `False` otherwise

---

### FraudAnalyzer (`src/fraud_analysis.py`)

Core fraud detection analysis engine.

#### Constructor
```python
FraudAnalyzer(engine: sqlalchemy.Engine)
```

**Parameters:**
- `engine`: SQLAlchemy database engine

#### Methods

##### `get_top_100_early_morning_transactions() -> pd.DataFrame`
Identifies top 100 highest transactions between 7-9 AM.

**Returns:** DataFrame with columns:
- `id`: Transaction ID
- `date`: Transaction timestamp
- `amount`: Transaction amount
- `card`: Credit card number
- `cardholder_name`: Name of cardholder
- `merchant_name`: Merchant name
- `merchant_category`: Business category

##### `count_small_transactions_per_cardholder() -> pd.DataFrame`
Analyzes small transactions (<$2) per cardholder for card testing detection.

**Returns:** DataFrame with columns:
- `card`: Credit card number
- `cardholder_name`: Name of cardholder
- `small_transaction_count`: Number of small transactions
- `avg_small_amount`: Average amount of small transactions
- `min_amount`: Minimum transaction amount
- `max_amount`: Maximum transaction amount

##### `identify_top_5_vulnerable_merchants() -> pd.DataFrame`
Identifies merchants most prone to small transaction fraud.

**Returns:** DataFrame with top 5 vulnerable merchants and their statistics

##### `detect_outlier_transactions() -> pd.DataFrame`
Detects statistical outliers using IQR and Z-score methods.

**Returns:** DataFrame with outlier transactions and their statistical measures

##### `analyze_rapid_transactions(time_window_minutes: int = 5, min_transaction_count: int = 3) -> pd.DataFrame`
Detects rapid successive transactions indicating potential fraud.

**Parameters:**
- `time_window_minutes`: Time window for detecting rapid transactions
- `min_transaction_count`: Minimum transactions in window to flag

**Returns:** DataFrame with rapid transaction patterns

##### `generate_fraud_summary_report() -> dict`
Generates comprehensive fraud detection summary.

**Returns:** Dictionary containing:
- `basic_statistics`: Overall transaction statistics
- `fraud_indicators`: Count of various fraud indicators
- `risk_assessment`: Risk level assessments

---

### FraudVisualizer (`src/fraud_visualization.py`)

Creates interactive visualizations for fraud analysis.

#### Constructor
```python
FraudVisualizer()
```

#### Methods

##### `plot_transaction_amount_distribution(transactions_df: pd.DataFrame) -> plotly.graph_objects.Figure`
Creates histogram of transaction amounts.

**Parameters:**
- `transactions_df`: DataFrame containing transaction data

**Returns:** Plotly figure object

##### `plot_hourly_transaction_patterns(hourly_data: pd.DataFrame) -> plotly.graph_objects.Figure`
Visualizes transaction patterns by hour of day.

**Parameters:**
- `hourly_data`: DataFrame with hourly aggregated data

**Returns:** Plotly figure with subplots for count and amount patterns

##### `plot_merchant_vulnerability_analysis(vulnerable_merchants: pd.DataFrame) -> plotly.graph_objects.Figure`
Creates bar chart of merchant vulnerability to fraud.

**Parameters:**
- `vulnerable_merchants`: DataFrame with merchant vulnerability data

**Returns:** Plotly bar chart figure

##### `plot_cardholder_risk_analysis(small_transactions_df: pd.DataFrame) -> plotly.graph_objects.Figure`
Scatter plot analysis of cardholder risk levels.

**Parameters:**
- `small_transactions_df`: DataFrame with small transaction patterns

**Returns:** Plotly scatter plot with risk categorization

##### `create_fraud_summary_dashboard(summary_data: dict, transactions_df: pd.DataFrame, **kwargs) -> dict`
Creates comprehensive dashboard with multiple visualizations.

**Parameters:**
- `summary_data`: Summary statistics dictionary
- `transactions_df`: Complete transaction dataset
- Additional DataFrames for specific analyses

**Returns:** Dictionary of plotly figures

##### `save_plots_to_html(plots_dict: dict, output_dir: str = "reports/visualizations") -> None`
Saves all plots to HTML files.

**Parameters:**
- `plots_dict`: Dictionary of plotly figures
- `output_dir`: Output directory for HTML files

---

### FraudDetectionPipeline (`src/main_analysis.py`)

Main orchestration class for complete fraud detection pipeline.

#### Constructor
```python
FraudDetectionPipeline(db_config: dict)
```

**Parameters:**
- `db_config`: Database configuration dictionary

#### Methods

##### `setup_database() -> bool`
Sets up database connection, schema, and imports data.

**Returns:** `True` if setup successful, `False` otherwise

##### `run_fraud_analysis() -> dict`
Executes complete fraud detection analysis.

**Returns:** Dictionary containing all analysis results:
- `early_morning_transactions`: Early morning analysis results
- `small_transactions`: Small transaction patterns
- `vulnerable_merchants`: Merchant vulnerability analysis
- `outliers`: Statistical outlier detection
- `summary`: Comprehensive summary report

##### `create_visualizations(analysis_results: dict) -> dict`
Generates all visualizations from analysis results.

**Parameters:**
- `analysis_results`: Results from fraud analysis

**Returns:** Dictionary of plotly figures

##### `generate_report(analysis_results: dict, output_file: str = "fraud_detection_report.json") -> dict`
Creates comprehensive fraud detection report.

**Parameters:**
- `analysis_results`: Analysis results dictionary
- `output_file`: Output filename for JSON report

**Returns:** Complete report dictionary

##### `run_complete_analysis() -> bool`
Executes the complete end-to-end fraud detection pipeline.

**Returns:** `True` if successful, `False` otherwise

---

## Configuration

### Database Configuration (`config/database.yaml`)

```yaml
database:
  host: localhost
  port: 5432
  database: fraud_detection
  user: postgres
  password: ${DB_PASSWORD}
```

### Fraud Rules Configuration (`config/fraud_rules.yaml`)

```yaml
fraud_rules:
  early_morning:
    start_hour: 7
    end_hour: 9
    min_amount_threshold: 50.0
  
  small_transactions:
    amount_threshold: 2.00
    max_count_per_card: 5
  
  outliers:
    z_score_threshold: 3.0
    iqr_multiplier: 1.5
```

---

## Database Schema

### Tables

#### `merchant_category`
- `id` (SERIAL PRIMARY KEY)
- `name` (VARCHAR(50) NOT NULL)

#### `card_holder`
- `id` (SERIAL PRIMARY KEY)
- `name` (VARCHAR(100) NOT NULL)

#### `merchant`
- `id` (SERIAL PRIMARY KEY)
- `name` (VARCHAR(200) NOT NULL)
- `id_merchant_category` (INTEGER, FK)

#### `credit_card`
- `card` (VARCHAR(20) PRIMARY KEY)
- `id_card_holder` (INTEGER, FK)

#### `transaction`
- `id` (SERIAL PRIMARY KEY)
- `date` (TIMESTAMP NOT NULL)
- `amount` (DECIMAL(10,2) NOT NULL)
- `card` (VARCHAR(20), FK)
- `id_merchant` (INTEGER, FK)

### Views

#### `early_morning_high_transactions`
High-value transactions between 7-9 AM

#### `small_transactions`
Cards with multiple small transactions (<$2)

#### `merchant_small_transaction_analysis`
Merchant vulnerability to small transaction fraud

#### `outlier_transactions`
Statistical outliers using IQR and Z-score methods

---

## Usage Examples

### Basic Usage

```python
from src import FraudDetectionPipeline

# Configure database
db_config = {
    'host': 'localhost',
    'port': '5432',
    'database': 'fraud_detection',
    'user': 'postgres',
    'password': 'your_password'
}

# Run complete analysis
pipeline = FraudDetectionPipeline(db_config)
success = pipeline.run_complete_analysis()
```

### Custom Analysis

```python
from src import FraudAnalyzer
from sqlalchemy import create_engine

# Setup
engine = create_engine("postgresql://user:pass@localhost/fraud_detection")
analyzer = FraudAnalyzer(engine)

# Run specific analyses
early_morning = analyzer.get_top_100_early_morning_transactions()
small_tx = analyzer.count_small_transactions_per_cardholder()
outliers = analyzer.detect_outlier_transactions()
```

### Custom Visualizations

```python
from src import FraudVisualizer

visualizer = FraudVisualizer()

# Create specific plots
amount_dist = visualizer.plot_transaction_amount_distribution(transactions)
hourly_patterns = visualizer.plot_hourly_transaction_patterns(hourly_data)

# Save to HTML
plots = {'distribution': amount_dist, 'patterns': hourly_patterns}
visualizer.save_plots_to_html(plots)
```

---

## Error Handling

All methods include comprehensive error handling and logging. Check the logs for detailed error information:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Performance Considerations

- Database indexes are automatically created for optimal query performance
- Large datasets are processed in chunks where appropriate
- Memory usage is optimized for datasets up to 1M transactions
- For larger datasets, consider implementing pagination in queries
