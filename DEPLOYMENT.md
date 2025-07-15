# Omaha Drain KPI Dashboard - Deployment Guide

## Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd /Users/raadchfat/omaha-drain-kpi-dashboard
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Run the dashboard:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser and go to:**
   ```
   http://localhost:8501
   ```

## Production Deployment

### Option 1: Local Production Server
```bash
# Install production dependencies
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8501 streamlit.web.cli:main -- --server.port 8501 --server.address 0.0.0.0
```

### Option 2: Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Option 3: Cloud Deployment (AWS, GCP, Azure)
1. Upload the project files to your cloud platform
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

## Data Requirements

### Excel File Formats

**Job Data (sample_job_data.xlsx):**
- Technician: Name of the technician
- Job_ID: Unique job identifier
- Status: "Completed", "Assigned", or "In Progress"
- Date: Date of the job
- Hours: Hours worked on the job

**Revenue Data (sample_revenue_data.xlsx):**
- Technician: Name of the technician
- Job_ID: Unique job identifier
- Revenue: Dollar amount
- Date: Date of the revenue

**Membership Data (sample_membership_data.xlsx):**
- Technician: Name of the technician
- Customer_ID: Unique customer identifier
- Membership_Type: "Basic", "Premium", "Gold", or null
- Date: Date of the membership opportunity

**Service Sales Data (sample_service_data.xlsx):**
- Technician: Name of the technician
- Service_Type: "Hydro Jetting", "Descaling", or "Water Heater"
- Date: Date of the service
- Revenue: Dollar amount

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Kill existing process
   lsof -ti:8501 | xargs kill -9
   ```

2. **Permission denied:**
   ```bash
   # Make sure you have write permissions
   chmod -R 755 /Users/raadchfat/omaha-drain-kpi-dashboard
   ```

3. **Missing dependencies:**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

4. **Excel file format issues:**
   - Ensure column names match exactly
   - Check for extra spaces in column names
   - Verify date formats are consistent

### Performance Optimization

1. **Large datasets:**
   - Use data caching: `@st.cache_data`
   - Implement pagination for large tables
   - Consider database integration for >100k records

2. **Memory usage:**
   - Process data in chunks
   - Use efficient data types (e.g., category for strings)
   - Clear cache periodically

## Security Considerations

1. **File upload security:**
   - Validate file types and sizes
   - Scan for malicious content
   - Implement user authentication

2. **Data privacy:**
   - Encrypt sensitive data
   - Implement access controls
   - Regular security audits

## Monitoring and Maintenance

1. **Log monitoring:**
   ```bash
   # View Streamlit logs
   tail -f ~/.streamlit/logs/streamlit.log
   ```

2. **Performance monitoring:**
   - Monitor response times
   - Track memory usage
   - Set up alerts for errors

3. **Regular updates:**
   ```bash
   # Update dependencies
   pip install --upgrade -r requirements.txt
   ```

## Support

For technical support or questions:
- Check the README.md file
- Review the deployment logs
- Contact the BI development team
