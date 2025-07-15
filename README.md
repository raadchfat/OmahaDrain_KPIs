# Omaha Drain Technician KPI Dashboard

A comprehensive web-based business intelligence dashboard for tracking service technician performance metrics at Omaha Drain.

## Features

- **8 Key Performance Indicators (KPIs)**:
  - Average Ticket Value
  - Job Close Rate
  - Weekly Revenue
  - Job Efficiency
  - Membership Win Rate
  - Hydro Jetting Jobs Sold
  - Descaling Jobs Sold
  - Water Heater Jobs Sold

- **Interactive Dashboard**: Real-time KPI visualization with charts and metrics
- **Excel File Integration**: Upload 4 different Excel files for comprehensive data analysis
- **Weekly Reporting**: Select specific weeks for performance analysis
- **Technician Filtering**: View individual or all technician performance
- **Data Validation**: Robust error handling for corrupted or invalid Excel files

## Installation

1. Clone or download this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the dashboard:
   ```bash
   streamlit run app.py
   ```

## Data Requirements

The dashboard requires 4 Excel files:

### 1. Job Data
Columns: Technician, Job ID, Status, Date, Hours

### 2. Revenue Data
Columns: Technician, Job ID, Revenue, Date

### 3. Membership Data
Columns: Technician, Customer ID, Membership Type, Date

### 4. Service Sales Data
Columns: Technician, Service Type, Date, Revenue

## Usage

1. Open the dashboard in your web browser
2. Upload the 4 required Excel files
3. Select the reporting week
4. View KPI metrics and visualizations
5. Filter by technician if needed

## KPI Calculations

- **Average Ticket Value**: Total revenue ÷ completed jobs
- **Job Close Rate**: Completed jobs ÷ assigned jobs × 100%
- **Weekly Revenue**: Total revenue for the week
- **Job Efficiency**: Jobs completed per hour
- **Membership Win Rate**: Memberships sold ÷ opportunities × 100%
- **Service Sales**: Count of specific services sold

## Technical Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Excel Handling**: OpenPyXL

## Support

For technical support or questions about data format, contact your BI development team.
