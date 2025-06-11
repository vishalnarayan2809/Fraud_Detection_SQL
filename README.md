# Fraud Detection with SQL

A comprehensive fraud detection system that analyzes credit card transactions using SQL, PostgreSQL, Python, and data visualization techniques.



## 🗂️ Project Structure


```
fraud-detection/
├── 📁 src/                          # Source code
│   ├── data_import.py               # Database setup and data import
│   ├── fraud_analysis.py            # Core fraud detection algorithms
│   ├── fraud_visualization.py       # Interactive visualizations
│   ├── main_analysis.py             # Main orchestration script
│   └── __init__.py                  # Python package initialization
├── 📁 data/                         # Raw data files
│   ├── card_holder.csv              # Cardholder information
│   ├── credit_card.csv              # Credit card details
│   ├── merchant.csv                 # Merchant information
│   ├── merchant_category.csv        # Business categories
│   └── transaction.csv              # Transaction records
├── 📁 sql/                          # SQL scripts and schema
│   ├── schema.sql                   # Database schema and views
│   ├── fraud_detection_queries.sql  # Standalone fraud detection queries
│   └── sample_queries.sql           # Example queries for testing
├── 📁 config/                       # Configuration files
│   ├── database.yaml                # Database configuration
│   └── fraud_rules.yaml             # Fraud detection rules
├── 📁 docs/                         # Documentation
│   ├── README.md                    # Main project documentation
│   ├── EXECUTION_GUIDE.md           # Step-by-step execution guide
│   ├── fraud_detection_erd.md       # Entity relationship diagram
│   ├── API_REFERENCE.md             # API documentation
│   └── CONTRIBUTING.md              # Contribution guidelines
├── 📁 tests/                        # Test files
│   ├── test_setup.py                # Project setup verification
│   ├── project_status.py            # Project status checker
│   └── test_fraud_detection.py      # Unit tests for fraud detection
├── 📁 scripts/                      # Utility scripts
│   ├── setup_environment.py         # Environment setup script
│   └── generate_sample_data.py      # Sample data generator
├── 📁 reports/                      # Generated reports (created at runtime)
│   ├── fraud_detection_report.json  # Comprehensive analysis report
│   ├── visualizations/              # Interactive HTML charts
│   └── csv_exports/                 # Detailed CSV results
├── requirements.txt                 # Python dependencies
├── setup.py                        # Package setup configuration
├── .gitignore                      # Git ignore rules
└── docker-compose.yml              # Docker setup for PostgreSQL
```

ERD
![Fraud_detection](https://github.com/user-attachments/assets/a4f100ec-03e7-4202-bf3d-5f7eb2cd29cd)


## 🚀 Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd fraud-detection
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```bash
   docker-compose up -d  # Start PostgreSQL
   python scripts/setup_environment.py
   ```

3. **Run Analysis**
   ```bash
   python src/main_analysis.py
   ```

4. **View Reports**
   ```bash
   # Reports will be generated in reports/ directory
   open reports/visualizations/dashboard.html
   ```

## 📊 Features

- **Comprehensive Fraud Detection**: Multiple algorithms for detecting fraudulent transactions
- **Interactive Visualizations**: Plotly-based dashboards and charts
- **Statistical Analysis**: Z-score, IQR, and pattern-based detection
- **Professional Structure**: Well-organized, maintainable codebase
- **Docker Support**: Easy PostgreSQL setup with Docker
- **Extensive Documentation**: Complete guides and API reference

## 🔧 Configuration

Edit `config/database.yaml` and `config/fraud_rules.yaml` to customize the system for your environment.

## 📈 Data Flow

1. **Data Import** (`src/data_import.py`) → Load CSV data into PostgreSQL
2. **Analysis** (`src/fraud_analysis.py`) → Run fraud detection algorithms
3. **Visualization** (`src/fraud_visualization.py`) → Generate interactive charts
4. **Reporting** (`reports/`) → Export results and summaries

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Check project status
python tests/project_status.py
```

## 📚 Documentation

- [Execution Guide](docs/EXECUTION_GUIDE.md) - Step-by-step instructions
- [ERD Diagram](docs/fraud_detection_erd.md) - Database structure
- [API Reference](docs/API_REFERENCE.md) - Code documentation
- [Contributing](docs/CONTRIBUTING.md) - Development guidelines

## 🐳 Docker Support

Use Docker Compose for easy PostgreSQL setup:
```bash
docker-compose up -d
```

## 📝 License

This project is for educational and research purposes. Please ensure compliance with data privacy regulations when working with real financial data.

---

**Built with ❤️ for fraud detection and data analysis education**
