How to Use
Getting Started
1. Clone and Install Dependencies
This project is optimized for the Debian environment. First, ensure you have Python 3 installed, then install the required libraries:
Bash pip install garminconnect fitparse streamlit pandas plotly
2. Configuration
Before running the sync, you must provide your Garmin credentials. Open sync_data.py and fill in your account information:Python
# Open sync_data.py
G_USER = "your_email@example.com"
G_PASS = "your_password"
3. Data Synchronization
Run the sync script to fetch your latest activities:
Bash python3 sync_data.py
4. Launch the Dashboard
Start the Streamlit application to view your data:
Bash streamlit run gym_app.py
