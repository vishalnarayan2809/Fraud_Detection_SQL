"""
Test script to verify fraud detection setup and functionality
"""

import pandas as pd
import os
import re

def test_csv_data_integrity():
    """Test CSV data structure and integrity"""
    print("="*50)
    print("TESTING CSV DATA INTEGRITY")
    print("="*50)
    
    data_dir = r'c:\Users\guruk\Fraud Detection'
    
    # Test each CSV file
    csv_files = {
        'card_holder.csv': ['id', 'name'],
        'credit_card.csv': ['card', 'id_card_holder'],
        'merchant.csv': ['id', 'name', 'id_merchant_category'],
        'merchant_category.csv': ['id', 'name'],
        'transaction.csv': ['id', 'date', 'amount', 'card', 'id_merchant']
    }
    
    results = {}
    
    for filename, expected_columns in csv_files.items():
        filepath = os.path.join(data_dir, filename)
        
        try:
            df = pd.read_csv(filepath)
            results[filename] = {
                'status': 'SUCCESS',
                'rows': len(df),
                'columns': list(df.columns),
                'expected_columns': expected_columns,
                'columns_match': list(df.columns) == expected_columns,
                'sample_data': df.head(3).to_dict('records') if len(df) > 0 else []
            }
            
            # Special checks
            if filename == 'credit_card.csv':
                # Check for scientific notation issues
                card_sample = df['card'].head().astype(str)
                has_scientific = any('E' in str(card) for card in card_sample)
                results[filename]['has_scientific_notation'] = has_scientific
                
                # Convert scientific notation to regular numbers
                df['card_converted'] = df['card'].apply(lambda x: f"{x:.0f}" if pd.notnull(x) else x)
                results[filename]['sample_converted_cards'] = df['card_converted'].head(3).tolist()
            
            if filename == 'transaction.csv':
                # Check date format
                date_sample = df['date'].head(3)
                results[filename]['sample_dates'] = date_sample.tolist()
                
                # Check amount range
                results[filename]['amount_stats'] = {
                    'min': float(df['amount'].min()),
                    'max': float(df['amount'].max()),
                    'mean': float(df['amount'].mean()),
                    'small_transactions_count': len(df[df['amount'] < 2.0])
                }
            
        except Exception as e:
            results[filename] = {
                'status': 'ERROR',
                'error': str(e)
            }
    
    return results

def test_sql_syntax():
    """Test SQL files for basic syntax issues"""
    print("="*50)
    print("TESTING SQL SYNTAX")
    print("="*50)
    
    sql_files = ['schema.sql', 'fraud_detection_queries.sql']
    results = {}
    
    for filename in sql_files:
        filepath = os.path.join(r'c:\Users\guruk\Fraud Detection', filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic syntax checks
            results[filename] = {
                'status': 'SUCCESS',
                'lines': len(content.split('\n')),
                'has_drop_statements': 'DROP TABLE' in content,
                'has_create_statements': 'CREATE TABLE' in content,
                'has_views': 'CREATE VIEW' in content,
                'has_indexes': 'CREATE INDEX' in content,
                'semicolon_count': content.count(';')
            }
            
            # Check for potential issues
            issues = []
            if 'SERIAL PRIMARY KEY' not in content and filename == 'schema.sql':
                issues.append("Missing SERIAL PRIMARY KEY")
            if 'FOREIGN KEY' not in content and filename == 'schema.sql':
                issues.append("Missing FOREIGN KEY constraints")
            
            results[filename]['potential_issues'] = issues
            
        except Exception as e:
            results[filename] = {
                'status': 'ERROR',
                'error': str(e)
            }
    
    return results

def test_python_imports():
    """Test if Python scripts can be imported without major syntax errors"""
    print("="*50)
    print("TESTING PYTHON SCRIPTS")
    print("="*50)
    
    script_files = ['data_import.py', 'fraud_analysis.py', 'fraud_visualization.py', 'main_analysis.py']
    results = {}
    
    for filename in script_files:
        filepath = os.path.join(r'c:\Users\guruk\Fraud Detection', filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic checks
            results[filename] = {
                'status': 'SUCCESS',
                'lines': len(content.split('\n')),
                'has_imports': content.count('import ') > 0,
                'has_classes': 'class ' in content,
                'has_functions': 'def ' in content,
                'has_main': 'if __name__ == "__main__"' in content
            }
            
            # Check for potential issues
            issues = []
            if 'TODO' in content:
                issues.append("Contains TODO items")
            if 'your_password_here' in content:
                issues.append("Contains placeholder password")
            
            results[filename]['potential_issues'] = issues
            
        except Exception as e:
            results[filename] = {
                'status': 'ERROR',
                'error': str(e)
            }
    
    return results

def check_project_completeness():
    """Check if all required project components are present"""
    print("="*50)
    print("CHECKING PROJECT COMPLETENESS")
    print("="*50)
    
    required_components = {
        'CSV Data Files': ['card_holder.csv', 'credit_card.csv', 'merchant.csv', 'merchant_category.csv', 'transaction.csv'],
        'Database Schema': ['schema.sql'],
        'Python Scripts': ['data_import.py', 'fraud_analysis.py', 'fraud_visualization.py', 'main_analysis.py'],
        'SQL Queries': ['fraud_detection_queries.sql'],
        'Documentation': ['README.md', 'requirements.txt']
    }
    
    results = {}
    data_dir = r'c:\Users\guruk\Fraud Detection'
    
    for category, files in required_components.items():
        results[category] = {
            'required': len(files),
            'present': 0,
            'missing': [],
            'found': []
        }
        
        for filename in files:
            filepath = os.path.join(data_dir, filename)
            if os.path.exists(filepath):
                results[category]['present'] += 1
                results[category]['found'].append(filename)
            else:
                results[category]['missing'].append(filename)
    
    return results

def verify_fraud_detection_requirements():
    """Verify specific fraud detection requirements are met"""
    print("="*50)
    print("VERIFYING FRAUD DETECTION REQUIREMENTS")
    print("="*50)
    
    requirements = {
        'Early Morning Transactions (7-9 AM)': False,
        'Small Transactions (<$2) Analysis': False,
        'Top 5 Vulnerable Merchants': False,
        'Database Views Created': False,
        'Statistical Outlier Detection': False,
        'Python Visualization': False,
        'Comprehensive Reporting': False
    }
    
    # Check schema.sql for views
    try:
        with open(r'c:\Users\guruk\Fraud Detection\schema.sql', 'r') as f:
            schema_content = f.read()
        
        if 'EXTRACT(HOUR FROM t.date) BETWEEN 7 AND 9' in schema_content:
            requirements['Early Morning Transactions (7-9 AM)'] = True
        
        if 't.amount < 2.00' in schema_content:
            requirements['Small Transactions (<$2) Analysis'] = True
        
        if 'CREATE VIEW' in schema_content:
            requirements['Database Views Created'] = True
        
        if 'PERCENTILE_CONT' in schema_content and 'STDDEV' in schema_content:
            requirements['Statistical Outlier Detection'] = True
            
    except Exception as e:
        print(f"Error checking schema.sql: {e}")
    
    # Check fraud_detection_queries.sql
    try:
        with open(r'c:\Users\guruk\Fraud Detection\fraud_detection_queries.sql', 'r') as f:
            queries_content = f.read()
        
        if 'TOP 5 MERCHANTS VULNERABLE' in queries_content:
            requirements['Top 5 Vulnerable Merchants'] = True
            
    except Exception as e:
        print(f"Error checking queries file: {e}")
    
    # Check visualization script
    try:
        with open(r'c:\Users\guruk\Fraud Detection\fraud_visualization.py', 'r') as f:
            viz_content = f.read()
        
        if 'plotly' in viz_content and 'FraudVisualizer' in viz_content:
            requirements['Python Visualization'] = True
            
    except Exception as e:
        print(f"Error checking visualization script: {e}")
    
    # Check main analysis script
    try:
        with open(r'c:\Users\guruk\Fraud Detection\main_analysis.py', 'r') as f:
            main_content = f.read()
        
        if 'generate_report' in main_content and 'FraudDetectionPipeline' in main_content:
            requirements['Comprehensive Reporting'] = True
            
    except Exception as e:
        print(f"Error checking main script: {e}")
    
    return requirements

def main():
    """Run all tests and generate a comprehensive report"""
    print("FRAUD DETECTION PROJECT - COMPREHENSIVE TESTING")
    print("="*60)
    
    # Run all tests
    csv_results = test_csv_data_integrity()
    sql_results = test_sql_syntax()
    python_results = test_python_imports()
    completeness_results = check_project_completeness()
    requirements_results = verify_fraud_detection_requirements()
    
    # Print results
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    # CSV Data Results
    print("\n1. CSV DATA INTEGRITY:")
    for filename, result in csv_results.items():
        status = result['status']
        if status == 'SUCCESS':
            rows = result['rows']
            cols_match = result['columns_match']
            print(f"   ✅ {filename}: {rows} rows, columns match: {cols_match}")
            if filename == 'credit_card.csv' and result.get('has_scientific_notation'):
                print(f"      ⚠️  Scientific notation detected - will be converted during import")
        else:
            print(f"   ❌ {filename}: {result['error']}")
    
    # SQL Results
    print("\n2. SQL SYNTAX:")
    for filename, result in sql_results.items():
        status = result['status']
        if status == 'SUCCESS':
            lines = result['lines']
            views = result['has_views']
            indexes = result['has_indexes']
            print(f"   ✅ {filename}: {lines} lines, views: {views}, indexes: {indexes}")
            if result['potential_issues']:
                for issue in result['potential_issues']:
                    print(f"      ⚠️  {issue}")
        else:
            print(f"   ❌ {filename}: {result['error']}")
    
    # Python Results
    print("\n3. PYTHON SCRIPTS:")
    for filename, result in python_results.items():
        status = result['status']
        if status == 'SUCCESS':
            lines = result['lines']
            classes = result['has_classes']
            functions = result['has_functions']
            print(f"   ✅ {filename}: {lines} lines, classes: {classes}, functions: {functions}")
            if result['potential_issues']:
                for issue in result['potential_issues']:
                    print(f"      ⚠️  {issue}")
        else:
            print(f"   ❌ {filename}: {result['error']}")
    
    # Completeness Results
    print("\n4. PROJECT COMPLETENESS:")
    all_complete = True
    for category, result in completeness_results.items():
        required = result['required']
        present = result['present']
        if present == required:
            print(f"   ✅ {category}: {present}/{required} files present")
        else:
            print(f"   ❌ {category}: {present}/{required} files present")
            print(f"      Missing: {', '.join(result['missing'])}")
            all_complete = False
    
    # Requirements Results
    print("\n5. FRAUD DETECTION REQUIREMENTS:")
    requirements_met = 0
    total_requirements = len(requirements_results)
    for requirement, status in requirements_results.items():
        if status:
            print(f"   ✅ {requirement}")
            requirements_met += 1
        else:
            print(f"   ❌ {requirement}")
    
    # Overall Assessment
    print("\n" + "="*60)
    print("OVERALL ASSESSMENT")
    print("="*60)
    
    overall_score = (requirements_met / total_requirements) * 100
    
    print(f"Requirements Met: {requirements_met}/{total_requirements} ({overall_score:.1f}%)")
    print(f"Project Completeness: {'✅ COMPLETE' if all_complete else '⚠️  INCOMPLETE'}")
    
    if overall_score >= 90:
        print("🎉 PROJECT STATUS: EXCELLENT - Ready for execution!")
    elif overall_score >= 75:
        print("✅ PROJECT STATUS: GOOD - Minor issues to address")
    elif overall_score >= 50:
        print("⚠️  PROJECT STATUS: FAIR - Several issues need attention")
    else:
        print("❌ PROJECT STATUS: NEEDS WORK - Major issues present")
    
    # Next Steps
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("1. Install required Python packages: pip install -r requirements.txt")
    print("2. Set up PostgreSQL database and update credentials in config")
    print("3. Run the complete analysis: python main_analysis.py")
    print("4. Review generated reports in the 'reports' folder")
    print("5. Examine visualizations in HTML format")

if __name__ == "__main__":
    main()
