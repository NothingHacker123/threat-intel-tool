# Threat Intelligence Tool 🛡️

## Overview
This tool uses the AlienVault OTX API to fetch threat data, analyze it, and display the results on an interactive dashboard..

## Features
- Fetching threat data.
- Analyzing data and assigning threat scores.
- Interactive Streamlit dashboard.
- Data export (CSV, JSON).
- Machine learning predictions.

## Requirements 📋

### Software Requirements
1. **Python 3.7+**:  This tool runs on Python 3.7 or later versions..
   -  To Check:
     ```bash
     python --version
     ```
   - If Python is not installed, download it from the [Python official website](https://www.python.org/downloads/) .

2. **Git**: Git must be installed to clone the repository.

    To check:
     ```bash
     git --version
     ```
   - If Git is not installed, download it from the [Git official website](https://git-scm.com/downloads) .

3. **AlienVault OTX API Key**: An AlienVault OTX API key is required to fetch threat data..
   - To generate an API key, sign up on [AlienVault OTX](https://otx.alienvault.com/api/) and create your API key..
   - Add the API key to the threat_intel_tool.py file:
     ```python
     API_KEY = 'your_api_key_here'
     ```

### Python Dependencies
This tool requires some Python packages to run, which are listed in the requirements.txt file. To install them, run this command:
```bash
pip install -r requirements.txt

⚡ Usage

Run the tool with the following command:
python3 threat_dashboard.py

Access the interactive dashboard in your browser to start exploring threat intelligence.

📸 Preview
![Image](https://github.com/user-attachments/assets/3116c936-9f10-4df5-8000-8546528bb9d4)




🛡️ Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

📞 Contact

If you have any questions or suggestions, reach out to me on Discord:

lucky03464

