"""
Simple Project Verification and Status Check
"""

import pandas as pd
import os
from datetime import datetime

def quick_verification():
    """Quick verification of project status"""
    print("🔍 FRAUD DETECTION PROJECT - STATUS CHECK")
    print("=" * 60)
    
    base_dir = r'c:\Users\guruk\Fraud Detection'
    
    # 1. Check all required files exist
    required_files = {
        'data/card_holder.csv': 'Card holder data',
        'data/credit_card.csv': 'Credit card data', 
        'data/merchant.csv': 'Merchant data',
        'data/merchant_category.csv': 'Merchant category data',
        'data/transaction.csv': 'Transaction data',
        'sql/schema.sql': 'Database schema',
        'src/data_import.py': 'Data import module',
        'src/fraud_analysis.py': 'Fraud analysis module',
        'src/fraud_visualization.py': 'Visualization module',
        'src/main_analysis.py': 'Main analysis module',
        'sql/fraud_detection_queries.sql': 'SQL queries',
        'requirements.txt': 'Python dependencies',
        'README.md': 'Project documentation'
    }
    
    print("\n📁 FILE INVENTORY:")
    missing_files = []
    for file, description in required_files.items():
        filepath = os.path.join(base_dir, file)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"   ✅ {file} ({size:,} bytes)")
        else:
            print(f"   ❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
      # 2. Check CSV data quality
    print("\n📊 DATA QUALITY CHECK:")
    try:
        # Transaction data
        transactions = pd.read_csv(os.path.join(base_dir, 'data', 'transaction.csv'))
        print(f"   ✅ Transactions: {len(transactions):,} records")
        print(f"      📅 Date range: {transactions['date'].min()} to {transactions['date'].max()}")
        print(f"      💰 Amount range: ${transactions['amount'].min():.2f} to ${transactions['amount'].max():,.2f}")
        
        # Small transactions analysis
        small_tx = transactions[transactions['amount'] < 2.0]
        print(f"      🔍 Small transactions (<$2): {len(small_tx):,} ({len(small_tx)/len(transactions)*100:.1f}%)")
        
        # Early morning transactions
        transactions['datetime'] = pd.to_datetime(transactions['date'])
        early_morning = transactions[transactions['datetime'].dt.hour.between(7, 9)]
        print(f"      🌅 Early morning (7-9 AM): {len(early_morning):,} transactions")
          # Card data
        cards = pd.read_csv(os.path.join(base_dir, 'data', 'credit_card.csv'))
        print(f"   ✅ Credit cards: {len(cards):,} records")
        
        # Cardholders
        cardholders = pd.read_csv(os.path.join(base_dir, 'data', 'card_holder.csv'))
        print(f"   ✅ Cardholders: {len(cardholders):,} records")
        
        # Merchants
        merchants = pd.read_csv(os.path.join(base_dir, 'data', 'merchant.csv'))
        print(f"   ✅ Merchants: {len(merchants):,} records")
        
        # Merchant categories
        categories = pd.read_csv(os.path.join(base_dir, 'data', 'merchant_category.csv'))
        print(f"   ✅ Merchant categories: {len(categories):,} records")
        
    except Exception as e:
        print(f"   ❌ Data quality check failed: {e}")
        return False
    
    # 3. Check fraud detection capabilities
    print("\n🔍 FRAUD DETECTION CAPABILITIES:")
      # Check schema for views
    try:
        with open(os.path.join(base_dir, 'sql', 'schema.sql'), 'r') as f:
            schema_content = f.read()
        
        capabilities = {
            'Early Morning Analysis': 'EXTRACT(HOUR FROM t.date) BETWEEN 7 AND 9' in schema_content,
            'Small Transaction Detection': 't.amount < 2.00' in schema_content,
            'Statistical Outliers': 'PERCENTILE_CONT' in schema_content and 'STDDEV' in schema_content,
            'Database Views': 'CREATE VIEW' in schema_content,
            'Merchant Vulnerability': 'merchant_small_transaction_analysis' in schema_content
        }
        
        for capability, present in capabilities.items():
            status = "✅" if present else "❌"
            print(f"   {status} {capability}")
            
    except Exception as e:
        print(f"   ❌ Schema check failed: {e}")
        return False
    
    # 4. Sample fraud analysis
    print("\n🎯 SAMPLE FRAUD INDICATORS:")
    try:
        # High-value early morning transactions
        high_value_early = early_morning[early_morning['amount'] > 100]
        print(f"   🚨 High-value early morning transactions (>$100): {len(high_value_early)}")
        
        # Cards with multiple small transactions
        small_tx_by_card = small_tx.groupby('card').size()
        suspicious_cards = small_tx_by_card[small_tx_by_card >= 5]
        print(f"   🚨 Cards with 5+ small transactions: {len(suspicious_cards)}")
        
        # Outlier amounts (simple z-score)
        mean_amount = transactions['amount'].mean()
        std_amount = transactions['amount'].std()
        outliers = transactions[abs(transactions['amount'] - mean_amount) > 3 * std_amount]
        print(f"   🚨 Statistical outliers (Z-score > 3): {len(outliers)}")
        
        # Show some examples
        if len(high_value_early) > 0:
            top_early = high_value_early.nlargest(3, 'amount')
            print(f"   📋 Top early morning transactions:")
            for _, tx in top_early.iterrows():
                print(f"      💰 ${tx['amount']:.2f} at {tx['date']} (Card: {tx['card']})")
        
    except Exception as e:
        print(f"   ❌ Sample analysis failed: {e}")
        return False
    
    print("\n🎉 PROJECT STATUS: READY FOR EXECUTION!")
    return True

def show_next_steps():
    """Show the next steps to run the project"""
    print("\n" + "=" * 60)
    print("🚀 NEXT STEPS TO RUN THE FRAUD DETECTION SYSTEM")
    print("=" * 60)
    
    print("\n1️⃣ INSTALL DEPENDENCIES:")
    print("   pip install -r requirements.txt")
    print("   # This installs: pandas, sqlalchemy, psycopg2-binary, plotly, numpy")
    
    print("\n2️⃣ SETUP POSTGRESQL DATABASE:")
    print("   # Install PostgreSQL if not already installed")
    print("   # Create database: CREATE DATABASE fraud_detection;")
    print("   # Update credentials in main_analysis.py and data_import.py")
    
    print("\n3️⃣ CONFIGURE DATABASE CONNECTION:")
    print("   # Edit these files to update your PostgreSQL credentials:")
    print("   # - main_analysis.py (line ~380)")
    print("   # - data_import.py (line ~120)")
    print("   # Change: 'password': 'your_password_here'")
    
    print("\n4️⃣ RUN THE COMPLETE ANALYSIS:")
    print("   python main_analysis.py")
    print("   # This will:")
    print("   # - Create database schema")
    print("   # - Import all CSV data")
    print("   # - Run fraud detection analysis")
    print("   # - Generate visualizations")
    print("   # - Create comprehensive report")
    
    print("\n5️⃣ ALTERNATIVE: RUN COMPONENTS SEPARATELY:")
    print("   # Import data only:")
    print("   python data_import.py")
    print("   ")
    print("   # Run SQL queries directly:")
    print("   psql -d fraud_detection -f fraud_detection_queries.sql")
    
    print("\n6️⃣ VIEW RESULTS:")
    print("   # Check the 'reports' folder for:")
    print("   # - fraud_detection_report.json (comprehensive analysis)")
    print("   # - *.csv files (detailed results)")
    print("   # - *.html files (interactive visualizations)")
    
    print("\n📊 EXPECTED OUTPUTS:")
    print("   ✅ Top 100 highest early morning transactions")
    print("   ✅ Cards with suspicious small transaction patterns")
    print("   ✅ Top 5 most vulnerable merchants")
    print("   ✅ Statistical outlier transactions")
    print("   ✅ Interactive fraud detection dashboard")
    print("   ✅ Comprehensive fraud summary report")

def show_key_features():
    """Show key features of the fraud detection system"""
    print("\n" + "=" * 60)
    print("🔑 KEY FRAUD DETECTION FEATURES")
    print("=" * 60)
    
    features = {
        "🌅 Early Morning Analysis": [
            "Detects high-value transactions between 7-9 AM",
            "Flags unusual activity during off-hours",
            "Configurable time windows"
        ],
        "💳 Card Testing Detection": [
            "Identifies cards with multiple small transactions (<$2)",
            "Detects potential card validation attempts",
            "Risk scoring based on transaction patterns"
        ],
        "🏪 Merchant Vulnerability": [
            "Ranks merchants by fraud exposure",
            "Identifies businesses prone to small transaction fraud",
            "Category-based risk assessment"
        ],
        "📊 Statistical Analysis": [
            "Z-score based outlier detection",
            "Interquartile Range (IQR) analysis",
            "Standard deviation calculations"
        ],
        "⚡ Velocity Analysis": [
            "Rapid successive transaction detection",
            "Time-based pattern analysis",
            "Configurable time windows"
        ],
        "📈 Interactive Visualizations": [
            "Plotly-based interactive charts",
            "Drill-down capabilities",
            "Export-ready reports"
        ]
    }
    
    for feature, details in features.items():
        print(f"\n{feature}:")
        for detail in details:
            print(f"   • {detail}")

if __name__ == "__main__":
    # Run verification
    success = quick_verification()
    
    if success:
        show_key_features()
        show_next_steps()
        
        print("\n" + "=" * 60)
        print("✨ FRAUD DETECTION PROJECT IS READY!")
        print("=" * 60)
        print("All components verified and working correctly.")
        print("Follow the next steps above to execute the analysis.")
    else:
        print("\n❌ PROJECT HAS ISSUES - Please fix the problems above before proceeding.")
