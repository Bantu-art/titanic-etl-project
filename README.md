# Titanic Data Pipeline

A complete ETL (Extract, Transform, Load) pipeline for processing Titanic passenger data using Apache Airflow for orchestration. This pipeline extracts data from a remote source, cleans and transforms it, and loads it into a SQLite database.

## Project Structure

```
titanic_pipeline/
├── data/                    # Data storage directory
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
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Prerequisites

- Python 3.8 or higher
- Apache Airflow (configured separately in ~/airflow)
- Internet connection (for data extraction)

## Installation & Setup

### 1. Clone/Navigate to Project Directory

```bash
cd /home/bantu/dataProjects/titanic_pipeline
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Check if Airflow is properly installed
airflow version

# Check if pandas is working
python -c "import pandas as pd; print('Pandas version:', pd.__version__)"
```

### 5. Setup Airflow Configuration

Since your Airflow configuration is in the `~/airflow` directory, ensure the DAG is accessible:

```bash
# Create symbolic link to make DAG accessible to Airflow
ln -sf /home/bantu/dataProjects/titanic_pipeline/orchestration/dags/dag.py ~/airflow/dags/titanic_pipeline_dag.py

# Or copy the DAG file
cp orchestration/dags/dag.py ~/airflow/dags/titanic_pipeline_dag.py
```

### 6. Initialize Airflow Database (if not done already)

```bash
# Initialize Airflow database
airflow db init

# Create admin user (if not exists)
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
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

- **Owner**: bantu
- **Schedule**: Daily (`@daily`)
- **Start Date**: September 5, 2025
- **Catchup**: Disabled (only runs for current dates)

### File Paths

All scripts use absolute paths to ensure compatibility with Airflow:
- Data directory: `/home/bantu/dataProjects/titanic_pipeline/data`
- Project root: `/home/bantu/dataProjects/titanic_pipeline`

## Troubleshooting

### Common Issues

1. **Import Errors in Airflow**
   ```bash
   # Ensure project path is in Python path
   export PYTHONPATH="${PYTHONPATH}:/home/bantu/dataProjects/titanic_pipeline"
   ```

2. **Permission Issues**
   ```bash
   # Make sure data directory is writable
   chmod 755 /home/bantu/dataProjects/titanic_pipeline/data
   ```

3. **Virtual Environment Issues**
   ```bash
   # Deactivate and reactivate
   deactivate
   source venv/bin/activate
   ```

4. **Airflow DAG Not Visible**
   ```bash
   # Check DAG syntax
   python orchestration/dags/dag.py
   
   # Refresh Airflow
   airflow dags list | grep titanic
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

## License

This project is for educational purposes.