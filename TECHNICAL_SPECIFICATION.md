# Omaha Drain Technician KPI Dashboard - Technical Specification

## Executive Summary

This document provides a comprehensive technical specification for the Omaha Drain Technician KPI Dashboard, a web-based business intelligence solution designed to track and analyze service technician performance metrics. The system integrates data from four distinct Excel files to generate unified KPI reports and visualizations.

## 1. System Overview

### 1.1 Purpose
The Omaha Drain KPI Dashboard enables management to:
- Monitor technician performance in real-time
- Identify performance trends and patterns
- Make data-driven decisions for service optimization
- Track revenue generation and service sales
- Improve operational efficiency through actionable insights

### 1.2 Key Features
- **Multi-source Data Integration**: Combines 4 Excel files into unified dataset
- **8 Core KPIs**: Comprehensive performance metrics for each technician
- **Interactive Visualizations**: Real-time charts and graphs
- **Weekly Reporting**: Flexible time-based analysis
- **Technician Filtering**: Individual and aggregate performance views
- **Data Validation**: Robust error handling and validation

## 2. System Architecture

### 2.1 Technology Stack
```
Frontend Framework: Streamlit 1.46.1
Data Processing: Pandas 2.3.1
Excel Handling: OpenPyXL 3.1.5
Visualization: Plotly 6.2.0
Numerical Computing: NumPy 2.0.2
Deployment: Streamlit Cloud / Local Server
```

### 2.2 System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │  Data Processor │    │   Dashboard UI  │
│   (4 Excel      │───▶│   (Pandas/      │───▶│   (Streamlit)   │
│    Files)       │    │   OpenPyXL)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  KPI Calculator │
                       │   (Custom       │
                       │    Logic)       │
                       └─────────────────┘
```

### 2.3 Data Flow
1. **Data Upload**: Users upload 4 Excel files via web interface
2. **Data Validation**: System validates file format and required columns
3. **Data Processing**: Pandas processes and filters data by week
4. **KPI Calculation**: Custom calculator computes 8 performance metrics
5. **Visualization**: Plotly generates interactive charts and metrics
6. **Display**: Streamlit renders dashboard with real-time updates

## 3. Data Requirements and Integration

### 3.1 Input Data Sources

#### 3.1.1 Job Data File (`sample_job_data.xlsx`)
**Purpose**: Track job assignments, completion status, and time tracking
**Required Columns**:
- `Technician`: Technician name/ID
- `Job_ID`: Unique job identifier
- `Status`: Job status (Completed, In Progress, Assigned, Cancelled)
- `Date`: Job date (datetime format)
- `Hours`: Time spent on job (numeric)

**Data Validation Rules**:
- Technician field cannot be null
- Job_ID must be unique
- Status must be one of predefined values
- Date must be valid datetime
- Hours must be positive numeric value

#### 3.1.2 Revenue Data File (`sample_revenue_data.xlsx`)
**Purpose**: Track revenue generated per job
**Required Columns**:
- `Technician`: Technician name/ID
- `Job_ID`: Unique job identifier (links to Job Data)
- `Revenue`: Revenue amount (numeric)
- `Date`: Revenue date (datetime format)

**Data Validation Rules**:
- Job_ID must exist in Job Data file
- Revenue must be positive numeric value
- Date must be valid datetime

#### 3.1.3 Membership Data File (`sample_membership_data.xlsx`)
**Purpose**: Track membership sales and opportunities
**Required Columns**:
- `Technician`: Technician name/ID
- `Customer_ID`: Unique customer identifier
- `Membership_Type`: Type of membership (Premium, Gold, Basic, null for opportunities)
- `Date`: Membership date (datetime format)

**Data Validation Rules**:
- Customer_ID must be unique
- Membership_Type must be one of predefined values or null
- Date must be valid datetime

#### 3.1.4 Service Sales Data File (`sample_service_data.xlsx`)
**Purpose**: Track specific service sales (Hydro Jetting, Descaling, Water Heater)
**Required Columns**:
- `Technician`: Technician name/ID
- `Service_Type`: Type of service sold
- `Date`: Service date (datetime format)
- `Revenue`: Service revenue (numeric)

**Data Validation Rules**:
- Service_Type must be one of: "Hydro Jetting", "Descaling", "Water Heater"
- Revenue must be positive numeric value
- Date must be valid datetime

### 3.2 Data Integration Process

#### 3.2.1 Data Loading
```python
def load_and_process_data(job_file, revenue_file, membership_file, service_file):
    """Load and process all uploaded files"""
    data = {}
    
    # Load each file with error handling
    if job_file:
        data['jobs'] = pd.read_excel(job_file)
    if revenue_file:
        data['revenue'] = pd.read_excel(revenue_file)
    if membership_file:
        data['membership'] = pd.read_excel(membership_file)
    if service_file:
        data['services'] = pd.read_excel(service_file)
    
    return data
```

#### 3.2.2 Data Filtering
```python
def filter_week_data(self, df, date_column):
    """Filter data for the specified week"""
    df[date_column] = pd.to_datetime(df[date_column])
    mask = (df[date_column] >= self.week_start) & (df[date_column] <= self.week_end)
    return df[mask]
```

#### 3.2.3 Data Validation
- **File Format Validation**: Ensure files are valid Excel format
- **Column Validation**: Verify required columns exist
- **Data Type Validation**: Ensure data types match expectations
- **Referential Integrity**: Validate relationships between files
- **Date Range Validation**: Ensure dates fall within expected ranges

## 4. KPI Calculations

### 4.1 Core Performance Metrics

#### 4.1.1 Average Ticket Value
**Formula**: `Total Revenue ÷ Completed Jobs`
**Calculation Logic**:
```python
def calculate_average_ticket_value(self, revenue_data, job_data):
    # Filter for completed jobs only
    completed_jobs = job_data[job_data['Status'].str.contains('Completed', case=False, na=False)]
    
    # Group by technician and calculate average
    avg_ticket = revenue_data.groupby('Technician')['Revenue'].mean().reset_index()
    return avg_ticket
```
**Business Impact**: Measures revenue efficiency per job

#### 4.1.2 Job Close Rate
**Formula**: `(Completed Jobs ÷ Total Assigned Jobs) × 100%`
**Calculation Logic**:
```python
def calculate_job_close_rate(self, job_data):
    # Count total jobs and completed jobs per technician
    total_jobs = job_data.groupby('Technician').size().reset_index(name='Total_Jobs')
    completed_jobs = job_data[job_data['Status'].str.contains('Completed', case=False, na=False)]
    completed_count = completed_jobs.groupby('Technician').size().reset_index(name='Completed_Jobs')
    
    # Calculate rate
    close_rate = total_jobs.merge(completed_count, on='Technician', how='left').fillna(0)
    close_rate['Job_Close_Rate'] = (close_rate['Completed_Jobs'] / close_rate['Total_Jobs'] * 100).round(1)
    return close_rate
```
**Business Impact**: Measures job completion efficiency

#### 4.1.3 Weekly Revenue
**Formula**: `Sum of all revenue for the week per technician`
**Calculation Logic**:
```python
def calculate_weekly_revenue(self, revenue_data):
    weekly_revenue = revenue_data.groupby('Technician')['Revenue'].sum().reset_index()
    return weekly_revenue
```
**Business Impact**: Direct revenue performance measurement

#### 4.1.4 Job Efficiency
**Formula**: `Completed Jobs ÷ Total Hours Worked`
**Calculation Logic**:
```python
def calculate_job_efficiency(self, job_data):
    # Filter for completed jobs with hours data
    completed_jobs = job_data[
        (job_data['Status'].str.contains('Completed', case=False, na=False)) &
        (job_data['Hours'].notna())
    ]
    
    # Calculate efficiency
    efficiency = completed_jobs.groupby('Technician').agg({
        'Job_ID': 'count',
        'Hours': 'sum'
    }).reset_index()
    
    efficiency['Job_Efficiency'] = (efficiency['Job_ID'] / efficiency['Hours']).round(2)
    return efficiency
```
**Business Impact**: Measures productivity per hour worked

#### 4.1.5 Membership Win Rate
**Formula**: `(Memberships Sold ÷ Total Opportunities) × 100%`
**Calculation Logic**:
```python
def calculate_membership_win_rate(self, membership_data):
    # Count total opportunities and wins per technician
    total_opportunities = membership_data.groupby('Technician').size().reset_index(name='Total_Opportunities')
    wins = membership_data[membership_data['Membership_Type'].notna()]
    win_count = wins.groupby('Technician').size().reset_index(name='Memberships_Won')
    
    # Calculate rate
    win_rate = total_opportunities.merge(win_count, on='Technician', how='left').fillna(0)
    win_rate['Membership_Win_Rate'] = (win_rate['Memberships_Won'] / win_rate['Total_Opportunities'] * 100).round(1)
    return win_rate
```
**Business Impact**: Measures sales conversion effectiveness

#### 4.1.6 Service Sales Metrics
**Formulas**:
- Hydro Jetting Jobs Sold: `Count of Hydro Jetting services`
- Descaling Jobs Sold: `Count of Descaling services`
- Water Heater Jobs Sold: `Count of Water Heater services`

**Calculation Logic**:
```python
def calculate_service_sales(self, service_data):
    # Count each service type
    service_counts = service_data.groupby(['Technician', 'Service_Type']).size().reset_index(name='Count')
    
    # Pivot to get each service as a column
    service_pivot = service_counts.pivot(index='Technician', columns='Service_Type', values='Count').fillna(0)
    return service_pivot
```
**Business Impact**: Tracks specific service line performance

### 4.2 KPI Aggregation and Reporting

#### 4.2.1 Technician-Level Aggregation
```python
def calculate_all_kpis(self, data):
    """Calculate all KPIs and return comprehensive results"""
    # Filter data for the week
    week_jobs = self.filter_week_data(data.get('jobs', pd.DataFrame()), 'Date')
    week_revenue = self.filter_week_data(data.get('revenue', pd.DataFrame()), 'Date')
    week_membership = self.filter_week_data(data.get('membership', pd.DataFrame()), 'Date')
    week_services = self.filter_week_data(data.get('services', pd.DataFrame()), 'Date')
    
    # Calculate individual KPIs
    avg_ticket = self.calculate_average_ticket_value(week_revenue, week_jobs)
    close_rate = self.calculate_job_close_rate(week_jobs)
    weekly_revenue = self.calculate_weekly_revenue(week_revenue)
    efficiency = self.calculate_job_efficiency(week_jobs)
    membership_rate = self.calculate_membership_win_rate(week_membership)
    service_sales = self.calculate_service_sales(week_services)
    
    # Combine all KPIs into unified dataset
    return self.combine_kpi_data(avg_ticket, close_rate, weekly_revenue, 
                                efficiency, membership_rate, service_sales)
```

#### 4.2.2 Data Combination Strategy
- **Technician Matching**: Use technician names as primary key
- **Missing Data Handling**: Fill missing values with 0 or appropriate defaults
- **Data Consistency**: Ensure all technicians appear in final dataset
- **Performance Optimization**: Use efficient pandas operations

## 5. User Interface Design

### 5.1 Dashboard Layout

#### 5.1.1 Header Section
- **Title**: "🔧 Omaha Drain Technician KPI Dashboard"
- **Navigation**: Week selection, technician filtering
- **Status Indicators**: File upload status, data processing status

#### 5.1.2 Sidebar Configuration
```python
with st.sidebar:
    st.header("📊 Dashboard Configuration")
    
    # Week selection
    week_start = st.date_input("Week Start Date", value=current_date)
    
    # Technician filter
    show_all_technicians = st.checkbox("Show All Technicians", value=True)
    
    # KPI definitions
    st.markdown("### 📋 KPI Definitions")
```

#### 5.1.3 Main Dashboard Area
- **File Upload Section**: 4 file upload widgets in 2x2 grid
- **KPI Metrics Section**: 8 metric cards in 4x2 grid
- **Visualization Section**: Charts and graphs
- **Data Table Section**: Detailed KPI breakdown

### 5.2 Interactive Elements

#### 5.2.1 File Upload Interface
```python
col1, col2 = st.columns(2)

with col1:
    job_data_file = st.file_uploader("Upload Job Data", type=['xlsx', 'xls'])
    revenue_data_file = st.file_uploader("Upload Revenue Data", type=['xlsx', 'xls'])

with col2:
    membership_data_file = st.file_uploader("Upload Membership Data", type=['xlsx', 'xls'])
    service_data_file = st.file_uploader("Upload Service Sales Data", type=['xlsx', 'xls'])
```

#### 5.2.2 KPI Display Cards
```python
cols = st.columns(4)

with cols[0]:
    st.metric(
        label="Average Ticket Value",
        value=f"${kpis_df['avg_ticket_value'].mean():.0f}",
        delta=f"{kpis_df['avg_ticket_value'].std():.1f}"
    )
```

#### 5.2.3 Interactive Visualizations
- **Bar Charts**: Technician performance comparison
- **Line Charts**: Time series trends
- **Pie Charts**: Service type distribution
- **Heatmaps**: Performance correlation analysis

### 5.3 Responsive Design
- **Mobile Compatibility**: Responsive layout for tablets and phones
- **Screen Adaptation**: Automatic column adjustment based on screen size
- **Loading States**: Progress indicators for data processing
- **Error Handling**: User-friendly error messages and recovery options

## 6. Data Visualization

### 6.1 Chart Types and Purposes

#### 6.1.1 Performance Comparison Charts
```python
def create_performance_comparison(kpis_df):
    fig = px.bar(kpis_df, x='Technician', y=['avg_ticket_value', 'job_close_rate'],
                 title='Technician Performance Comparison',
                 barmode='group')
    return fig
```

#### 6.1.2 Trend Analysis Charts
```python
def create_trend_analysis(historical_data):
    fig = px.line(historical_data, x='Week', y='weekly_revenue',
                  color='Technician', title='Weekly Revenue Trends')
    return fig
```

#### 6.1.3 Service Sales Distribution
```python
def create_service_distribution(service_data):
    fig = px.pie(service_data, values='Count', names='Service_Type',
                 title='Service Sales Distribution')
    return fig
```

### 6.2 Interactive Features
- **Hover Information**: Detailed tooltips on chart elements
- **Zoom and Pan**: Interactive chart navigation
- **Filtering**: Dynamic data filtering through chart interactions
- **Export Options**: Chart export to PNG, PDF formats

## 7. System Performance and Scalability

### 7.1 Performance Requirements
- **Data Loading**: < 5 seconds for files up to 10MB
- **KPI Calculation**: < 3 seconds for 1000+ records
- **Dashboard Rendering**: < 2 seconds for initial load
- **Chart Generation**: < 1 second per chart

### 7.2 Scalability Considerations
- **Data Volume**: Support for up to 50,000 records per file
- **Concurrent Users**: Support for 10+ simultaneous users
- **Memory Usage**: Efficient memory management for large datasets
- **Caching**: Implement data caching for improved performance

### 7.3 Optimization Strategies
```python
@st.cache_data
def load_and_process_data(job_file, revenue_file, membership_file, service_file):
    """Cached data loading for improved performance"""
    # Implementation with caching
```

## 8. Error Handling and Data Validation

### 8.1 Input Validation
```python
def validate_excel_file(file, required_columns):
    """Validate Excel file format and required columns"""
    try:
        df = pd.read_excel(file)
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        return df
    except Exception as e:
        st.error(f"Error validating file: {str(e)}")
        return None
```

### 8.2 Data Quality Checks
- **Null Value Detection**: Identify and handle missing data
- **Data Type Validation**: Ensure correct data types
- **Range Validation**: Check for reasonable value ranges
- **Consistency Checks**: Verify data consistency across files

### 8.3 Error Recovery
- **Graceful Degradation**: Continue operation with partial data
- **User Feedback**: Clear error messages and recovery suggestions
- **Data Backup**: Automatic backup of processed data
- **Logging**: Comprehensive error logging for debugging

## 9. Security and Data Privacy

### 9.1 Data Security
- **File Upload Security**: Validate file types and scan for malware
- **Data Encryption**: Encrypt sensitive data in transit and at rest
- **Access Control**: Implement user authentication and authorization
- **Audit Logging**: Track all data access and modifications

### 9.2 Privacy Protection
- **Data Anonymization**: Remove personally identifiable information
- **Data Retention**: Implement data retention policies
- **Compliance**: Ensure GDPR and other privacy regulation compliance
- **Secure Disposal**: Proper data disposal procedures

## 10. Deployment and Maintenance

### 10.1 Deployment Options

#### 10.1.1 Local Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app.py --server.headless true --server.port 8501
```

#### 10.1.2 Cloud Deployment
- **Streamlit Cloud**: Direct deployment from GitHub
- **AWS/GCP/Azure**: Container-based deployment
- **Heroku**: Platform-as-a-Service deployment

### 10.2 Maintenance Procedures
- **Regular Updates**: Keep dependencies updated
- **Backup Procedures**: Regular data and configuration backups
- **Monitoring**: System health monitoring and alerting
- **Documentation**: Maintain up-to-date documentation

### 10.3 Version Control
- **Git Repository**: Source code version control
- **Release Management**: Tagged releases for production
- **Change Log**: Document all changes and updates
- **Rollback Procedures**: Ability to rollback to previous versions

## 11. Testing Strategy

### 11.1 Unit Testing
```python
def test_average_ticket_value_calculation():
    """Test average ticket value calculation"""
    calculator = KPICalculator()
    test_data = {
        'revenue': pd.DataFrame({
            'Technician': ['John', 'John', 'Mike'],
            'Revenue': [100, 200, 150]
        }),
        'jobs': pd.DataFrame({
            'Technician': ['John', 'John', 'Mike'],
            'Status': ['Completed', 'Completed', 'Completed']
        })
    }
    
    result = calculator.calculate_average_ticket_value(
        test_data['revenue'], test_data['jobs']
    )
    
    assert result['Average_Ticket_Value'].iloc[0] == 150  # (100+200)/2
```

### 11.2 Integration Testing
- **Data Integration Tests**: Verify data combination logic
- **KPI Calculation Tests**: Validate all KPI formulas
- **UI Component Tests**: Test dashboard functionality
- **End-to-End Tests**: Complete workflow testing

### 11.3 Performance Testing
- **Load Testing**: Test with large datasets
- **Stress Testing**: Test system limits
- **Memory Testing**: Monitor memory usage
- **Response Time Testing**: Measure system responsiveness

## 12. Future Enhancements

### 12.1 Planned Features
- **Historical Trend Analysis**: Multi-week performance tracking
- **Predictive Analytics**: Performance forecasting
- **Mobile App**: Native mobile application
- **API Integration**: Real-time data feeds
- **Advanced Reporting**: Custom report generation

### 12.2 Technical Improvements
- **Database Integration**: Replace Excel files with database
- **Real-time Updates**: Live data synchronization
- **Advanced Visualizations**: 3D charts and interactive dashboards
- **Machine Learning**: Automated insights and recommendations

## 13. Conclusion

The Omaha Drain Technician KPI Dashboard provides a comprehensive solution for tracking and analyzing service technician performance. The system successfully addresses the challenge of integrating data from multiple Excel sources while providing actionable insights through intuitive visualizations and calculated metrics.

Key strengths of the system include:
- **Robust Data Integration**: Seamless combination of 4 data sources
- **Comprehensive KPI Calculation**: 8 key performance indicators
- **User-Friendly Interface**: Intuitive web-based dashboard
- **Scalable Architecture**: Support for growth and expansion
- **Quality Assurance**: Comprehensive testing and validation

The technical specification provides a solid foundation for implementation, maintenance, and future enhancements of the dashboard system.

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Author**: Technical Development Team  
**Review Cycle**: Quarterly 