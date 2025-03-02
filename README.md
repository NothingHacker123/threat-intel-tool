# Threat Intelligence Tool 🛡️

## Overview
Ye tool AlienVault OTX API ka use karke threat data fetch karta hai, analyze karta hai, aur ek interactive dashboard mein display karta hai.

## Features
- Threat data fetch karna.
- Data analyze karna aur threat scores assign karna.
- Interactive Streamlit dashboard.
- Data export (CSV, JSON).
- Machine learning predictions.

## Requirements 📋

### Software Requirements
1. **Python 3.7+**: Ye tool Python 3.7 ya usse naye version par run hota hai.
   - Check karne ke liye:
     ```bash
     python --version
     ```
   - Agar Python installed nahi hai, toh [Python official website](https://www.python.org/downloads/) se download karein.

2. **Git**: Repository ko clone karne ke liye Git installed hona chahiye.
   - Check karne ke liye:
     ```bash
     git --version
     ```
   - Agar Git installed nahi hai, toh [Git official website](https://git-scm.com/downloads) se download karein.

3. **AlienVault OTX API Key**: Threat data fetch karne ke liye AlienVault OTX API key chahiye.
   - API key generate karne ke liye [AlienVault OTX](https://otx.alienvault.com/api/) par sign up karein aur API key generate karein.
   - API key ko `threat_intel_tool.py` file mein add karein:
     ```python
     API_KEY = 'your_api_key_here'
     ```

### Python Dependencies
Ye tool chalane ke liye kuch Python packages ki zarurat hai. Ye packages `requirements.txt` file mein listed hain. Inhe install karne ke liye ye command run karein:
```bash
pip install -r requirements.txt

