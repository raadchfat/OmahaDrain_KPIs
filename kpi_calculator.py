import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

class KPICalculator:
    """Calculate KPIs for Omaha Drain technicians"""
    
    def __init__(self):
        self.week_start = None
        self.week_end = None
    
    def set_week_period(self, week_start):
        """Set the week period for calculations"""
        self.week_start = pd.to_datetime(week_start)
        self.week_end = self.week_start + timedelta(days=6)
    
    def filter_week_data(self, df, date_column):
        """Filter data for the specified week"""
        if date_column not in df.columns:
            st.error(f"Date column '{date_column}' not found in data")
            return df
        
        df[date_column] = pd.to_datetime(df[date_column])
        mask = (df[date_column] >= self.week_start) & (df[date_column] <= self.week_end)
        return df[mask]
    
    def calculate_average_ticket_value(self, revenue_data, job_data):
        """Calculate average ticket value per technician"""
        if revenue_data is None or job_data is None:
            return pd.DataFrame()
        
        # Filter for completed jobs only
        completed_jobs = job_data[job_data['Status'].str.contains('Completed', case=False, na=False)]
        
        # Group by technician and calculate average
        avg_ticket = revenue_data.groupby('Technician')['Revenue'].mean().reset_index()
        avg_ticket.columns = ['Technician', 'Average_Ticket_Value']
        
        return avg_ticket
    
    def calculate_job_close_rate(self, job_data):
        """Calculate job close rate per technician"""
        if job_data is None:
            return pd.DataFrame()
        
        # Count total jobs and completed jobs per technician
        total_jobs = job_data.groupby('Technician').size().reset_index(name='Total_Jobs')
        completed_jobs = job_data[job_data['Status'].str.contains('Completed', case=False, na=False)]
        completed_count = completed_jobs.groupby('Technician').size().reset_index(name='Completed_Jobs')
        
        # Merge and calculate rate
        close_rate = total_jobs.merge(completed_count, on='Technician', how='left').fillna(0)
        close_rate['Job_Close_Rate'] = (close_rate['Completed_Jobs'] / close_rate['Total_Jobs'] * 100).round(1)
        
        return close_rate[['Technician', 'Job_Close_Rate']]
    
    def calculate_weekly_revenue(self, revenue_data):
        """Calculate total weekly revenue per technician"""
        if revenue_data is None:
            return pd.DataFrame()
        
        weekly_revenue = revenue_data.groupby('Technician')['Revenue'].sum().reset_index()
        weekly_revenue.columns = ['Technician', 'Weekly_Revenue']
        
        return weekly_revenue
    
    def calculate_job_efficiency(self, job_data):
        """Calculate job efficiency (jobs per hour) per technician"""
        if job_data is None:
            return pd.DataFrame()
        
        # Filter for completed jobs with hours data
        completed_jobs = job_data[
            (job_data['Status'].str.contains('Completed', case=False, na=False)) &
            (job_data['Hours'].notna())
        ]
        
        if completed_jobs.empty:
            return pd.DataFrame()
        
        # Calculate efficiency
        efficiency = completed_jobs.groupby('Technician').agg({
            'Job_ID': 'count',
            'Hours': 'sum'
        }).reset_index()
        
        efficiency['Job_Efficiency'] = (efficiency['Job_ID'] / efficiency['Hours']).round(2)
        efficiency.columns = ['Technician', 'Jobs_Completed', 'Total_Hours', 'Job_Efficiency']
        
        return efficiency[['Technician', 'Job_Efficiency']]
    
    def calculate_membership_win_rate(self, membership_data):
        """Calculate membership win rate per technician"""
        if membership_data is None:
            return pd.DataFrame()
        
        # Count total opportunities and wins per technician
        total_opportunities = membership_data.groupby('Technician').size().reset_index(name='Total_Opportunities')
        wins = membership_data[membership_data['Membership_Type'].notna()]
        win_count = wins.groupby('Technician').size().reset_index(name='Memberships_Won')
        
        # Merge and calculate rate
        win_rate = total_opportunities.merge(win_count, on='Technician', how='left').fillna(0)
        win_rate['Membership_Win_Rate'] = (win_rate['Memberships_Won'] / win_rate['Total_Opportunities'] * 100).round(1)
        
        return win_rate[['Technician', 'Membership_Win_Rate']]
    
    def calculate_service_sales(self, service_data):
        """Calculate service sales counts per technician"""
        if service_data is None:
            return pd.DataFrame()
        
        # Count each service type
        service_counts = service_data.groupby(['Technician', 'Service_Type']).size().reset_index(name='Count')
        
        # Pivot to get each service as a column
        service_pivot = service_counts.pivot(index='Technician', columns='Service_Type', values='Count').fillna(0)
        service_pivot = service_pivot.reset_index()
        
        # Ensure all expected service types exist
        expected_services = ['Hydro Jetting', 'Descaling', 'Water Heater']
        for service in expected_services:
            if service not in service_pivot.columns:
                service_pivot[service] = 0
        
        return service_pivot
    
    def calculate_all_kpis(self, data):
        """Calculate all KPIs and return comprehensive results"""
        if not data:
            return None
        
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
        
        # Get all unique technicians
        all_technicians = set()
        for df in [avg_ticket, close_rate, weekly_revenue, efficiency, membership_rate, service_sales]:
            if not df.empty and 'Technician' in df.columns:
                all_technicians.update(df['Technician'].unique())
        
        if not all_technicians:
            return None
        
        # Create comprehensive KPI dataframe
        kpi_data = []
        for tech in all_technicians:
            tech_data = {'Technician': tech}
            
            # Average Ticket Value
            tech_avg = avg_ticket[avg_ticket['Technician'] == tech]
            tech_data['avg_ticket_value'] = tech_avg['Average_Ticket_Value'].iloc[0] if not tech_avg.empty else 0
            
            # Job Close Rate
            tech_close = close_rate[close_rate['Technician'] == tech]
            tech_data['job_close_rate'] = tech_close['Job_Close_Rate'].iloc[0] if not tech_close.empty else 0
            
            # Weekly Revenue
            tech_revenue = weekly_revenue[weekly_revenue['Technician'] == tech]
            tech_data['weekly_revenue'] = tech_revenue['Weekly_Revenue'].iloc[0] if not tech_revenue.empty else 0
            
            # Job Efficiency
            tech_efficiency = efficiency[efficiency['Technician'] == tech]
            tech_data['job_efficiency'] = tech_efficiency['Job_Efficiency'].iloc[0] if not tech_efficiency.empty else 0
            
            # Membership Win Rate
            tech_membership = membership_rate[membership_rate['Technician'] == tech]
            tech_data['membership_win_rate'] = tech_membership['Membership_Win_Rate'].iloc[0] if not tech_membership.empty else 0
            
            # Service Sales
            tech_services = service_sales[service_sales['Technician'] == tech]
            tech_data['hydro_jetting_sold'] = tech_services['Hydro Jetting'].iloc[0] if not tech_services.empty else 0
            tech_data['descaling_sold'] = tech_services['Descaling'].iloc[0] if not tech_services.empty else 0
            tech_data['water_heater_sold'] = tech_services['Water Heater'].iloc[0] if not tech_services.empty else 0
            
            kpi_data.append(tech_data)
        
        return pd.DataFrame(kpi_data)
