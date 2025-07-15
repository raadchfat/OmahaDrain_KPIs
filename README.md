# 🔧 Omaha Drain Technician KPI Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.46.1-red.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.3.1-green.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

A comprehensive web-based business intelligence dashboard for tracking service technician performance metrics at Omaha Drain. This system integrates data from four distinct Excel files to generate unified KPI reports and visualizations.

## 📊 Features

### 🎯 8 Key Performance Indicators (KPIs)
- **Average Ticket Value** - Revenue efficiency per job
- **Job Close Rate** - Job completion efficiency
- **Weekly Revenue** - Direct revenue performance
- **Job Efficiency** - Productivity per hour worked
- **Membership Win Rate** - Sales conversion effectiveness
- **Hydro Jetting Jobs Sold** - Service line performance
- **Descaling Jobs Sold** - Service line performance
- **Water Heater Jobs Sold** - Service line performance

### 🚀 Core Capabilities
- **Interactive Dashboard**: Real-time KPI visualization with charts and metrics
- **Multi-Source Data Integration**: Upload 4 different Excel files for comprehensive analysis
- **Weekly Reporting**: Select specific weeks for performance analysis
- **Technician Filtering**: View individual or all technician performance
- **Data Validation**: Robust error handling for corrupted or invalid Excel files
- **Responsive Design**: Mobile-compatible interface

## 🏗️ System Architecture

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

## 📁 Data Requirements

The dashboard requires 4 Excel files with specific column requirements:

### 1. Job Data (`sample_job_data.xlsx`)
**Purpose**: Track job assignments, completion status, and time tracking
**Required Columns**:
- `Technician`: Technician name/ID
- `Job_ID`: Unique job identifier
- `Status`: Job status (Completed, In Progress, Assigned, Cancelled)
- `Date`: Job date (datetime format)
- `Hours`: Time spent on job (numeric)

### 2. Revenue Data (`sample_revenue_data.xlsx`)
**Purpose**: Track revenue generated per job
**Required Columns**:
- `Technician`: Technician name/ID
- `Job_ID`: Unique job identifier (links to Job Data)
- `Revenue`: Revenue amount (numeric)
- `Date`: Revenue date (datetime format)

### 3. Membership Data (`sample_membership_data.xlsx`)
**Purpose**: Track membership sales and opportunities
**Required Columns**:
- `Technician`: Technician name/ID
- `Customer_ID`: Unique customer identifier
- `Membership_Type`: Type of membership (Premium, Gold, Basic, null for opportunities)
- `Date`: Membership date (datetime format)

### 4. Service Sales Data (`sample_service_data.xlsx`)
**Purpose**: Track specific service sales (Hydro Jetting, Descaling, Water Heater)
**Required Columns**:
- `Technician`: Technician name/ID
- `Service_Type`: Type of service sold
- `Date`: Service date (datetime format)
- `Revenue`: Service revenue (numeric)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/raadchfat/OmahaDrain_KPIs.git
   cd omaha-drain-kpi-dashboard
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**
   ```bash
   # Start the dashboard
   streamlit run app.py
   
   # Or run in headless mode
   streamlit run app.py --server.headless true --server.port 8501
   ```

5. **Access the dashboard**
   - Open your web browser
   - Navigate to: `http://localhost:8501`
   - Upload the 4 sample Excel files
   - Configure week selection and view KPIs

## 📖 Usage Guide

1. **Upload Data Files**
   - Upload the 4 required Excel files in the "Data Upload" section
   - Ensure files match the required column structure
   - Wait for data validation to complete

2. **Configure Dashboard**
   - Select the reporting week in the sidebar
   - Choose whether to view all technicians or filter by individual
   - The dashboard will automatically update with your data

3. **Analyze Performance**
   - View KPI metrics in the dashboard cards
   - Explore interactive charts and visualizations
   - Compare technician performance across metrics

## 🧮 KPI Calculations

| KPI | Formula | Business Impact |
|-----|---------|----------------|
| **Average Ticket Value** | Total Revenue ÷ Completed Jobs | Revenue efficiency per job |
| **Job Close Rate** | (Completed Jobs ÷ Total Jobs) × 100% | Job completion efficiency |
| **Weekly Revenue** | Sum of all revenue for the week | Direct revenue performance |
| **Job Efficiency** | Completed Jobs ÷ Total Hours | Productivity per hour |
| **Membership Win Rate** | (Memberships Sold ÷ Opportunities) × 100% | Sales conversion effectiveness |
| **Service Sales** | Count of specific services sold | Service line performance |

## 🛠️ Technical Stack

- **Frontend Framework**: [Streamlit](https://streamlit.io/) 1.46.1
- **Data Processing**: [Pandas](https://pandas.pydata.org/) 2.3.1
- **Excel Handling**: [OpenPyXL](https://openpyxl.readthedocs.io/) 3.1.5
- **Visualization**: [Plotly](https://plotly.com/) 6.2.0
- **Numerical Computing**: [NumPy](https://numpy.org/) 2.0.2

## 📚 Documentation

- **[Technical Specification](TECHNICAL_SPECIFICATION.md)** - Complete system architecture and requirements
- **[Implementation Plan](IMPLEMENTATION_PLAN.md)** - 5-phase deployment roadmap
- **[Project Summary](PROJECT_SUMMARY.md)** - Executive overview and business value
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Production deployment instructions

## 🚀 Deployment Options

### Streamlit Cloud (Recommended)
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy the app with main file path: `app.py`

### Docker Deployment
```bash
# Build and run with Docker
docker build -t omaha-drain-kpi-dashboard .
docker run -p 8501:8501 omaha-drain-kpi-dashboard

# Or use Docker Compose
docker-compose up -d
```

### Local Production
```bash
# Install production dependencies
pip install -r requirements_production.txt

# Run with production settings
streamlit run app.py --server.headless true --server.port 8501
```

## 🧪 Testing

### Run Tests
```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### Sample Data
The repository includes sample Excel files for testing:
- `sample_job_data.xlsx`
- `sample_revenue_data.xlsx`
- `sample_membership_data.xlsx`
- `sample_service_data.xlsx`

## 🔧 Development

### Project Structure
```
omaha-drain-kpi-dashboard/
├── app.py                      # Main Streamlit application
├── kpi_calculator.py           # KPI calculation engine
├── create_sample_data.py       # Sample data generator
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── TECHNICAL_SPECIFICATION.md  # Technical documentation
├── IMPLEMENTATION_PLAN.md      # Implementation roadmap
├── PROJECT_SUMMARY.md          # Project overview
├── DEPLOYMENT_GUIDE.md         # Deployment instructions
├── sample_*.xlsx              # Sample data files
└── tests/                     # Test suite
```

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📊 Business Value

### Performance Monitoring
- **Real-time Insights**: Immediate visibility into technician performance
- **Trend Analysis**: Identify performance patterns over time
- **Benchmarking**: Compare technician performance against standards
- **Goal Setting**: Data-driven performance targets

### Operational Efficiency
- **Automated Reporting**: Eliminates manual data compilation
- **Standardized Metrics**: Consistent KPI calculations across organization
- **Quick Decision Making**: Rapid access to performance data
- **Resource Optimization**: Identify areas for improvement

### Revenue Optimization
- **Revenue Tracking**: Monitor revenue generation by technician
- **Service Sales Analysis**: Track specific service line performance
- **Membership Conversion**: Monitor sales effectiveness
- **Efficiency Improvements**: Optimize job completion rates

## 🎯 Success Metrics

### Technical Metrics
- **System Uptime**: > 99.5%
- **Response Time**: < 3 seconds for data processing
- **Error Rate**: < 1% of user sessions
- **Data Accuracy**: 100% KPI calculation accuracy

### Business Metrics
- **User Adoption**: 80% of technician managers actively using
- **Performance Improvement**: 10% improvement in technician KPIs
- **Decision Making Speed**: 50% reduction in reporting time
- **ROI**: Positive return within 6 months

## 🆘 Support

### Documentation
- **[Technical Specification](TECHNICAL_SPECIFICATION.md)** - Complete technical details
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Deployment and troubleshooting
- **[Implementation Plan](IMPLEMENTATION_PLAN.md)** - Implementation roadmap

### Contact
- **Technical Support**: tech-support@omahadrain.com
- **User Training**: training@omahadrain.com
- **Emergency Contact**: emergency-support@omahadrain.com

### Issues
If you encounter any issues, please:
1. Check the [Deployment Guide](DEPLOYMENT_GUIDE.md) for troubleshooting
2. Search existing [GitHub Issues](https://github.com/raadchfat/OmahaDrain_KPIs/issues)
3. Create a new issue with detailed information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for rapid web application development
- Data processing powered by [Pandas](https://pandas.pydata.org/)
- Visualizations created with [Plotly](https://plotly.com/)
- Excel file handling with [OpenPyXL](https://openpyxl.readthedocs.io/)

---

**Project Status**: Production Ready  
**Last Updated**: December 2024  
**Version**: 1.0  
**Maintainer**: Technical Development Team

⭐ **Star this repository if you find it helpful!**
