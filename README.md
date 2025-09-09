# Titanic Data Pipeline

A complete ETL (Extract, Transform, Load) pipeline for processing Titanic passenger data using Apache Airflow for orchestration. This pipeline extracts data from a remote source, cleans and transforms it, and loads it into a SQLite database.

## Project Structure

```
titanic-etl-project/
├── data/                    # Data storage directory (created during setup)
│   ├── raw_titanic.csv     # Raw extracted data
│   ├── clean_titanic.csv   # Transformed data
│   └── titanic.db          # SQLite database
├── extraction/             # Data extraction module
│   ├── extract.py          # Main extraction script
│   └── test.py             # Extraction testing script
├── transformation/         # Data transformation module
│   ├── transform.py        # Main transformation script
│   └── test.py             # Transformation testing script
├── loading/                # Data loading module
│   └── load.py             # Database loading script
├── orchestration/          # Airflow orchestration
│   └── dags/
│       └── dag.py          # Airflow DAG definition
├── venv/                   # Virtual environment (created during setup)
├── requirements.txt        # Python dependencies
├── setup.sh               # Automated setup script
└── README.md              # This file
```

## Prerequisites

- Python 3.8 or higher
- Apache Airflow (configured separately in ~/airflow)
- Internet connection (for data extraction)

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd titanic-etl-project

# Run automated setup
./setup.sh

# Activate virtual environment
source venv/bin/activate
```

### Option 2: Manual Setup

```bash
# Clone and navigate to project
git clone <repository-url>
cd titanic-etl-project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create data directory
mkdir -p data

# Setup Airflow DAG
mkdir -p ~/airflow/dags
cp orchestration/dags/dag.py ~/airflow/dags/titanic_pipeline_dag.py
```

### Verify Installation

```bash
# Check if Airflow is properly installed
airflow version

# Check if pandas is working
python -c "import pandas as pd; print('Pandas version:', pd.__version__)"
```

## How It Works

### Pipeline Components

#### 1. **Extract** (`extraction/extract.py`)
- Downloads Titanic dataset from GitHub repository
- Saves raw data as `data/raw_titanic.csv`
- Source: https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv

#### 2. **Transform** (`transformation/transform.py`)
- **Age Imputation**: Fills missing ages with median age by Sex and Passenger Class
- **Data Cleaning**: Removes Cabin column (too many missing values)
- **Embarked Imputation**: Fills missing embarkation ports with most common value
- **Name Processing**: Extracts surnames into separate column, cleans name format
- **Ticket Processing**: Extracts ticket prefixes for better analysis
- Saves cleaned data as `data/clean_titanic.csv`

#### 3. **Load** (`loading/load.py`)
- Loads transformed data into SQLite database
- Creates `titanic_passengers` table in `data/titanic.db`
- Replaces existing data on each run

#### 4. **Orchestration** (`orchestration/dags/dag.py`)
- Airflow DAG that coordinates the entire pipeline
- Runs daily at scheduled time
- Ensures proper execution order: Extract → Transform → Load

## Running the Pipeline

### Option 1: Run Individual Components (Testing)

```bash
# Activate virtual environment
source venv/bin/activate

# Run extraction only
python extraction/extract.py

# Run transformation only (requires raw data)
python transformation/transform.py

# Run loading only (requires clean data)
python loading/load.py
```

### Option 2: Run via Airflow (Production)

```bash
# Start Airflow webserver (in one terminal)
airflow webserver --port 8080

# Start Airflow scheduler (in another terminal)
airflow scheduler

# Access Airflow UI at http://localhost:8080
# Enable and trigger the 'titanic_pipeline' DAG
```

### Option 3: Run Airflow DAG from Command Line

```bash
# Test the DAG
airflow dags test titanic_pipeline 2025-01-15

# Run specific task
airflow tasks test titanic_pipeline extract 2025-01-15
airflow tasks test titanic_pipeline transform 2025-01-15
airflow tasks test titanic_pipeline load 2025-01-15
```

## Testing

The project includes test scripts for development and debugging:

```bash
# Test extraction (saves to parent directory)
python extraction/test.py

# Test transformation (works with relative paths)
python transformation/test.py
```

## Data Flow

1. **Raw Data**: Original Titanic dataset with missing values and inconsistent formatting
2. **Transformed Data**: Cleaned dataset with:
   - Imputed missing ages (grouped by sex and class)
   - Removed cabin column
   - Filled missing embarkation ports
   - Extracted surnames and ticket prefixes
   - Consistent formatting
3. **Database**: SQLite database with `titanic_passengers` table for analysis

## Configuration

### Key Settings in DAG

- **Owner**: data_engineer
- **Schedule**: Daily (`@daily`)
- **Start Date**: January 1, 2024
- **Catchup**: Disabled (only runs for current dates)

### File Paths

All scripts use relative paths for portability:
- Automatically detects project root directory
- Works from any installation location
- No hardcoded paths

## Troubleshooting

### Common Issues

1. **DAG Not Visible in Airflow**
   ```bash
   # Check if DAG file exists
   ls ~/airflow/dags/titanic_pipeline_dag.py
   
   # Test DAG syntax
   python ~/airflow/dags/titanic_pipeline_dag.py
   
   # List all DAGs
   airflow dags list | grep titanic
   ```

2. **Permission Issues**
   ```bash
   # Make setup script executable
   chmod +x setup.sh
   
   # Ensure data directory is writable
   chmod 755 data/
   ```

3. **Virtual Environment Issues**
   ```bash
   # Deactivate and reactivate
   deactivate
   source venv/bin/activate
   
   # Reinstall dependencies if needed
   pip install -r requirements.txt
   ```

4. **Path Issues**
   ```bash
   # All scripts now use relative paths
   # Run from project root directory
   cd titanic-etl-project
   python extraction/extract.py
   ```

## Dependencies

Key packages used:
- **apache-airflow**: Workflow orchestration
- **pandas**: Data manipulation and analysis
- **sqlite3**: Database operations (built-in)
- **requests**: HTTP requests (via pandas)

## Next Steps

- Add data validation tests
- Implement error handling and retry logic
- Add data quality checks
- Create visualization dashboard
- Add email notifications for pipeline failures
- Implement incremental data loading
- Add Docker containerization
- Create CI/CD pipeline

## License

This project is for educational purposes.