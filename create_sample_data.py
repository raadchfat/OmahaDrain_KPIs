import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducible data
np.random.seed(42)

# Generate sample data
technicians = ['John Smith', 'Mike Johnson', 'Sarah Wilson', 'David Brown']
services = ['Hydro Jetting', 'Descaling', 'Water Heater', 'Drain Cleaning', 'Pipe Repair']
membership_types = ['Basic', 'Premium', 'Gold', None]

# Generate dates for the last 4 weeks
end_date = datetime.now()
start_date = end_date - timedelta(weeks=4)
dates = pd.date_range(start=start_date, end=end_date, freq='D')

# 1. Job Data
job_data = []
for date in dates:
    for tech in technicians:
        num_jobs = np.random.randint(2, 8)
        for i in range(num_jobs):
            job_data.append({
                'Technician': tech,
                'Job_ID': f'JOB-{date.strftime("%Y%m%d")}-{i+1:03d}',
                'Status': np.random.choice(['Completed', 'Assigned', 'In Progress'], p=[0.8, 0.15, 0.05]),
                'Date': date,
                'Hours': np.random.uniform(1, 6)
            })

job_df = pd.DataFrame(job_data)

# 2. Revenue Data
revenue_data = []
for _, job in job_df.iterrows():
    if job['Status'] == 'Completed':
        revenue_data.append({
            'Technician': job['Technician'],
            'Job_ID': job['Job_ID'],
            'Revenue': np.random.uniform(100, 500),
            'Date': job['Date']
        })

revenue_df = pd.DataFrame(revenue_data)

# 3. Membership Data
membership_data = []
for date in dates:
    for tech in technicians:
        num_opportunities = np.random.randint(1, 5)
        for i in range(num_opportunities):
            membership_data.append({
                'Technician': tech,
                'Customer_ID': f'CUST-{date.strftime("%Y%m%d")}-{i+1:03d}',
                'Membership_Type': np.random.choice(membership_types, p=[0.3, 0.2, 0.1, 0.4]),
                'Date': date
            })

membership_df = pd.DataFrame(membership_data)

# 4. Service Sales Data
service_data = []
for date in dates:
    for tech in technicians:
        num_services = np.random.randint(1, 4)
        for i in range(num_services):
            service_data.append({
                'Technician': tech,
                'Service_Type': np.random.choice(['Hydro Jetting', 'Descaling', 'Water Heater']),
                'Date': date,
                'Revenue': np.random.uniform(150, 800)
            })

service_df = pd.DataFrame(service_data)

# Save to Excel files
job_df.to_excel('sample_job_data.xlsx', index=False)
revenue_df.to_excel('sample_revenue_data.xlsx', index=False)
membership_df.to_excel('sample_membership_data.xlsx', index=False)
service_df.to_excel('sample_service_data.xlsx', index=False)

print("Sample data files created successfully!")
print("Files created:")
print("- sample_job_data.xlsx")
print("- sample_revenue_data.xlsx")
print("- sample_membership_data.xlsx")
print("- sample_service_data.xlsx")
