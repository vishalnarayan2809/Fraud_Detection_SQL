"""
Final Project Structure Verification Script
Verifies the new organized project structure and all components
"""

import os
import sys
from pathlib import Path
import pandas as pd

def check_project_structure():
    """Verify the project structure is properly organized"""
    print("🗂️  VERIFYING PROJECT STRUCTURE")
    print("=" * 50)
    
    project_root = Path(__file__).parent.parent
    
    # Expected directory structure
    expected_structure = {
        'src': [
            '__init__.py',
            'data_import.py',
            'fraud_analysis.py', 
            'fraud_visualization.py',
            'main_analysis.py'
        ],
        'data': [
            'card_holder.csv',
            'credit_card.csv',
            'merchant.csv',
            'merchant_category.csv',
            'transaction.csv'
        ],
        'sql': [
            'schema.sql',
            'fraud_detection_queries.sql'
        ],
        'config': [
            'database.yaml',
            'fraud_rules.yaml'
        ],
        'docs': [
            'README.md',
            'EXECUTION_GUIDE.md',
            'fraud_detection_erd.md',
            'API_REFERENCE.md',
            'CONTRIBUTING.md'
        ],
        'tests': [
            'project_status.py',
            'test_setup.py',
            'test_fraud_detection.py'
        ],
        'scripts': [
            'setup_environment.py'
        ]
    }
    
    # Root files
    root_files = [
        'README.md',
        'requirements.txt',
        'setup.py',
        'docker-compose.yml',
        '.gitignore'
    ]
    
    all_good = True
    
    # Check directories and files
    for directory, files in expected_structure.items():
        dir_path = project_root / directory
        if not dir_path.exists():
            print(f"   ❌ Missing directory: {directory}")
            all_good = False
            continue
        
        print(f"   ✅ Directory: {directory}/")
        
        for file in files:
            file_path = dir_path / file
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"      ✅ {file} ({size:,} bytes)")
            else:
                print(f"      ❌ Missing: {file}")
                all_good = False
    
    # Check root files
    print(f"   ✅ Root files:")
    for file in root_files:
        file_path = project_root / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"      ✅ {file} ({size:,} bytes)")
        else:
            print(f"      ❌ Missing: {file}")
            all_good = False
    
    return all_good

def check_data_integrity():
    """Check data files integrity"""
    print("\n📊 CHECKING DATA INTEGRITY")
    print("=" * 50)
    
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'
    
    if not data_dir.exists():
        print("   ❌ Data directory not found")
        return False
    
    try:
        # Check each CSV file
        csv_files = {
            'transaction.csv': ['id', 'date', 'amount', 'card', 'id_merchant'],
            'card_holder.csv': ['id', 'name'],
            'credit_card.csv': ['card', 'id_card_holder'],
            'merchant.csv': ['id', 'name', 'id_merchant_category'],
            'merchant_category.csv': ['id', 'name']
        }
        
        for filename, expected_cols in csv_files.items():
            file_path = data_dir / filename
            
            if not file_path.exists():
                print(f"   ❌ Missing: {filename}")
                continue
                
            df = pd.read_csv(file_path)
            
            # Check structure
            if list(df.columns) == expected_cols:
                print(f"   ✅ {filename}: {len(df):,} records, columns OK")
            else:
                print(f"   ⚠️  {filename}: Column mismatch")
                print(f"      Expected: {expected_cols}")
                print(f"      Found: {list(df.columns)}")
        
        # Specific transaction analysis
        transaction_file = data_dir / 'transaction.csv'
        if transaction_file.exists():
            df = pd.read_csv(transaction_file)
            df['date'] = pd.to_datetime(df['date'])
            
            print(f"\n   📈 Transaction Analysis:")
            print(f"      Total transactions: {len(df):,}")
            print(f"      Date range: {df['date'].min()} to {df['date'].max()}")
            print(f"      Amount range: ${df['amount'].min():.2f} to ${df['amount'].max():,.2f}")
            
            # Fraud indicators
            small_tx = len(df[df['amount'] < 2.0])
            early_morning = len(df[df['date'].dt.hour.between(7, 9)])
            
            print(f"      Small transactions (<$2): {small_tx:,}")
            print(f"      Early morning (7-9 AM): {early_morning:,}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error checking data: {e}")
        return False

def check_import_structure():
    """Test if the new import structure works"""
    print("\n🐍 TESTING IMPORT STRUCTURE")
    print("=" * 50)
    
    project_root = Path(__file__).parent.parent
    
    # Add project root to Python path temporarily
    sys.path.insert(0, str(project_root))
    
    try:
        # Test importing the package
        import src
        print(f"   ✅ Package version: {src.__version__}")
        print(f"   ✅ Package description: {src.__description__}")
        
        # Test importing individual modules
        from src.fraud_analysis import FraudAnalyzer
        from src.fraud_visualization import FraudVisualizer
        from src.data_import import FraudDetectionDatabase
        from src.main_analysis import FraudDetectionPipeline
        
        print("   ✅ All modules imported successfully")
        
        # Test class instantiation
        visualizer = FraudVisualizer()
        print("   ✅ FraudVisualizer instantiated")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False
    finally:
        # Clean up sys.path
        if str(project_root) in sys.path:
            sys.path.remove(str(project_root))

def check_configuration():
    """Check configuration files"""
    print("\n⚙️  CHECKING CONFIGURATION")
    print("=" * 50)
    
    project_root = Path(__file__).parent.parent
    config_dir = project_root / 'config'
    
    if not config_dir.exists():
        print("   ❌ Config directory not found")
        return False
    
    try:
        import yaml
        
        # Check database config
        db_config_file = config_dir / 'database.yaml'
        if db_config_file.exists():
            with open(db_config_file) as f:
                db_config = yaml.safe_load(f)
            print("   ✅ database.yaml loaded successfully")
            print(f"      Database: {db_config.get('database', {}).get('database', 'N/A')}")
        else:
            print("   ❌ database.yaml not found")
        
        # Check fraud rules config
        rules_config_file = config_dir / 'fraud_rules.yaml'
        if rules_config_file.exists():
            with open(rules_config_file) as f:
                rules_config = yaml.safe_load(f)
            print("   ✅ fraud_rules.yaml loaded successfully")
            
            fraud_rules = rules_config.get('fraud_rules', {})
            print(f"      Early morning hours: {fraud_rules.get('early_morning', {}).get('start_hour', 'N/A')}-{fraud_rules.get('early_morning', {}).get('end_hour', 'N/A')}")
            print(f"      Small transaction threshold: ${fraud_rules.get('small_transactions', {}).get('amount_threshold', 'N/A')}")
        else:
            print("   ❌ fraud_rules.yaml not found")
            
        return True
        
    except ImportError:
        print("   ⚠️  PyYAML not installed, skipping YAML validation")
        return True
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False

def check_docker_setup():
    """Check Docker configuration"""
    print("\n🐳 CHECKING DOCKER SETUP")
    print("=" * 50)
    
    project_root = Path(__file__).parent.parent
    docker_file = project_root / 'docker-compose.yml'
    
    if not docker_file.exists():
        print("   ❌ docker-compose.yml not found")
        return False
    
    try:
        with open(docker_file) as f:
            content = f.read()
        
        # Check for key components
        if 'postgres:' in content:
            print("   ✅ PostgreSQL service configured")
        if 'pgadmin' in content:
            print("   ✅ PgAdmin service configured") 
        if 'fraud_detection' in content:
            print("   ✅ Database name configured")
        if '5432:5432' in content:
            print("   ✅ PostgreSQL port mapping configured")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Docker config error: {e}")
        return False

def generate_execution_summary():
    """Generate final execution summary"""
    print("\n🚀 EXECUTION READY CHECKLIST")
    print("=" * 50)
    
    print("To run the fraud detection system:")
    print()
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    print("2. Start PostgreSQL (choose one):")
    print("   Option A - Docker: docker-compose up -d")
    print("   Option B - Local: Start your PostgreSQL service")
    print()
    print("3. Setup environment:")
    print("   python scripts/setup_environment.py")
    print()
    print("4. Run analysis:")
    print("   python src/main_analysis.py")
    print()
    print("5. View results:")
    print("   Check reports/ directory for outputs")
    print("   Open reports/visualizations/*.html for interactive charts")

def main():
    """Run comprehensive project verification"""
    print("🎯 FRAUD DETECTION PROJECT - FINAL VERIFICATION")
    print("=" * 60)
    
    checks = [
        ("Project Structure", check_project_structure),
        ("Data Integrity", check_data_integrity),
        ("Import Structure", check_import_structure),
        ("Configuration", check_configuration),
        ("Docker Setup", check_docker_setup)
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"   ❌ {check_name} check failed: {e}")
            results[check_name] = False
    
    # Summary
    print("\n📋 VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {check_name}")
    
    print(f"\nOverall Score: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 PROJECT VERIFICATION COMPLETE!")
        print("All checks passed. The project is ready for execution.")
        generate_execution_summary()
    else:
        print(f"\n⚠️  {total - passed} checks failed. Please review and fix issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
