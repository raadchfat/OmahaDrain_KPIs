import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from kpi_calculator import KPICalculator

# Page configuration
st.set_page_config(
    page_title="Omaha Drain Technician KPI Dashboard",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .upload-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px dashed #cccccc;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">�� Omaha Drain Technician KPI Dashboard</h1>', unsafe_allow_html=True)

# Initialize KPI calculator
kpi_calc = KPICalculator()

# Sidebar for configuration
with st.sidebar:
    st.header("📊 Dashboard Configuration")
    
    # Week selection
    st.subheader("📅 Select Reporting Week")
    current_date = datetime.now()
    week_start = st.date_input(
        "Week Start Date",
        value=current_date - timedelta(days=current_date.weekday()),
        help="Select the start of the reporting week"
    )
    
    # Set week period for KPI calculator
    kpi_calc.set_week_period(week_start)
    
    # Technician filter
    st.subheader("👷 Technician Filter")
    show_all_technicians = st.checkbox("Show All Technicians", value=True)
    
    st.markdown("---")
    st.markdown("### 📋 KPI Definitions")
    st.markdown("""
    - **Average Ticket Value**: Total revenue ÷ completed jobs
    - **Job Close Rate**: Completed jobs ÷ assigned jobs × 100%
    - **Weekly Revenue**: Total revenue for the week
    - **Job Efficiency**: Jobs completed per hour
    - **Membership Win Rate**: Memberships sold ÷ opportunities × 100%
    - **Service Sales**: Count of specific services sold
    """)

# File upload section
st.header("📁 Data Upload")
st.markdown("Upload the 4 required Excel files for KPI calculation:")

# Create columns for file uploads
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Job Data")
    job_data_file = st.file_uploader(
        "Upload Job Data (jobs completed/assigned)",
        type=['xlsx', 'xls'],
        help="Should contain: Technician, Job ID, Status, Date, Hours"
    )
    
    st.subheader("💰 Revenue Data")
    revenue_data_file = st.file_uploader(
        "Upload Revenue Data (ticket values)",
        type=['xlsx', 'xls'],
        help="Should contain: Technician, Job ID, Revenue, Date"
    )

with col2:
    st.subheader("🎯 Membership Data")
    membership_data_file = st.file_uploader(
        "Upload Membership Sales Data",
        type=['xlsx', 'xls'],
        help="Should contain: Technician, Customer, Membership Type, Date"
    )
    
    st.subheader("🔧 Service Sales Data")
    service_data_file = st.file_uploader(
        "Upload Service Sales Data (Hydro Jetting, Descaling, Water Heater)",
        type=['xlsx', 'xls'],
        help="Should contain: Technician, Service Type, Date, Revenue"
    )

# Data processing and KPI calculation
@st.cache_data
def load_and_process_data(job_file, revenue_file, membership_file, service_file):
    """Load and process all uploaded files"""
    data = {}
    
    try:
        if job_file:
            data['jobs'] = pd.read_excel(job_file)
            st.success(f"✅ Job data loaded: {len(data['jobs'])} records")
        if revenue_file:
            data['revenue'] = pd.read_excel(revenue_file)
            st.success(f"✅ Revenue data loaded: {len(data['revenue'])} records")
        if membership_file:
            data['membership'] = pd.read_excel(membership_file)
            st.success(f"✅ Membership data loaded: {len(data['membership'])} records")
        if service_file:
            data['services'] = pd.read_excel(service_file)
            st.success(f"✅ Service data loaded: {len(data['services'])} records")
            
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None
    
    return data

# Main dashboard logic
if all([job_data_file, revenue_data_file, membership_data_file, service_data_file]):
    st.success("🎉 All files uploaded successfully!")
    
    # Load and process data
    with st.spinner("Processing data..."):
        data = load_and_process_data(job_data_file, revenue_data_file, membership_data_file, service_data_file)
    
    if data:
        # Calculate KPIs using the KPI calculator
        kpis_df = kpi_calc.calculate_all_kpis(data)
        
        if kpis_df is not None and not kpis_df.empty:
            st.header("📈 KPI Dashboard")
            
            # Filter technicians if needed
            if not show_all_technicians:
                selected_tech = st.selectbox("Select Technician", kpis_df['Technician'].unique())
                kpis_df = kpis_df[kpis_df['Technician'] == selected_tech]
            
            # Display KPIs in cards
            st.subheader("🎯 Key Performance Indicators")
            
            # Create metric cards
            cols = st.columns(4)
            
            with cols[0]:
                st.metric(
                    label="Average Ticket Value",
                    value=f"${kpis_df['avg_ticket_value'].mean():.0f}",
                    delta=f"{kpis_df['avg_ticket_value'].std():.1f}"
                )
            
            with cols[1]:
                st.metric(
                    label="Job Close Rate",
                    value=f"{kpis_df['job_close_rate'].mean():.1f}%",
                    delta=f"{kpis_df['job_close_rate'].std():.1f}%"
                )
            
            with cols[2]:
                st.metric(
                    label="Weekly Revenue",
                    value=f"${kpis_df['weekly_revenue'].sum():,.0f}",
                    delta=f"{kpis_df['weekly_revenue'].mean():.0f}"
                )
            
            with cols[3]:
                st.metric(
                    label="Job Efficiency",
                    value=f"{kpis_df['job_efficiency'].mean():.1f}",
                    delta=f"{kpis_df['job_efficiency'].std():.1f}"
                )
            
            # Additional metrics
            st.subheader("📊 Additional Metrics")
            cols2 = st.columns(4)
            
            with cols2[0]:
                st.metric(
                    label="Membership Win Rate",
                    value=f"{kpis_df['membership_win_rate'].mean():.1f}%",
                    delta=f"{kpis_df['membership_win_rate'].std():.1f}%"
                )
            
            with cols2[1]:
                st.metric(
                    label="Hydro Jetting Sold",
                    value=f"{kpis_df['hydro_jetting_sold'].sum():.0f}",
                    delta=f"{kpis_df['hydro_jetting_sold'].mean():.1f}"
                )
            
            with cols2[2]:
                st.metric(
                    label="Descaling Sold",
                    value=f"{kpis_df['descaling_sold'].sum():.0f}",
                    delta=f"{kpis_df['descaling_sold'].mean():.1f}"
                )
            
            with cols2[3]:
                st.metric(
                    label="Water Heater Sold",
                    value=f"{kpis_df['water_heater_sold'].sum():.0f}",
                    delta=f"{kpis_df['water_heater_sold'].mean():.1f}"
                )
            
            # Detailed KPI table
            st.subheader("📊 Detailed KPI Breakdown")
            st.dataframe(kpis_df, use_container_width=True)
            
            # Visualizations
            st.subheader("📈 Performance Visualizations")
            
            # Service sales chart
            fig_services = px.bar(
                kpis_df,
                x='Technician',
                y=['hydro_jetting_sold', 'descaling_sold', 'water_heater_sold'],
                title="Service Sales by Technician",
                barmode='group'
            )
            st.plotly_chart(fig_services, use_container_width=True)
            
            # Revenue vs Efficiency scatter
            fig_scatter = px.scatter(
                kpis_df,
                x='job_efficiency',
                y='weekly_revenue',
                size='avg_ticket_value',
                color='Technician',
                title="Revenue vs Efficiency Analysis",
                hover_data=['job_close_rate']
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # KPI radar chart
            if len(kpis_df) > 0:
                # Normalize values for radar chart
                radar_data = kpis_df.copy()
                for col in ['avg_ticket_value', 'job_close_rate', 'weekly_revenue', 'job_efficiency', 'membership_win_rate']:
                    if radar_data[col].max() > 0:
                        radar_data[col] = (radar_data[col] - radar_data[col].min()) / (radar_data[col].max() - radar_data[col].min()) * 100
                
                fig_radar = go.Figure()
                
                for _, tech in radar_data.iterrows():
                    fig_radar.add_trace(go.Scatterpolar(
                        r=[tech['avg_ticket_value'], tech['job_close_rate'], tech['job_efficiency'], tech['membership_win_rate']],
                        theta=['Avg Ticket', 'Close Rate', 'Efficiency', 'Membership'],
                        fill='toself',
                        name=tech['Technician']
                    ))
                
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    showlegend=True,
                    title="Technician Performance Comparison"
                )
                
                st.plotly_chart(fig_radar, use_container_width=True)
            
        else:
            st.error("❌ Unable to calculate KPIs. Please check your data format and ensure all required columns are present.")
            st.info("💡 Make sure your Excel files contain the expected column names and data formats.")
    
else:
    st.info("📋 Please upload all 4 Excel files to view the KPI dashboard.")
    
    # Show sample data structure
    with st.expander("📋 Expected Data Structure"):
        st.markdown("""
        **Job Data Columns:**
        - Technician Name
        - Job ID
        - Status (Completed/Assigned)
        - Date
        - Hours Worked
        
        **Revenue Data Columns:**
        - Technician Name
        - Job ID
        - Revenue Amount
        - Date
        
        **Membership Data Columns:**
        - Technician Name
        - Customer ID
        - Membership Type
        - Date
        
        **Service Sales Data Columns:**
        - Technician Name
        - Service Type (Hydro Jetting/Descaling/Water Heater)
        - Date
        - Revenue
        """)

# Footer
st.markdown("---")
st.markdown("*Omaha Drain KPI Dashboard - Business Intelligence Solution*")
