#!/bin/bash

# Titanic ETL Project Setup Script
echo "🚀 Setting up Titanic ETL Project..."

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 Project directory: $PROJECT_DIR"

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create data directory
echo "📂 Creating data directory..."
mkdir -p data

# Setup Airflow DAGs
echo "✈️ Setting up Airflow DAGs..."
AIRFLOW_HOME="${HOME}/airflow"
mkdir -p "${AIRFLOW_HOME}/dags"

# Copy DAG with dynamic path
cp orchestration/dags/dag.py "${AIRFLOW_HOME}/dags/titanic_pipeline_dag.py"

# Update DAG to use current project path
sed -i "s|titanic-etl-project|$(basename "$PROJECT_DIR")|g" "${AIRFLOW_HOME}/dags/titanic_pipeline_dag.py"

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Test individual components:"
echo "   - python extraction/extract.py"
echo "   - python transformation/transform.py" 
echo "   - python loading/load.py"
echo "3. Start Airflow: airflow standalone"
echo "4. Access Airflow UI: http://localhost:8080"