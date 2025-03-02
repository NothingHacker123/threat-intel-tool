# Step 1: Import Libraries
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
import ast
import psutil  # For system monitoring

# Step 2: Add OTX API Key Directly (Not Recommended for Production)
API_KEY = "3301e65c7d00e16e07ed4b8259a8c72e498e3e4b467c3a88e2f58dca3e0d8104"

# Step 3: Fetch Data from AlienVault OTX
def fetch_threat_data(api_key):
    url = 'https://otx.alienvault.com/api/v1/pulses/subscribed'
    headers = {'X-OTX-API-KEY': api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if not data['results']:  # If data is empty, fetch popular pulses
            url = 'https://otx.alienvault.com/api/v1/pulses/popular'
            response = requests.get(url, headers=headers)
            data = response.json()
        return data
    else:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")
        return {'results': []}

# Step 4: Analyze Data and Add Threat Scores
def analyze_data(data):
    df = pd.DataFrame(data['results'])
    df['threat_score'] = df['indicators'].apply(lambda x: 'High' if len(x) > 10 else 'Medium' if len(x) > 5 else 'Low')
    return df

# Step 5: Convert Lists to Strings
def convert_lists_to_strings(df):
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():  # Check if column contains lists
            df[col] = df[col].apply(lambda x: ', '.join(str(i) for i in x) if isinstance(x, list) else x)
    return df

# Step 6: System Monitoring Function
def system_monitor():
    st.header("System Monitoring 🖥️")
    
    # CPU Usage
    cpu_usage = psutil.cpu_percent()
    st.write(f"CPU Usage: {cpu_usage}%")
    
    # RAM Usage
    ram_usage = psutil.virtual_memory().percent
    st.write(f"RAM Usage: {ram_usage}%")
    
    # Disk Usage
    disk_usage = psutil.disk_usage('/').percent
    st.write(f"Disk Usage: {disk_usage}%")
    
    # Network Activity
    network_stats = psutil.net_io_counters()
    st.write(f"Bytes Sent: {network_stats.bytes_sent}")
    st.write(f"Bytes Received: {network_stats.bytes_recv}")

# Step 7: Safely Convert Strings to Python Objects
def safe_literal_eval(x):
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)
        except (ValueError, SyntaxError):
            return x  # Return the original value if parsing fails
    return x  # Return the original value if it's not a string

# Step 8: Enhance Threat Map with Real Geolocation Data
def enhance_threat_map(df):
    # Extract IP addresses from indicators
    ip_addresses = df['indicators'].apply(
        lambda x: [i['indicator'] for i in x if i['type'] == 'IPv4']
    ).explode().dropna()

    # Get geolocation for IP addresses (using a free API like ipinfo.io)
    latitudes, longitudes = [], []
    for ip in ip_addresses:
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            data = response.json()
            loc = data.get('loc', '').split(',')
            if len(loc) == 2:
                latitudes.append(float(loc[0]))
                longitudes.append(float(loc[1]))
        except Exception as e:
            st.warning(f"Failed to fetch geolocation for IP: {ip}")

    # If no IP addresses found, use default values
    if not latitudes or not longitudes:
        st.warning("No valid IP addresses found for geolocation.")
        latitudes = [0.0] * len(df)  # Default latitude
        longitudes = [0.0] * len(df)  # Default longitude

    # Add geolocation data to DataFrame
    df['latitude'] = latitudes[:len(df)]
    df['longitude'] = longitudes[:len(df)]

    # Plot the map
    fig = px.scatter_geo(df, lat='latitude', lon='longitude', hover_name='name', size_max=10)
    st.plotly_chart(fig)

# Step 9: Streamlit Dashboard
def main():
    st.title('Advanced Threat Intelligence + System Monitor 🛡️🖥️')
    st.write('Fetching and analyzing threat data...')

    # Fetch data
    data = fetch_threat_data(API_KEY)
    df = analyze_data(data)

    # Convert lists to strings
    df = convert_lists_to_strings(df)

    # Safely convert indicators column to Python objects
    df['indicators'] = df['indicators'].apply(safe_literal_eval)

    # Feature Engineering for Machine Learning
    df['indicator_count'] = df['indicators'].apply(lambda x: len(x) if isinstance(x, list) else 1)
    df['has_bitcoin'] = df['indicators'].apply(lambda x: 1 if any(i.get('type') == 'BitcoinAddress' for i in x) else 0)
    df['has_ip'] = df['indicators'].apply(lambda x: 1 if any(i.get('type') == 'IPv4' for i in x) else 0)
    df['has_url'] = df['indicators'].apply(lambda x: 1 if any(i.get('type') == 'URL' for i in x) else 0)

    # Show data in dashboard
    st.write('Threat Data:')
    st.dataframe(df)

    # Show threat score distribution
    st.write('Threat Score Distribution:')
    threat_counts = df['threat_score'].value_counts()
    st.bar_chart(threat_counts)

    # Pie chart for threat scores
    st.write('Threat Score Distribution (Pie Chart):')
    fig, ax = plt.subplots()
    ax.pie(threat_counts, labels=threat_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

    # Search bar for threats
    search_query = st.text_input('Search Threats by Name:')
    if search_query:
        filtered_df = df[df['name'].str.contains(search_query, case=False)]
        st.write('Filtered Threat Data:')
        st.dataframe(filtered_df)

    # Show threat details
    st.write('Threat Details:')
    for index, row in df.iterrows():
        st.write(f"**Name**: {row['name']}")
        st.write(f"**Description**: {row['description']}")
        st.write(f"**Indicators**: {row['indicators']}")
        st.write("---")

    # Save data to CSV
    st.write('Save Data to CSV:')
    if st.button('Save as CSV'):
        df.to_csv('threat_data.csv', index=False)
        st.success('Data saved to threat_data.csv!')

    # Load data from CSV
    st.write('Load Data from CSV:')
    if st.button('Load from CSV'):
        try:
            df = pd.read_csv('threat_data.csv')
            st.write('Loaded Threat Data:')
            st.dataframe(df)
        except Exception as e:
            st.error(f"Failed to load data: {e}")

    # Save data to JSON
    st.write('Save Data to JSON:')
    if st.button('Save as JSON'):
        df.to_json('threat_data.json', orient='records')
        st.success('Data saved to threat_data.json!')

    # Load data from JSON
    st.write('Load Data from JSON:')
    if st.button('Load from JSON'):
        try:
            df = pd.read_json('threat_data.json')
            st.write('Loaded Threat Data:')
            st.dataframe(df)
        except Exception as e:
            st.error(f"Failed to load data: {e}")

    # Threat Map (Geolocation)
    st.write('Threat Map:')
    enhance_threat_map(df)  # Use real geolocation data

    # Threat Trends Over Time
    st.write('Threat Trends Over Time:')
    df['created'] = pd.to_datetime(df['created'])
    df.set_index('created', inplace=True)
    st.line_chart(df['threat_score'].value_counts())

    # Threat Indicators Analysis
    st.write('Threat Indicators Analysis:')
    indicators_df = df.explode('indicators')
    st.write('Top 10 Indicators:')
    top_indicators = indicators_df['indicators'].value_counts().head(10)
    st.bar_chart(top_indicators)

    # Export Data
    st.write('Export Data:')
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button('Download CSV', data=csv, file_name='threat_data.csv', mime='text/csv')

    # Machine Learning Integration
    st.write('Threat Prediction:')
    try:
        # Features and Target
        X = df[['indicator_count', 'has_bitcoin', 'has_ip', 'has_url']]  # Numeric features
        y = df['threat_score'].apply(lambda x: 2 if x == 'High' else 1 if x == 'Medium' else 0)  # Convert to numeric

        # Train model
        model = RandomForestClassifier()
        model.fit(X, y)
        st.write('Model trained successfully!')
    except Exception as e:
        st.error(f"Failed to train model: {e}")

    # Real-Time Alerts
    if 'High' in df['threat_score'].values:
        st.toast(f"🚨 High threat detected: {df[df['threat_score'] == 'High']['name'].values[0]}", icon='⚠️')

    # System Monitoring Section
    system_monitor()

# Run the Streamlit app
if __name__ == '__main__':
    main()
