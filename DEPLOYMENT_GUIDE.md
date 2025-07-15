# Omaha Drain KPI Dashboard - Deployment Guide

## Quick Start

### Local Development Deployment

#### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)

#### Step 1: Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd omaha-drain-kpi-dashboard

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: Run the Dashboard
```bash
# Start the dashboard
streamlit run app.py

# Or run in headless mode
streamlit run app.py --server.headless true --server.port 8501
```

#### Step 3: Access the Dashboard
- Open your web browser
- Navigate to: `http://localhost:8501`
- Upload the 4 sample Excel files
- Configure week selection and view KPIs

### Production Deployment

#### Option 1: Streamlit Cloud (Recommended)

##### Step 1: Prepare Repository
```bash
# Ensure all files are committed
git add .
git commit -m "Production ready dashboard"
git push origin main
```

##### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `app.py`
6. Click "Deploy"

##### Step 3: Configure Environment
- Set environment variables in Streamlit Cloud dashboard
- Configure secrets for production settings
- Set up custom domain if needed

#### Option 2: Docker Deployment

##### Step 1: Build Docker Image
```bash
# Build the image
docker build -t omaha-drain-kpi-dashboard .

# Run the container
docker run -p 8501:8501 omaha-drain-kpi-dashboard
```

##### Step 2: Docker Compose (Recommended)
```bash
# Start with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

#### Option 3: Cloud Platform Deployment

##### AWS Deployment
```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure

# Deploy using AWS Elastic Beanstalk
eb init omaha-drain-kpi-dashboard
eb create production
eb deploy
```

##### Google Cloud Platform
```bash
# Install Google Cloud SDK
# Deploy to App Engine
gcloud app deploy app.yaml
```

##### Azure Deployment
```bash
# Install Azure CLI
# Deploy to Azure App Service
az webapp up --name omaha-drain-kpi-dashboard --resource-group myResourceGroup
```

## Configuration

### Environment Variables

Create a `.env` file for local development:
```env
# Application settings
DEBUG=False
SECRET_KEY=your-secret-key-here

# File upload settings
MAX_FILE_SIZE=52428800
ALLOWED_EXTENSIONS=.xlsx,.xls

# Data processing settings
CACHE_TTL=3600

# Database settings (if using database)
DATABASE_URL=sqlite:///kpi_dashboard.db
```

### Production Configuration

#### Streamlit Configuration
Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

#### Security Settings
```python
# Add to app.py
import os
from dotenv import load_dotenv

load_dotenv()

# Security headers
st.set_page_config(
    page_title="Omaha Drain Technician KPI Dashboard",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File upload security
def validate_file_upload(file):
    """Validate uploaded file"""
    if file is None:
        return False
    
    # Check file size
    if file.size > int(os.getenv('MAX_FILE_SIZE', 52428800)):
        st.error("File too large. Maximum size is 50MB.")
        return False
    
    # Check file extension
    allowed_extensions = os.getenv('ALLOWED_EXTENSIONS', '.xlsx,.xls').split(',')
    file_extension = os.path.splitext(file.name)[1].lower()
    
    if file_extension not in allowed_extensions:
        st.error(f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}")
        return False
    
    return True
```

## Monitoring and Maintenance

### Health Checks

#### Application Health Check
```python
# Add to app.py
@st.cache_data
def health_check():
    """Perform application health check"""
    try:
        # Test data processing
        test_data = pd.DataFrame({
            'Technician': ['Test'],
            'Job_ID': ['TEST-001'],
            'Status': ['Completed'],
            'Date': [pd.Timestamp.now()],
            'Hours': [1.0]
        })
        
        calculator = KPICalculator()
        result = calculator.calculate_job_close_rate(test_data)
        
        return {
            'status': 'healthy',
            'timestamp': pd.Timestamp.now(),
            'data_processing': 'ok',
            'kpi_calculations': 'ok'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'timestamp': pd.Timestamp.now(),
            'error': str(e)
        }

# Display health status in sidebar
with st.sidebar:
    health = health_check()
    if health['status'] == 'healthy':
        st.success("✅ System Healthy")
    else:
        st.error("❌ System Issues Detected")
```

#### Performance Monitoring
```python
# Add performance monitoring
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/dashboard.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def monitor_performance(func):
    """Decorator to monitor function performance"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.2f} seconds: {str(e)}")
            raise
    return wrapper
```

### Backup and Recovery

#### Data Backup Strategy
```python
# Add backup functionality
import shutil
from datetime import datetime

def backup_uploaded_files(uploaded_files):
    """Backup uploaded files"""
    backup_dir = f"backups/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    for file in uploaded_files:
        if file is not None:
            with open(f"{backup_dir}/{file.name}", "wb") as f:
                f.write(file.getbuffer())
    
    logger.info(f"Files backed up to {backup_dir}")

def cleanup_old_backups(days_to_keep=30):
    """Clean up old backup files"""
    backup_root = "backups"
    if os.path.exists(backup_root):
        current_time = datetime.now()
        for backup_dir in os.listdir(backup_root):
            backup_path = os.path.join(backup_root, backup_dir)
            backup_time = datetime.fromtimestamp(os.path.getctime(backup_path))
            
            if (current_time - backup_time).days > days_to_keep:
                shutil.rmtree(backup_path)
                logger.info(f"Removed old backup: {backup_path}")
```

## Troubleshooting

### Common Issues

#### Issue 1: Dashboard Won't Start
**Symptoms**: Streamlit fails to start or shows error
**Solutions**:
```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip list | grep streamlit

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check port availability
lsof -i :8501
```

#### Issue 2: File Upload Errors
**Symptoms**: Files won't upload or show validation errors
**Solutions**:
```python
# Check file format
if not file.name.endswith(('.xlsx', '.xls')):
    st.error("Please upload Excel files only")

# Check file size
if file.size > 50 * 1024 * 1024:  # 50MB
    st.error("File too large")

# Check required columns
required_columns = ['Technician', 'Job_ID', 'Status', 'Date', 'Hours']
missing_columns = set(required_columns) - set(df.columns)
if missing_columns:
    st.error(f"Missing columns: {missing_columns}")
```

#### Issue 3: KPI Calculation Errors
**Symptoms**: KPIs show incorrect values or errors
**Solutions**:
```python
# Check data types
print(df.dtypes)

# Check for null values
print(df.isnull().sum())

# Validate date format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
invalid_dates = df['Date'].isnull().sum()
if invalid_dates > 0:
    st.warning(f"Found {invalid_dates} invalid dates")
```

#### Issue 4: Performance Issues
**Symptoms**: Slow loading or processing
**Solutions**:
```python
# Enable caching
@st.cache_data
def load_data(file):
    return pd.read_excel(file)

# Optimize data processing
def optimize_dataframe(df):
    # Convert object columns to category for memory efficiency
    for col in df.select_dtypes(include=['object']):
        if df[col].nunique() / len(df) < 0.5:
            df[col] = df[col].astype('category')
    return df
```

### Log Analysis

#### View Application Logs
```bash
# View real-time logs
tail -f logs/dashboard.log

# Search for errors
grep "ERROR" logs/dashboard.log

# Search for performance issues
grep "executed in" logs/dashboard.log | sort -k5 -n
```

#### Performance Analysis
```python
# Add performance profiling
import cProfile
import pstats

def profile_function(func, *args, **kwargs):
    """Profile function performance"""
    profiler = cProfile.Profile()
    profiler.enable()
    result = func(*args, **kwargs)
    profiler.disable()
    
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
    
    return result
```

## Security Considerations

### Data Security
```python
# Implement data encryption
from cryptography.fernet import Fernet

def encrypt_sensitive_data(data):
    """Encrypt sensitive data"""
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data, key

def decrypt_sensitive_data(encrypted_data, key):
    """Decrypt sensitive data"""
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data.decode()
```

### Access Control
```python
# Implement basic authentication
import hashlib

def check_authentication(username, password):
    """Simple authentication check"""
    # In production, use proper authentication system
    valid_users = {
        'admin': hashlib.sha256('admin123'.encode()).hexdigest(),
        'manager': hashlib.sha256('manager123'.encode()).hexdigest()
    }
    
    if username in valid_users:
        return valid_users[username] == hashlib.sha256(password.encode()).hexdigest()
    return False

# Add to main app
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if check_authentication(username, password):
            st.session_state.authenticated = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")
    st.stop()
```

## Scaling Considerations

### Horizontal Scaling
```python
# Use Redis for session management
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def store_session_data(session_id, data):
    """Store session data in Redis"""
    redis_client.setex(session_id, 3600, json.dumps(data))

def get_session_data(session_id):
    """Retrieve session data from Redis"""
    data = redis_client.get(session_id)
    return json.loads(data) if data else None
```

### Load Balancing
```nginx
# Nginx configuration for load balancing
upstream streamlit_backend {
    server 127.0.0.1:8501;
    server 127.0.0.1:8502;
    server 127.0.0.1:8503;
}

server {
    listen 80;
    server_name dashboard.omahadrain.com;
    
    location / {
        proxy_pass http://streamlit_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Support and Maintenance

### Regular Maintenance Tasks

#### Daily Tasks
- Monitor application logs for errors
- Check system performance metrics
- Verify backup completion

#### Weekly Tasks
- Review performance analytics
- Update dependencies if needed
- Clean up old backup files

#### Monthly Tasks
- Security audit and updates
- Performance optimization review
- User feedback analysis

### Support Contact Information
- **Technical Support**: tech-support@omahadrain.com
- **User Training**: training@omahadrain.com
- **Emergency Contact**: emergency-support@omahadrain.com

---

**Deployment Status**: Ready for Production  
**Last Updated**: December 2024  
**Version**: 1.0  
**Maintainer**: Technical Development Team 