How to Use
1. Clone & Install Dependencies
This project is optimized for Debian environments. Ensure you have Python 3.9+ installed, then install the required libraries:
pip install garminconnect fitparse streamlit pandas plotly
2. Configuration
Before running the synchronization, provide your Garmin credentials in sync_data.py:
Open sync_data.py and edit the following lines:
G_USER = "your_email@example.com"
G_PASS = "your_password"
3. Data Synchronization
Run the sync script to fetch your latest activities and health metrics from Garmin Connect:
python3 sync_data.py
4. Launch the Dashboard
Start the Streamlit application to visualize your data:
streamlit run gym_app.py
