# Lumu Technologies

Backend Integrations Test

## Prerequisites

- Installed Python 3.x
- Virtual environment (recommended)

## Setting up the Virtual Environment

Clone the repository:

```bash
git clone https://github.com/davidcasr/lumu-test.git
```

## Installation

Navigate to the repository directory
```
cd your-repository
```

Create a virtual env
```
virtualenv venv or python -m venv venv
```

Activate the virtual environment
```
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

Install the requirements

```
pip install -r requirements.txt
```

## Running the Script
Ensure the virtual environment is activated.

Run the script from the command line:

``` bash
python script.py
```

Make sure the log file is located in logs/queries or adjust the file_path variable as needed.

The script will print statistics and send data to the API in batches.

## Additional Configuration

If you need to configure credentials or specific settings, be sure to review and modify the `.env.example` file before running the script.

Previously, you must create a `.env` file following the example in the .`env.example` file and include the used credentials.

## Support Links

- Custom Collector API Specifications https://docs.lumu.io/portal/en/kb/articles/cc-api-specifications#Send_DNS_Queries
- ¿Cómo crear un entorno o ambiente virtual en Python? https://davidcasr.medium.com/c%C3%B3mo-crear-un-entorno-o-ambiente-virtual-en-python-57a1607a4180
- Archivos .env en Python https://davidcasr.medium.com/archivos-env-en-python-c80ec95cb991