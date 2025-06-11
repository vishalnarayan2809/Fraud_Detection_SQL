"""
Environment Setup Script for Fraud Detection System
"""

import os
import sys
import subprocess
import yaml
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnvironmentSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config_dir = self.project_root / "config"
        
    def check_python_version(self):
        """Check if Python version is compatible"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            raise Exception("Python 3.8 or higher is required")
        logger.info(f"Python version {version.major}.{version.minor}.{version.micro} is compatible")
        
    def install_requirements(self):
        """Install Python requirements"""
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            raise Exception("requirements.txt not found")
            
        logger.info("Installing Python requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
        logger.info("Requirements installed successfully")
        
    def create_directories(self):
        """Create necessary directories"""
        directories = [
            "reports/visualizations",
            "reports/csv_exports", 
            "backups",
            "logs",
            "temp"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
            
    def setup_environment_variables(self):
        """Setup environment variables"""
        env_file = self.project_root / ".env"
        
        if not env_file.exists():
            logger.info("Creating .env file...")
            env_content = """# Fraud Detection Environment Variables
DB_PASSWORD=fraud_detection_2024
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fraud_detection
DB_USER=postgres

# Security
SECRET_KEY=your-secret-key-here
DEBUG=false

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/fraud_detection.log
"""
            with open(env_file, 'w') as f:
                f.write(env_content)
            logger.info("Created .env file with default values")
        else:
            logger.info(".env file already exists")
            
    def check_docker(self):
        """Check if Docker is available"""
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
            logger.info("Docker is available")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("Docker not found. You'll need to setup PostgreSQL manually")
            return False
            
    def setup_database_with_docker(self):
        """Setup database using Docker Compose"""
        if not self.check_docker():
            return False
            
        docker_compose_file = self.project_root / "docker-compose.yml"
        if not docker_compose_file.exists():
            logger.error("docker-compose.yml not found")
            return False
            
        logger.info("Starting PostgreSQL with Docker Compose...")
        try:
            subprocess.run(
                ["docker-compose", "up", "-d"], 
                cwd=self.project_root, 
                check=True
            )
            logger.info("PostgreSQL started successfully")
            logger.info("Database will be available at localhost:5432")
            logger.info("PgAdmin will be available at http://localhost:8080")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start Docker services: {e}")
            return False
            
    def validate_setup(self):
        """Validate the setup"""
        logger.info("Validating setup...")
        
        # Check required files
        required_files = [
            "src/__init__.py",
            "config/database.yaml",
            "config/fraud_rules.yaml",
            "sql/schema.sql",
            "requirements.txt"
        ]
        
        for file_path in required_files:
            if not (self.project_root / file_path).exists():
                logger.error(f"Required file missing: {file_path}")
                return False
        
        # Try importing main modules
        try:
            sys.path.insert(0, str(self.project_root))
            from src import FraudDetectionPipeline
            logger.info("Main modules can be imported successfully")
        except ImportError as e:
            logger.error(f"Import error: {e}")
            return False
            
        logger.info("Setup validation completed successfully")
        return True
        
    def run_setup(self):
        """Run complete setup process"""
        logger.info("Starting Fraud Detection System setup...")
        
        try:
            self.check_python_version()
            self.install_requirements()
            self.create_directories()
            self.setup_environment_variables()
            
            # Try Docker setup
            docker_success = self.setup_database_with_docker()
            
            if not docker_success:
                logger.info("Manual database setup required:")
                logger.info("1. Install PostgreSQL")
                logger.info("2. Create database: CREATE DATABASE fraud_detection;")
                logger.info("3. Update config/database.yaml with your credentials")
                
            self.validate_setup()
            
            logger.info("=" * 60)
            logger.info("🎉 SETUP COMPLETED SUCCESSFULLY!")
            logger.info("=" * 60)
            logger.info("Next steps:")
            logger.info("1. Update config/database.yaml with your database credentials")
            logger.info("2. Run: python src/main_analysis.py")
            logger.info("3. Check reports/ directory for results")
            
            if docker_success:
                logger.info("\nDocker services started:")
                logger.info("- PostgreSQL: localhost:5432")
                logger.info("- PgAdmin: http://localhost:8080")
                logger.info("  (Email: admin@frauddetection.com, Password: admin123)")
                
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            sys.exit(1)

def main():
    """Main setup function"""
    setup = EnvironmentSetup()
    setup.run_setup()

if __name__ == "__main__":
    main()
